from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLabel, \
    QLineEdit, QHBoxLayout
from settings import Setting
from worker_thread import WorkerThread

setting = Setting()
api_key = 'REMOVED_KEY7baa2a5a6bf04b91aaf5eec210a4f0e6'

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
        self.new_api = None

        self.confirm_button = None
        self.text_show_now_api = None
        self.text_edit = None
        self.text1 = None
        self.setWindowTitle("模型和API选择")
        self.resize(*setting.model_api_select_window)  # 设置子窗口的大小

        # 创建一个中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowModality(Qt.WindowModality.WindowModal)  # 设置为窗口模态
        # 创建一个布局
        layout = QVBoxLayout()

        self.text1 = QLabel('当前api:')

        # 显示当前使用的api
        self.text_show_now_api = QLineEdit(api_key)
        self.text_show_now_api.setReadOnly(True)

        # 修改api输入框
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入内容...")

        # 确认按钮
        self.confirm_button = QPushButton('确认')
        self.confirm_button.clicked.connect(self.update_api)


        self.horizon_Layout = QHBoxLayout()
        self.horizon_Layout.addWidget(self.text1)
        self.horizon_Layout.addWidget(self.text_show_now_api)

        layout.addLayout(self.horizon_Layout)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.confirm_button)

        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)  # 点击按钮关闭窗口
        layout.addWidget(self.close_button)

        # 设置布局
        central_widget.setLayout(layout)
    def update_api(self):
        # 将输入框api更新并使用
        global api_key
        self.new_api = self.text_edit.toPlainText().strip()
        if self.new_api:
            api_key = self.new_api
            self.text_show_now_api.setText(api_key)



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

        # 通过线程异步运行阿里云api的调用类
        self.thread_caa = WorkerThread(self.api, self.input_text)
        self.thread_caa.start()

        print(self.input_text)
        self.input_text_edit.clear()

# [新聊天]按钮功能
class MakeNewChatButton(QWidget):
    def __init__(self,dialogue_id):
        super().__init__()
        self.dialogue_id = dialogue_id
        QToolTip.setFont(QFont('SansSerif', 10))
        # QToolTip.setFont(QFont('华文琥珀', 10))
        # 创建QPushButton
        self.btn = QPushButton('新聊天', self)

        # 字体设置为Arial，大小为14
        self.btn.setFont(QFont(*setting.input_text_edit_button_Font))

        # 绑定按钮作用
        self.btn.clicked.connect(self.make_new_chat)
        self.btn.setShortcut("创建新的聊天")
        # 鼠标挪上去显示个提示
        self.btn.setToolTip('man!what can I say?')

        # 设置按钮固定大小
        self.btn.setFixedSize(*setting.input_text_edit_button)

    def make_new_chat(self):
        print('创建新的聊天')