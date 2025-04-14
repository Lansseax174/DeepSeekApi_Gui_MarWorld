from datetime import datetime
import os
import json

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget

dialogue_content_log = 'LogDialogue\DialogueContentLog'


class DialogueIdListWinodw(QWidget):
    chat_bubble_add_assistant = pyqtSignal(str)
    chat_bubble_add_user = pyqtSignal(str)
    clean_bubble = pyqtSignal()
    update_dialogueID_window = pyqtSignal(str)
    chat_bubble_time = pyqtSignal(str)
    def __init__(self, log_dialogue, dialogue_id1):
        super().__init__()
        self.selected_file_path = None
        self.selected_filename = None
        self.data = None
        self.log_dialogue = log_dialogue
        self.dialogue_id1 = dialogue_id1
        self.dialogue_list = QListWidget()
        # self.load_dialogue_list()
        # 载入魅力的json文件列表 (注释化，丢到chat_display_screen.py里运行这一行了，
        # 因为self.on_item_clicked(self.dialogue_list.item(0))这一行导致的

        layout = QVBoxLayout(self)
        layout.addWidget(self.dialogue_list)
        self.dialogue_list.itemClicked.connect(self.on_item_clicked2)

    def load_dialogue_list(self):

        self.dialogue_list.clear()

        if not os.path.exists(dialogue_content_log):
            os.makedirs(dialogue_content_log)
            print('存储对话log文件的目录不存在')

        # 获取所有 Json文件的文件名(不包括路径)
        json_files = [
            file for file in os.listdir(dialogue_content_log)
            if file.endswith(".json")
        ]

        # json_files排序.key = lambda 建立一个匿名函数 获取 file文件的时间戳来排序，reverse决定排序顺序是正还是反
        json_files.sort(key = lambda file: os.path.getctime(os.path.join(dialogue_content_log, file))
                        ,reverse = True)

        # for file in json_files:
        #     self.dialogue_list.addItem(file[:-5])
        for file in json_files:
            # 去掉文件名后5个字符(既.json)
            read_file_name = file[0:-5]

            timestamp = os.path.getmtime(os.path.join(dialogue_content_log,file))

            read_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            self.dialogue_list.addItem(f"{read_file_name}\n({read_time})")

        self.dialogue_list.setCurrentItem(self.dialogue_list.item(0))
        self.on_item_clicked1(self.dialogue_list.item(0))

    def load_dialogues_from_json(self):
        try:
            dialogues = self.data.get("dialogues", [])
        except Exception:
            print('[错误] 获取 dialogues 失败')
            return
        try:
            for dialogue in dialogues:
                time = dialogue["time"]
                text = dialogue["content"]
                type1 = dialogue["type"]
                if type1 == "user":
                    self.chat_bubble_time.emit(time)
                    self.chat_bubble_add_user.emit(text)
                elif type1 == "answer":
                    self.chat_bubble_time.emit(time)
                    self.chat_bubble_add_assistant.emit(text)
        except Exception:
            print('[错误] for dialogue in dialogues 失败')
            return
        print(dialogues)
    #
    # def get_lastest_modify_time(self):

    def on_item_clicked1(self, item):
        self.selected_filename = item.text()
        # 获取点中的文件的文件名
        self.selected_file_path = os.path.join(
            'LogDialogue', 'DialogueContentLog', f"{self.selected_filename[:-22]}.json")

        self.log_dialogue.log_file = os.path.join(
            'LogDialogue', 'DialogueContentLog', f'{self.selected_filename[:-22]}.json')

        with open(self.selected_file_path, 'r', encoding='utf-8-sig') as log_file_object:
            self.data = json.load(log_file_object)

        print('选中')
        # self.update_dialogueID_window.emit(f'{self.selected_filename[:-22]}.json')
        self.clean_bubble.emit()
        self.load_dialogues_from_json()

    def on_item_clicked2(self, item):
        self.selected_filename = item.text()
        # 获取点中的文件的文件名
        self.selected_file_path = os.path.join(
            'LogDialogue', 'DialogueContentLog', f"{self.selected_filename[:-22]}.json")

        self.log_dialogue.log_file = os.path.join(
            'LogDialogue', 'DialogueContentLog', f'{self.selected_filename[:-22]}.json')

        with open(self.selected_file_path, 'r', encoding='utf-8-sig') as log_file_object:
            self.data = json.load(log_file_object)

        print('选中')
        self.dialogue_id1.dialogue_id = f'{self.selected_filename[:-22]}.json'
        self.update_dialogueID_window.emit(f'{self.selected_filename[:-22]}')
        print(f'{self.selected_filename[:-22]}' + "\n----")
        self.clean_bubble.emit()
        self.load_dialogues_from_json()