from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTextEdit, QGridLayout, QMainWindow, QVBoxLayout

import button


class WindowGui(QMainWindow):
    def __init__(self, api):
        super().__init__()
        # 定义一些后面要用的变量
        self.button = None
        self.text_show_answer_content = None
        self.text_show_reasoning_content = None

        self.api = api
        self.reasoning_text = self.api.reasoning_content_output_spread
        self.answer_text = self.api.answer_content_output_spread
        self.init_window()

        # reasoning_content_updated_signal作为激活信号激活self.update_reasoning_text
        # 并将信号的内容传入到self.update_reasoning_text
        self.api.reasoning_content_updated_signal.connect(self.update_reasoning_text)

        # answer_content_updated_signal作为激活信号激活self.update_answer_text
        # 并将信号的内容传入到self.update_answer_text
        self.api.answer_content_updated_signal.connect(self.update_answer_text)

        # 监听思考和回答完成信号
        self.api.finished_signal.connect(self.output_token_ends)

    def init_window(self):
        self.resize(1000, 700)
        self.move(550, 200)
        # self.setFixedSize(300, 300)

        self.setWindowTitle("MarWorld")

        quit_button = button.QuitButton(self)
        model_api_button = button.ModelAndApiSelectButton(self)

        self.statusBar().showMessage('Ready.')
        # 创建一个显示模型的回答内容的显示框
        self.text_show_answer_content = QTextEdit()
        self.text_show_answer_content.setText(self.answer_text)
        self.text_show_answer_content.setReadOnly(True)  # 只读，不可输入内容
        self.text_show_answer_content.setFixedSize(600, 400)

        # 创建一个显示模型的思考内容的显示框
        self.text_show_reasoning_content = QTextEdit()
        self.text_show_reasoning_content.setText(self.reasoning_text)
        self.text_show_reasoning_content.setReadOnly(True)  # 只读，不可输入内容
        self.text_show_reasoning_content.setFixedSize(300, 700)

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_text)
        # self.timer.start(1000)

        # 用户输入内容的文本框
        input_text_edit = QTextEdit()
        input_text_edit.setPlaceholderText("在这里输入内容...")
        input_text_edit.setFixedSize(600, 200)

        button_container = QWidget()
        button_layout = QVBoxLayout()
        button_layout.addWidget(quit_button)
        button_layout.addWidget(model_api_button)
        button_container.setLayout(button_layout)
        # 设置按钮间距为 0，确保它们上下挨着
        button_layout.setSpacing(0)

        # 使用吊炸天的网格布局来管理元素大小和位置
        layout = QGridLayout()
        layout.addWidget(self.text_show_answer_content, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.text_show_reasoning_content, 0, 1, 2, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(button_container, 0, 3, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(input_text_edit, 1, 0, Qt.AlignmentFlag.AlignTop)
        # 防止AlignmentFlag.AlignLeft导致quit_button的大小被挤成0,0直接vanish
        quit_button.setMinimumSize(135, 60)
        model_api_button.setMinimumSize(100, 50)

        # 使用QWidet来设置布局
        central_widget = QWidget(self)
        # 将网格布局设置为central_widget的布局管理器
        central_widget.setLayout(layout)
        # 设置中心布局为central_widget
        self.setCentralWidget(central_widget)

    def update_reasoning_text(self, text):
        self.reasoning_text = text
        self.text_show_reasoning_content.setText(self.reasoning_text)
        self.statusBar().showMessage('正在输出思考内容...')

    def update_answer_text(self, text):
        self.answer_text = text
        self.text_show_answer_content.setText(self.answer_text)
        self.statusBar().showMessage('正在输出回答内容...')

    def output_token_ends(self):
        self.statusBar().showMessage("Ready.")
