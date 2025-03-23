from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys

class ChatBubble(QWidget):
    """ 自定义聊天气泡 """
    def __init__(self, sender, text, align="left", avatar_path="default_avatar.png"):
        super().__init__()

        layout = QHBoxLayout()

        # 头像
        avatar = QLabel(self)
        avatar.setPixmap(QPixmap(avatar_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                                     Qt.TransformationMode.SmoothTransformation))
        avatar.setFixedSize(40, 40)

        # 消息文本
        message = QLabel(text)
        message.setWordWrap(True)
        message.setStyleSheet(
            f"background-color: {'#a0cfff' if align == 'right' else '#d3d3d3'}; "
            "padding: 8px; border-radius: 8px; font-size: 14px;"
        )
        message.setMaximumWidth(300)  # 限制最大宽度，模拟微信气泡
        message.setMinimumHeight(40)  # 最小高度

        # 发送者名称
        sender_label = QLabel(f"{sender}")
        sender_label.setStyleSheet("font-weight: bold; font-size: 12px;")

        message_layout = QVBoxLayout()
        message_layout.addWidget(sender_label)
        message_layout.addWidget(message)
        message_layout.setContentsMargins(5, 5, 5, 5)

        if align == "left":  # 对方消息，头像在左
            layout.addWidget(avatar)
            layout.addLayout(message_layout)
            layout.addStretch()
        else:  # 自己的消息，头像在右
            layout.addStretch()
            layout.addLayout(message_layout)
            layout.addWidget(avatar)

        self.setLayout(layout)

class ChatWindow(QWidget):
    """ 聊天窗口 """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("微信风格聊天窗口")
        self.setGeometry(100, 100, 600, 500)

        # 聊天记录窗口
        self.chat_list = QListWidget(self)
        self.chat_list.setFixedSize(580, 400)

        # 输入框
        self.input_text = QLineEdit(self)
        self.input_text.setFixedSize(500, 30)

        # 发送按钮
        self.send_button = QPushButton("发送", self)
        self.send_button.setFixedSize(80, 30)
        self.send_button.clicked.connect(self.send_message)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.chat_list)
        layout.addWidget(self.input_text)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_message(self):
        """ 发送自己的消息，并模拟对方回复 """
        text = self.input_text.text().strip()
        if text:
            self.add_message("我", text, "right", "my_avatar.png")  # 右侧显示自己的消息
            self.input_text.clear()

            # 模拟对方的回复
            self.add_message("对方", "你好，我是对方！", "left", "friend_avatar.png")

    def add_message(self, sender, text, align, avatar):
        """ 在聊天窗口添加一条消息 """
        item = QListWidgetItem()
        chat_bubble = ChatBubble(sender, text, align, avatar)

        item.setSizeHint(chat_bubble.sizeHint())  # 适配气泡大小
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, chat_bubble)

        self.chat_list.scrollToBottom()  # 滚动到底部


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
