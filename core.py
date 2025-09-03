from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMessageBox
from openai import OpenAI
import button
import sys

class CallAlibabaApi(QObject):
    # content_updated_signal = pyqtSignal(str)
    answer_content_updated_signal = pyqtSignal(str)  # 更新回答文本显示框的信号
    reasoning_content_updated_signal = pyqtSignal(str)  # 更新回答思考文本显示框的信号
    log_reasoning_content_updated_signal = pyqtSignal(str)  # 将reasoning写入log的信号
    log_answer_content_updated_signal = pyqtSignal(str)  # 将answer写入log的信号
    start_reason = pyqtSignal()
    stop_reason = pyqtSignal()
    start_answer = pyqtSignal()
    stop_answer = pyqtSignal()
    finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.api_key = None
        self.reason_log_judge = 0
        self.streaming_word = ''
        self.reason_content_default = '-' * 40 + '思考内容' + '-' * 40 + '\n\n'
        self.reasoning_content_output_spread = self.reason_content_default # 传参,思考内容
        self.answer_content_output_spread = ''  # 传参，回答内容
        self.input_text = None  # user输入的内容

    def call_alibaba_api(self, input_text):
        self.input_text = input_text
        self.api_key = button.api_key
        if self.judge_api_key():
            return

        # 初始化OpenAI客户端
        client = OpenAI(
            api_key= self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        reasoning_content = ""  # 定义完整思考过程
        answer_content = ""  # 定义完整回复
        is_answering = False  # 判断是否结束思考过程并开始回复

        # 创建聊天完成请求
        completion = client.chat.completions.create(
            model="deepseek-v3.1",
            # 此处以 deepseek-r1 为例，可按需更换模型名称
            messages=[
                {"role": "user", "content": self.input_text}
            ],
            extra_body={"enable_thinking": True},
            stream=True,
            # 解除以下注释会在最后一个chunk返回Token使用量
            stream_options={
                "include_usage": True
            }
        )
        print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
        self.reasoning_content_output_spread = self.reason_content_default
        self.start_reason.emit()
        for chunk in completion:
            # 如果chunk.choices为空，则打印usage
            if not chunk.choices:
                print("\nUsage:")
                print(chunk.usage)
            else:
                delta = chunk.choices[0].delta
                # 打印思考过程
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    print(delta.reasoning_content, end='', flush=True)
                    reasoning_content += delta.reasoning_content
                    self.streaming_word = delta.reasoning_content
                    self.reasoning_content_output_spread += delta.reasoning_content
                    # 将self.reasoning_content_output_spread内容作为
                    # 信号内容通过信号content_updated_signal传出
                    self.reasoning_content_updated_signal.emit(self.reasoning_content_output_spread)
                    self.reason_log_judge += 1
                else:
                    if self.reason_log_judge > 0:
                        self.log_reasoning_content_updated_signal.emit(self.reasoning_content_output_spread)
                        self.reason_log_judge = 0
                    # 开始回复
                    if delta.content != "" and is_answering is False:
                        print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                        self.stop_reason.emit()
                        self.start_answer.emit()
                        is_answering = True
                    # 打印回复过程
                    print(delta.content, end='', flush=True)
                    answer_content += delta.content
                    self.streaming_word = delta.content
                    self.answer_content_output_spread += delta.content
                    self.answer_content_updated_signal.emit(self.answer_content_output_spread)


        self.stop_answer.emit()
        self.log_answer_content_updated_signal.emit(self.answer_content_output_spread)
        self.finished_signal.emit()  # 发送完成思考和回答的信号

    def judge_api_key(self):
        if not self.api_key or self.api_key == "Your_Api_Key":

            app = QApplication.instance()
            if app is None:
                app = QApplication([])

            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("API Key 未配置")
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)  # 或 NoButton
            msg_box.show()  # 用 show() 而不是 exec()
            return True  # 不合法,返回[确认不合法]True!
        return False  # 合法,返回[没问题]False!
