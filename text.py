import sys
import os
from PyQt6.QtWidgets import QApplication, QListWidget, QVBoxLayout, QWidget

LOG_DIR = "log"  # 日志目录

class ChatListWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 创建列表控件
        self.chat_list = QListWidget()
        self.load_chat_list()  # 加载 JSON 文件

        # 设置布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.chat_list)

    def load_chat_list(self):
        """加载 log 目录下的 JSON 文件到列表"""
        self.chat_list.clear()
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        for file in os.listdir(LOG_DIR):
            if file.endswith(".json"):
                self.chat_list.addItem(file[:-5])  # 显示文件名（去掉 .json）

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ChatListWidget()
    widget.show()  # 直接显示 JSON 文件列表
    sys.exit(app.exec())
