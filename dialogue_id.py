import os
import json
from typing import cast

from settings import  Setting

setting = Setting()
# [打开窗口]ID+1
# [切换API/模型]ID+1

class DialogueID:
    def __init__(self):
        self.zero_front_of_int = None
        self.current_id = None
        self.file_path = None
        self.dialogue_id = None

        self.init_currentID_by_json()
        self.get_dialogue_id()
        self.json_filename = os.path.join('LogDialogue', 'DialogueContentLog', f"{self.dialogue_id}.json")
        self.current_id_plus()

    def get_dialogue_id(self):
        # 10位对话ID,计算int前0的数量后转为str并拼接在前面
        self.zero_front_of_int = 10 - len(str(self.current_id))
        self.dialogue_id = ('0' * self.zero_front_of_int) + str(self.current_id)

    def current_id_plus(self):
        if self.dialogue_id_has_used():
            print('当前对话使用过')
            self.current_id += 1
            self.get_dialogue_id()
            self.json_filename = os.path.join('LogDialogue', 'DialogueContentLog', f"{self.dialogue_id}.json")
            with open(self.file_path, 'w', encoding='utf-8-sig') as object:
                json.dump(self.current_id, cast("SupportsWrite[str]", object), ensure_ascii=False, indent=4)
            self.make_dialogue_log_json()
        else:
            print('当前对话ID未使用过，不改变ID')

    def init_currentID_by_json(self):
        os.makedirs('LogDialogue', exist_ok=True)  # 确保目录存在

        self.file_path = 'LogDialogue\DialogueIDLog.json'
        # 判断文件是否存在
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8-sig') as object:
                self.current_id = int(object.read().strip())
                print(f'已读取Json文件:---\n{self.file_path}\n{self.current_id}\n---')
        else:

            with open(self.file_path, 'w', encoding='utf-8-sig') as object:
                object.write(str(setting.start_number_dialogue_id))
                print(f'已创建Json文件:{self.file_path}, 数值:{setting.start_number_dialogue_id}')
                self.current_id = setting.start_number_dialogue_id

    def make_dialogue_log_json(self):
        # 创建多级目录，确保指定的文件夹存在，如果目录已经存在，则不会报错
        os.makedirs('LogDialogue\DialogueContentLog', exist_ok=True)

        self.json_filename = os.path.join(
            'LogDialogue', 'DialogueContentLog', f"{self.dialogue_id}.json")
        default_data = {"dialogues": []}

        if os.path.exists(self.json_filename):
            print('当前对话ID已创建且未使用。')
        else:
            with open(self.json_filename, 'w', encoding='utf-8-sig') as object:
                json.dump(default_data, cast("SupportsWrite[str]", object), ensure_ascii=False, indent=4)

    def dialogue_id_has_used(self):
        # 判断当前ID是否有对话记录，如果没有，则不改变对话ID
        if not os.path.exists(self.json_filename):
            print('当前对话ID的Json文件不存在')
            self.make_dialogue_log_json()
            print('当前对话ID的Json文件已创建')

        try:
            with open(self.json_filename, 'r', encoding='utf-8-sig') as object:
                temp_data = json.load(object)
                if len(temp_data['dialogues']) == 0:
                    return False  # 如果dialogues为空，则说明没有使用过，返回False
                else:
                    return True
        except json.JSONDecodeError:
            print('damn我崩了!Json解析失败')