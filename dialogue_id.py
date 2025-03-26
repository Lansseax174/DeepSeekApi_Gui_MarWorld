import os
import json
from typing import cast

from settings import  Setting

setting = Setting()
# [打开窗口]ID+1
# [切换API/模型]ID+1

class DialogueID:
    def __init__(self):
        self.json_filename = None
        self.current_id = None
        self.file_path = None
        self.dialogue_id = None

        self.init_currentID_by_json()
        self.get_next_id()

    def get_next_id(self):
        # 10位对话ID,计算int前0的数量后转为str并拼接在前面
        zero_front_of_int = 10 - len(str(self.current_id))
        self.dialogue_id = ('0' * zero_front_of_int) + str(self.current_id)
        self.current_id += 1

        with open(self.file_path, 'w', encoding='utf-8-sig') as object:
            json.dump(self.current_id, cast("SupportsWrite[str]", object), ensure_ascii=False, indent=4)


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

