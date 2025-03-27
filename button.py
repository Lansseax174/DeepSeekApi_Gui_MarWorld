from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QVBoxLayout, QTextEdit
from settings import Setting
from worker_thread import WorkerThread

setting = Setting()

class QuitButton(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        QToolTip.setFont(QFont('SansSerif', 10))
        # QToolTip.setFont(QFont('华文琥珀', 10))
        # 创建QPushButton
        self.btn = QPushButton('退出MarWorld', self)

        # 字体设置为Arial，大小为14
        self.btn.setFont(QFont(*setting.quit_button_Font))

        # 绑定按钮作用
        self.btn.clicked.connect(QApplication.quit)

        # 鼠标挪上去显示个提示
        self.btn.setToolTip('退出按钮')

        # 设置按钮固定大小
        self.btn.setFixedSize(*setting.quit_button)


class ModelAndApiSelectWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_edit = None
        self.setWindowTitle("模型和API选择")
        self.resize(*setting.model_api_select_window)  # 设置子窗口的大小

        # 创建一个中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowModality(Qt.WindowModality.WindowModal)  # 设置为窗口模态
        # 创建一个布局
        layout = QVBoxLayout()

        # 添加一些控件（示例：一个文本编辑框和一个按钮）
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入内容...")
        layout.addWidget(self.text_edit)

        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)  # 点击按钮关闭窗口
        layout.addWidget(self.close_button)

        # 设置布局
        central_widget.setLayout(layout)


class ModelAndApiSelectButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_api_window = None

        QToolTip.setFont(QFont('SansSerif', 10))
        self.btn = QPushButton('Api-Model', self)
        font = QFont('华文琥珀', 13)  # 字体设置为Arial，大小为14
        self.btn.setFont(font)
        self.btn.clicked.connect(self.open_model_api_window)
        self.btn.setFixedSize(*setting.model_api_select_button)

    def open_model_api_window(self):
        parent = self.parent()
        self.model_api_window = ModelAndApiSelectWindow(parent)
        self.model_api_window.show()

# [发送]按钮功能
class InputTextEditButton(QWidget):
    def __init__(self, input_text_edit, api, chat_window, log_object):
        super().__init__()
        self.log_object = log_object
        self.thread_caa = None
        self.chat_window = chat_window
        self.api = api
        self.input_text = None
        self.input_text_edit = input_text_edit
        QToolTip.setFont(QFont('SansSerif', 10))
        # QToolTip.setFont(QFont('华文琥珀', 10))
        # 创建QPushButton
        self.btn = QPushButton('发送', self)

        # 字体设置为Arial，大小为14
        self.btn.setFont(QFont(*setting.input_text_edit_button_Font))

        # 绑定按钮作用
        self.btn.clicked.connect(self.process_input_text)
        self.btn.setShortcut("Return")
        # 鼠标挪上去显示个提示
        self.btn.setToolTip('man!')

        # 设置按钮固定大小
        self.btn.setFixedSize(*setting.input_text_edit_button)

    def process_input_text(self):
        self.input_text = self.input_text_edit.toPlainText()
        self.log_object.logging_user_input_content(self.input_text)
        self.chat_window.user_text = self.input_text
        self.chat_window.send_message(self.input_text)

        # # 通过线程异步运行阿里云api的调用类
        # self.thread_caa = WorkerThread(self.api, self.input_text)
        # self.thread_caa.start()

        print(self.input_text)
        self.input_text_edit.clear()