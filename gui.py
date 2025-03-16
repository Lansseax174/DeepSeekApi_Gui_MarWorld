from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QTextEdit, QGridLayout, QStatusBar, QMainWindow

from button import Button


class WindowGui(QMainWindow):
    def __init__(self, api):
        super().__init__()
        # 定义一些后面要用的变量
        self.text_show_reasoning_content = None

        self.api = api
        self.text = self.api.reasoning_content_output_spread
        self.init_window()

        # content_updated_signal作为激活信号激活self.update_text
        # 并将信号的内容传入到self.update_text
        self.api.content_updated_signal.connect(self.update_text)

    def init_window(self):
        self.resize(1000, 700)
        self.move(550, 200)
        # self.setFixedSize(300, 300)

        self.setWindowTitle("MarWorld")

        self.button = Button(self)
        self.statusBar().showMessage('Ready')

        self.text_show_reasoning_content = QTextEdit()
        self.text_show_reasoning_content.setText(self.text)
        self.text_show_reasoning_content.setReadOnly(True)
        self.text_show_reasoning_content.setFixedSize(600, 400)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_text)
        # self.timer.start(1000)

        # 使用吊炸天的网格布局来管理元素大小和位置
        layout = QGridLayout()
        layout.addWidget(self.text_show_reasoning_content, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.button, 1, 0,Qt.AlignmentFlag.AlignLeft)
        self.button.setMinimumSize(100, 50)

        # 使用QWidet来设置布局
        central_widget = QWidget(self)
        # 将网格布局设置为central_widget的布局管理器
        central_widget.setLayout(layout)
        # 设置中心布局为central_widget
        self.setCentralWidget(central_widget)

    def update_text(self, text):
        self.text = text
        self.text_edit.setText(self.text)
