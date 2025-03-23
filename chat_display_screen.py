import sys

from PIL.ImageQt import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QListWidget, QApplication, QListWidgetItem


class ChatBubble(QWidget):
    def __init__(self, sender, text, align, avatar_path):
        super().__init__()

        layout = QHBoxLayout()

        # 头像
        avatar = QLabel(self)
        # 尺寸限制，保持比例，平滑缩放
        set_avater = QPixmap(avatar_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
        avatar.setPixmap(set_avater)
        avatar.setFixedSize(40, 40)

        # 消息文本
        message = QLabel(text)
        message.setWordWrap(True)  # 自动换行true
        message.setStyleSheet(
            f"background-color: {'#a0cfff' if align == 'right' else '#d3d3d3'};"
            "padding: 8px; border-radius: 8px; font-size: 14px;"
        )  # 气泡设置
        message.setMaximumSize(300, 400)  # 最大宽度和高度
        message.setMinimumSize(30, 40)   # 最小高度

        # 发送者名称显示
        sender_label = QLabel(f"{sender}")
        sender_label.setStyleSheet("font-weight: bold; font-size: 12px")  # 加粗,字体大小

        # 垂直布局(VBox)
        message_layout = QVBoxLayout()
        message_layout.addWidget(sender_label)
        message_layout.addWidget(message)
        message_layout.setContentsMargins(5, 5, 5, 5)  # 左，上，右，下的内边距设置

        if align == 'left':
            layout.addWidget(avatar)
            layout.addLayout(message_layout)
            layout.addStretch()
        else:
            layout.addStretch()
            layout.addLayout(message_layout)
            layout.addWidget(avatar)
        self.setLayout(layout)

class ChatWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("类Wechat窗口")
        self.setGeometry(100, 100, 600, 500)  # x位置,y位置，宽度，高度

        # 聊天记录窗口
        self.chat_list = QListWidget(self)
        self.chat_list.setFixedSize(580, 400)

    def send_message(self):
        text = 'aaaaaaaaaaaaaa'
        if text:
            self.add_message('我', text, 'right', "my_avatar.png")

    def add_message(self, sender, text, align, avatar):
        # QListWidget中的一个项，承载具体的内容
        item = QListWidgetItem()
        chat_bubble = ChatBubble(sender, text, align, avatar)

        item.setSizeHint(chat_bubble.sizeHint())  # 设置item显示的大小
        self.chat_list.addItem(item)  # 将item加入到chat_list
        self.chat_list.setItemWidget(item, chat_bubble)  # 使每一个item显示为chat_bubble组件，而不是静态文本
        self.chat_list.scrollToBottom() # 当有新内容加入时，自动滚动到底部

app = QApplication(sys.argv)
a = ChatWindow()
a.send_message()
a.show()

sys.exit(app.exec())