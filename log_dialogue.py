import json
import os
from datetime import datetime


def get_time():
    now = datetime.now()
    if now.hour < 12:
        am_pm = '上午'
    else:
        am_pm = '下午'

    if 1 <= now.hour <= 12:
        hour_12 = now.hour
    elif now.hour > 12:
        hour_12 = now.hour - 12
    else:
        hour_12 = 12

    formatted_time = f"{now.year}-{now.month}-{now.day} {am_pm} {hour_12}:{now.minute:02d}"
    # formatted_time = f"{now.year}-{now.month}-{now.day} {am_pm} {hour_12}:{now.minute:02d}"
    # formatted_time = f"\n{now.month}-{now.day}{am_pm}{hour_12}:{now.minute:02d}"
    return formatted_time


class LogContext:
    def __init__(self, api, dialogue_id1):
        self.json_filename = None
        self.add_user_input_dictionary = None
        self.add_api_answer_dictionary = None
        self.add_api_reasoning_dictionary = None
        self.add_reason = 0

        self.dialogue_id1 = dialogue_id1
        self.api = api
        self.log_file = os.path.join(
            'LogDialogue', 'DialogueContentLog', f'{self.dialogue_id1.dialogue_id}.json')

        self.reasoning_content = ''
        self.answer_content = self.api.answer_content_output_spread
        self.formatted_time = get_time()



        # reasoning_content_updated_signal作为激活信号激活self.update_reasoning_text
        # 并将信号的内容传入到self.update_reasoning_text
        self.api.log_reasoning_content_updated_signal.connect(self.logging_api_reasoning_content)
        self.api.log_answer_content_updated_signal.connect(self.logging_api_answer_content)
        self.api.finished_signal.connect(self.finish_api_logging)

        # 根据dialogue_id创建存储对话内容的Json文件
    def update_time(self):
        self.formatted_time = get_time()

    def logging_api_reasoning_content(self, text):
        self.update_time()
        self.add_api_reasoning_dictionary = [
                                             {"time": self.formatted_time,
                                              "role": "assistant",
                                              "type": "reasoning",
                                              "content": text
                                              }
                                             ]

        self.log_call_alibaba_api(self.add_api_reasoning_dictionary)

    def logging_api_answer_content(self, text):
        self.update_time()
        print(text)
        self.add_api_answer_dictionary = [
                                           {"time": self.formatted_time,
                                            "role": "assistant",
                                            "type": "answer",
                                            "content": text
                                           }
                                          ]
        self.log_call_alibaba_api(self.add_api_answer_dictionary)

    def logging_user_input_content(self, text):
        self.update_time()
        self.add_user_input_dictionary = [
                                           {"time": self.formatted_time,
                                            "role": "user",
                                            "type": "user",
                                            "content": text
                                           }
                                          ]
        self.log_call_alibaba_api(self.add_user_input_dictionary)

    @staticmethod
    def finish_api_logging():
        print('finish_api_log')

    def log_call_alibaba_api(self, log_will_add):

        try:
            with open(self.log_file, 'r', encoding='utf-8-sig') as log_file_object:
                content = log_file_object.read().strip()
                if content:
                    data = json.loads(content)
                else:
                    print('json文件为空')
                    data = {"dialogues": []}

        except FileNotFoundError:
            data = {"dialogues": []}
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
        except Exception as e:
            print(f"发生了其他错误: {e}")

        if "dialogues" in data:
            data["dialogues"].extend(log_will_add)
        else:
            data["dialogues"] = log_will_add
        with open(self.log_file, 'w', encoding='utf-8-sig') as log_file_object:
            json.dump(data, log_file_object, ensure_ascii=False, indent=4)



