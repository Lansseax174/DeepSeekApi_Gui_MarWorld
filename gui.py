from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QTextEdit, QGridLayout, QStatusBar, QMainWindow

from button import Button


class WindowGui(QMainWindow):
    def __init__(self, api):
        super().__init__()
        # 定义一些后面要用的变量
        self.button = None

        self.api = api
        self.reasoning_text = self.api.reasoning_content_output_spread
        self.answer_text = self.api.answer_content_output_spread
        self.init_window()

        # reasoning_content_updated_signal作为激活信号激活self.update_text
        # 并将信号的内容传入到self.update_text
        self.api.reasoning_content_updated_signal.connect(self.update_reasoning_text)
        self.api.answer_content_updated_signal.connect(self.update_answer_text,
                                                       Qt.ConnectionType.QueuedConnection)

    def init_window(self):
        self.resize(1000, 700)
        self.move(550, 200)
        # self.setFixedSize(300, 300)

        self.setWindowTitle("MarWorld")

        self.button = Button(self)
        self.statusBar().showMessage('Ready')

        # 创建一个显示模型的回答内容的显示框
        self.text_show_answer_content = QTextEdit()
        self.text_show_answer_content.setText(self.answer_text)
        self.text_show_answer_content.setReadOnly(True)
        self.text_show_answer_content.setFixedSize(600, 400)

        # 创建一个显示模型的思考内容的显示框
        self.text_show_reasoning_content = QTextEdit()
        self.text_show_reasoning_content.setText(self.reasoning_text)
        self.text_show_reasoning_content.setReadOnly(True)
        self.text_show_reasoning_content.setFixedSize(300, 700)


        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_text)
        # self.timer.start(1000)

        # 使用吊炸天的网格布局来管理元素大小和位置
        layout = QGridLayout()
        layout.addWidget(self.text_show_answer_content, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.text_show_reasoning_content, 0, 1, 2, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.button, 1, 0, Qt.AlignmentFlag.AlignLeft)
        # 防止AlignmentFlag.AlignLeft导致button的大小被挤成0,0直接vanish
        self.button.setMinimumSize(100, 50)

        # 使用QWidet来设置布局
        central_widget = QWidget(self)
        # 将网格布局设置为central_widget的布局管理器
        central_widget.setLayout(layout)
        # 设置中心布局为central_widget
        self.setCentralWidget(central_widget)

    def update_reasoning_text(self, text):
        self.reasoning_text = text
        self.text_show_reasoning_content.setText(self.reasoning_text)

    def update_answer_text(self, text):
        self.answer_text = text
        self.text_show_answer_content.setText(self.answer_text)
