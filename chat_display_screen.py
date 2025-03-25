from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QListWidget, QListWidgetItem, QSizePolicy


class ChatBubble(QWidget):
    def __init__(self, sender, text, align, avatar_path, api, setting):
        super().__init__()
        self.text = text
        self.api = api
        self.setting = setting

        layout = QHBoxLayout()

        # 头像
        avatar = QLabel(self)
        # 尺寸限制，保持比例，平滑缩放
        set_avatar = QPixmap(avatar_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
        avatar.setPixmap(set_avatar)
        avatar.setFixedSize(40, 40)

        # 消息文本
        self.message = QLabel(text)
        self.message.setWordWrap(True)  # 自动换行true
        self.message.setStyleSheet(
            f"background-color: {'rgb(158, 234, 106)' if align == 'right' else 'rgb(225, 225, 225)'};"
            f"color: { 'rgb(0, 0, 0)' if align == 'right' else 'rgb(0, 0, 0)'}"
            "; padding: 8px; border-radius: 8px; font-size: 14px;"
        )  # 气泡设置
        # 让气泡内的文本可以被选中操作
        self.message.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.message.setMaximumSize(*self.setting.message_MaximumSize)  # 最大宽度和高度
        self.message.setMinimumSize(*self.setting.message_MinimumSize)   # 最小宽度和高度

        # 发送者名称显示
        sender_label = QLabel(f"{sender}")
        sender_label.setStyleSheet("font-weight: bold; font-size: 12px")  # 加粗,字体大小

        # 垂直布局(VBox)
        message_layout = QVBoxLayout()
        message_layout.addWidget(sender_label)
        message_layout.addWidget(self.message)
        message_layout.setContentsMargins(5, 5, 5, 5)  # 左，上，右，下的内边距设置


        # 模拟对话，align是left代表左边[对方]，否则是右边[自己]
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

    def __init__(self, api, setting):
        super().__init__()
        self.setting = setting
        self.user_make_bubble_judge = 0
        self.assistant_answer_text = ''
        self.api = api
        self.api.start_answer.connect(self.send_assistant_message)
        self.api.answer_content_updated_signal.connect(self.update_stream_text)
        self.api.stop_answer.connect(self.allow_make_bubble)
        self.chat_bubble1 = None
        self.user_text = None
        self.setWindowTitle("类Wechat窗口")

        # 聊天记录窗口创建
        self.chat_list = QListWidget(self)
        self.chat_list.setMinimumSize(*self.setting.chat_window)

    def send_assistant_message(self):
        print('work3')
        self.add_message('DeepSeek', self.assistant_answer_text, 'left', "my_avatar.png")

    def send_message(self, text):
        self.user_text = text
        print('work1')
        if self.user_text:
            self.user_make_bubble_judge = 1
            self.add_message('我', self.user_text, 'right', "my_avatar.png")


    def add_message(self, sender, text, align, avatar):
        # QListWidget中的一个项，承载具体的内容
        item = QListWidgetItem()
        self.chat_bubble1 = ChatBubble(sender, text, align, avatar, self.api, self.setting)
        item.setSizeHint(self.chat_bubble1.sizeHint())  # 设置item显示的大小
        self.chat_list.addItem(item)  # 将item加入到chat_list
        self.chat_list.setItemWidget(item, self.chat_bubble1)  # 使每一个item显示为chat_bubble组件，而不是静态文本
        self.chat_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.chat_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)  # 让滚动条按像素平滑滚动
        self.chat_list.scrollToBottom() # 当有新内容加入时，自动滚动到底部
        self.chat_list.repaint()  # 强制 UI 更新
        print('work2')

    def allow_make_bubble(self):
        print('allow_make_bubble')
        self.chat_bubble1 = None

    def update_stream_text(self, new_text):
        if self.chat_bubble1:
            self.chat_bubble1.message.setText(new_text)  # 更新文本
            item = self.chat_list.item(self.chat_list.count() - 1)  # 获取最新消息的 item
            if item:
                item.setSizeHint(self.chat_bubble1.sizeHint())  # 重新调整大小
            self.chat_list.scrollToBottom()  # 保持滚动到底部
            self.chat_list.repaint()  # 强制 UI 更新