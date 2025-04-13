import os
import json

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget

dialogue_content_log = 'LogDialogue\DialogueContentLog'


class DialogueIdListWinodw(QWidget):
    chat_bubble_add_assistant = pyqtSignal(str)
    chat_bubble_add_user = pyqtSignal(str)
    clean_bubble = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.dialogue_list = QListWidget()
        self.load_dialogue_list()  # 载入魅力的json文件列表

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

    def load_dialogues_from_json(self):
        try:
            dialogues = self.data.get("dialogues", [])
        except Exception as e:
            print('[错误] 获取 dialogues 失败')
            return
        try:
            for dialogue in dialogues:
                text = dialogue["content"]
                type = dialogue["type"]
                print('0')
                if type == "user":
                    self.chat_bubble_add_user.emit(text)
                elif type == "answer":
                    self.chat_bubble_add_assistant.emit(text)
        except Exception as e:
            print('[错误] for dialogue in dialogues 失败')
            return
        print(dialogues)

    def on_item_clicked(self, item):
        self.selected_filename = item.text()
        # 获取点中的文件的文件名
        self.selected_file_path = os.path.join('LogDialogue', 'DialogueContentLog', f"{self.selected_filename}.json")

        with open(self.selected_file_path, 'r', encoding='utf-8-sig') as log_file_object:
            self.data = json.load(log_file_object)

        print('选中')
        self.clean_bubble.emit()
        self.load_dialogues_from_json()

