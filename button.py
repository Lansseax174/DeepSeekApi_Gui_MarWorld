from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLabel, \
    QLineEdit, QHBoxLayout
from settings import Setting
from worker_thread import WorkerThread
import os
setting = Setting()

api_key = 'Your_Api_Key'
model_key = 'deepseek-v3.1'

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
        self.new_model = None

        self.confirm_button = None
        self.text_show_now_api = None
        self.text1 = None
        self.setWindowTitle("模型和API选择")
        self.resize(*setting.model_api_select_window)  # 设置子窗口的大小

        # 创建一个中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowModality(Qt.WindowModality.WindowModal)  # 设置为窗口模态
        # 创建一个布局
        layout = QVBoxLayout()

        self.text1 = QLabel('当前     api:')
        self.text2 = QLabel('当前model:')

        # 显示当前使用的api
        self.text_show_now_api = QLineEdit(api_key)
        self.text_show_now_api.setReadOnly(True)

        # 显示当前使用的model
        self.text_show_now_model = QLineEdit(model_key)
        self.text_show_now_model.setReadOnly(True)

        # 修改api输入框
        self.text_edit_api = QTextEdit()
        self.text_edit_api.setFixedSize(400, 70)
        self.text_edit_api.setPlaceholderText("在这里输入api")

        # 确认api按钮
        self.confirm_button_api = QPushButton('确认api')
        self.confirm_button_api.setFixedSize(100, 70)
        self.confirm_button_api.clicked.connect(self.update_api)

        # 修改model输入框
        self.text_edit_model = QTextEdit()
        self.text_edit_model.setFixedSize(400,70)
        self.text_edit_model.setPlaceholderText("在这里输入model")

        # 确认model按钮
        self.confirm_button_model = QPushButton('确认model')
        self.confirm_button_model.setFixedSize(100,70)
        self.confirm_button_model.clicked.connect(self.update_model)


        self.horizon_Layout1 = QHBoxLayout()
        self.horizon_Layout1.addWidget(self.text1)
        self.horizon_Layout1.addWidget(self.text_show_now_api)

        self.horizon_Layout2 = QHBoxLayout()
        self.horizon_Layout2.addWidget(self.text2)
        self.horizon_Layout2.addWidget(self.text_show_now_model)

        self.horizon_Layout3 = QHBoxLayout()
        self.horizon_Layout3.addWidget(self.text_edit_api)
        self.horizon_Layout3.addWidget(self.confirm_button_api)

        self.horizon_Layout4 = QHBoxLayout()
        self.horizon_Layout4.addWidget(self.text_edit_model)
        self.horizon_Layout4.addWidget(self.confirm_button_model)

        layout.addLayout(self.horizon_Layout1)
        layout.addLayout(self.horizon_Layout2)
        layout.addLayout(self.horizon_Layout3)
        layout.addLayout(self.horizon_Layout4)

        self.close_button = QPushButton("关闭")
        self.close_button.setFixedSize(80,50)
        self.close_button.clicked.connect(self.close)  # 点击按钮关闭窗口
        layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 设置布局
        central_widget.setLayout(layout)

    def update_api(self):
        # 将输入框api更新并使用
        global api_key
        self.new_api = self.text_edit_api.toPlainText().strip()
        if self.new_api:
            api_key = self.new_api
            self.text_show_now_api.setText(api_key)

    def update_model(self):
        # 将输入框api更新并使用
        global model_key
        self.new_model = self.text_edit_model.toPlainText().strip()
        if self.new_model:
            model_key = self.new_model
            self.text_show_now_model.setText(model_key)



class ModelAndApiSelectButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_api_window = None

        QToolTip.setFont(QFont('SansSerif', 10))
        self.btn = QPushButton('Api-Model更改', self)
        font = QFont('华文琥珀', 13)  # 字体设置为Arial，大小为14
        self.btn.setFont(font)
        self.btn.clicked.connect(self.open_model_api_window)
        self.btn.setFixedSize(*setting.model_api_select_button)

    def open_model_api_window(self):
        parent = self.parent()
        self.model_api_window = ModelAndApiSelectWindow(parent)
        # 实例化更改model和api的界面
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
    def __init__(self,dialogue_id, dialouge_list1):
        super().__init__()
        self.dialouge_list1 = dialouge_list1
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
        self.dialogue_id.current_id_plus()
        self.dialouge_list1.load_dialogue_list()
        first_item = self.dialouge_list1.dialogue_list.item(0)
        if first_item:
            self.dialouge_list1.on_item_clicked2(first_item)