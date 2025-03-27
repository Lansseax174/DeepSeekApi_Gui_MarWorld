import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget

dialogue_content_log = 'LogDialogue\DialogueContentLog'

class DialogueIdListWinodw(QWidget):
    def __init__(self):
        super().__init__()

        self.dialogue_list = QListWidget()
        self.load_dialogue_list()  # 载入魅力的json文件

        layout = QVBoxLayout(self)
        layout.addWidget(self.dialogue_list)
        self.dialogue_list.itemClicked.connect(self.on_item_clicked)

    def load_dialogue_list(self):

        self.dialogue_list.clear()

        if not os.path.exists(dialogue_content_log):
            os.makedirs(dialogue_content_log)
            print('存储对话log文件的目录不存在')

        for file in os.listdir(dialogue_content_log):
            if file.endswith(".json"):
                self.dialogue_list.addItem(file[:-5])

    def on_item_clicked(self):
        print('选中！')