import json
from typing import cast
import time


class LogContext:
    def __init__(self, api):
        self.add_reason = None
        self.add_api_answer_content = None
        self.add_api_reasoning_content = None
        self.add_user_content = None
        self.api = api
        self.log_file = 'log.json'

        self.reasoning_content = ''
        self.answer_content = self.api.answer_content_output_spread
        self.formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.add_api_reasoning_content = {"time": self.formatted_time,
                                          "role": "assistant",
                                          "content": ""}

        # reasoning_content_updated_signal作为激活信号激活self.update_reasoning_text
        # 并将信号的内容传入到self.update_reasoning_text
        self.api.log_reasoning_content_updated_signal.connect(self.logging_api_reasoning_content)

        # answer_content_updated_signal作为激活信号激活self.update_answer_text
        # 并将信号的内容传入到self.update_answer_text
        self.api.log_answer_content_updated_signal.connect(self.logging_api_answer_content)

        self.api.finished_signal.connect(self.finish_api_logging)

    def logging_user_content(self):
        print('')

    def update_time(self):
        self.formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def logging_api_reasoning_content(self, text):
        self.add_reason = 1
        if self.api.judge_reason is True:
            self.reasoning_content += text

    def logging_api_answer_content(self, text):

        if self.api.judge_reason is False and self.add_reason == 1:
            self.add_api_reasoning_content = {"time": self.formatted_time,
                                              "role": "assistant",
                                              "content": self.reasoning_content}
            self.log_call_alibaba_api(self.add_api_reasoning_content)
            self.add_reason = 0

        self.answer_content += text
        # self.add_api_answer_content = {"time": self.formatted_time,
        #                                "role": "assistant",
        #                                "content": self.answer_content}

    def finish_api_logging(self):
        print('a')

    def log_call_alibaba_api(self, log_will_add):

        self.add_user_content = {"time": self.formatted_time, "role": "user", "content": "你好，今天怎么样？"}
        #
        # dialogue = [
        #     {"time": self.formatted_time, "role": "user", "content": "你好，今天怎么样？"},
        #     {"time": self.formatted_time, "role": "assistant", "content": "我很好，谢谢！你呢？"},
        #     {"time": self.formatted_time, "role": "user", "content": "我也不错！"}
        # ]

        # dialogue = []
        dialogue2 = None

        with open(self.log_file, 'r+', encoding='utf-8-sig') as log_file_object:
            logs = json.load(log_file_object)

            logs.append(log_will_add)

            log_file_object.seek(0)

            json.dump(logs, cast("SupportsWrite[str]", log_file_object),
                      ensure_ascii=False, indent=4)

        with open(self.log_file, 'r', encoding='utf-8-sig') as log_file_object:
            dialogue2 = json.load(log_file_object)

        for i in dialogue2:
            print(i)

# log = LogContext()
# log.log_call_alibaba_api()
