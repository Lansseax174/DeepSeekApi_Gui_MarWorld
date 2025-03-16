from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QTextEdit, QGridLayout

from button import Button


class WindowGui(QWidget):
    def __init__(self, api):
        super().__init__()

        self.api = api
        self.text = self.api.reasoning_content_output_spread
        self.init_window()

        # content_updated_signal作为激活信号激活self.update_text
        # 并将信号的内容传入到self.update_text
        self.api.content_updated_signal.connect(self.update_text)

    def init_window(self):
        self.resize(1000, 700)
        self.move(550, 200)
        layout = QGridLayout()
        self.setWindowTitle("MarWorld")

        button = Button(self)

        self.text_edit = QTextEdit()
        self.text_edit.setText(self.text)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFixedSize(200, 200)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_text)
        # self.timer.start(1000)

        layout.addWidget(self.text_edit, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button, 1, 0)
        self.setLayout(layout)

    def update_text(self, text):
        self.text = text
        self.text_edit.setText(self.text)
