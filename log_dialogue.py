import json
from typing import cast
import time


class LogContext:
    def __init__(self, api):
        self.add_api_answer_dictionary = None
        self.add_api_reasoning_dictionary = None
        self.add_reason = 0

        self.api = api
        self.log_file = 'log.json'

        self.reasoning_content = ''
        self.answer_content = self.api.answer_content_output_spread
        self.formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())



        # reasoning_content_updated_signal作为激活信号激活self.update_reasoning_text
        # 并将信号的内容传入到self.update_reasoning_text
        self.api.log_reasoning_content_updated_signal.connect(self.logging_api_reasoning_content)
        self.api.log_answer_content_updated_signal.connect(self.logging_api_answer_content)
        self.api.finished_signal.connect(self.finish_api_logging)
    # def logging_user_content(self):
    #
    #
    def update_time(self):
        self.formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def logging_api_reasoning_content(self, text):
        self.update_time()
        self.add_api_reasoning_dictionary = [
                                             {"time": self.formatted_time,
                                              "role": "assistant",
                                              "content": text
                                              }
                                             ]

        self.log_call_alibaba_api(self.add_api_reasoning_dictionary)
    def logging_api_answer_content(self, text):
        self.update_time()
        self.add_api_answer_dictionary = [
                                           {"time": self.formatted_time,
                                            "role": "assistant",
                                            "content": text
                                           }
                                          ]
        self.log_call_alibaba_api(self.add_api_answer_dictionary)
    def finish_api_logging(self):
        print('a')

    def log_call_alibaba_api(self, log_will_add):
        try:
            with open(self.log_file, 'r', encoding='utf-8-sig') as log_file_object:
                data = json.load(log_file_object)
        except FileNotFoundError:
            data = {"dialogues": []}

        if "dialogues" in data:
            data["dialogues"].extend(log_will_add)
        else:
            data["dialogues"] = log_will_add
        with open(self.log_file, 'w', encoding='utf-8-sig') as log_file_object:
            json.dump(data, cast("SupportsWrite[str]", log_file_object), ensure_ascii=False, indent=4)

