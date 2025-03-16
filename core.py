from PyQt6.QtCore import pyqtSignal, QObject
from openai import OpenAI


class CallAlibabaApi(QObject):
    # content_updated_signal = pyqtSignal(str)
    answer_content_updated_signal = pyqtSignal(str)  # 更新回答文本显示框的信号
    reasoning_content_updated_signal = pyqtSignal(str)  # 更新回答思考文本显示框的信号
    finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.reasoning_content_output_spread = '思考内容----\n'
        self.answer_content_output_spread = '回答内容----\n'

    def call_alibaba_api(self):
        # 初始化OpenAI客户端
        client = OpenAI(
            # 如果没有配置环境变量，请用百炼API Key替换：api_key="REMOVED_KEYxxx"
            api_key="REMOVED_KEY7baa2a5a6bf04b91aaf5eec210a4f0e6",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        reasoning_content = ""  # 定义完整思考过程
        answer_content = ""  # 定义完整回复
        is_answering = False  # 判断是否结束思考过程并开始回复

        # 创建聊天完成请求
        completion = client.chat.completions.create(
            model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称
            messages=[
                {"role": "user", "content": "你好"}
            ],
            stream=True,
            # 解除以下注释会在最后一个chunk返回Token使用量
            # stream_options={
            #     "include_usage": True
            # }
        )

        print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

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
                    self.reasoning_content_output_spread += delta.reasoning_content
                    # 将self.reasoning_content_output_spread内容作为
                    # 信号内容通过信号content_updated_signal传出
                    self.reasoning_content_updated_signal.emit(self.reasoning_content_output_spread)
                else:
                    # 开始回复
                    if delta.content != "" and is_answering is False:
                        print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                        is_answering = True
                    # 打印回复过程
                    print(delta.content, end='', flush=True)
                    answer_content += delta.content
                    self.answer_content_output_spread += delta.content
                    self.answer_content_updated_signal.emit(self.answer_content_output_spread)
        # print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
        # print(reasoning_content)
        # print("=" * 20 + "完整回复" + "=" * 20 + "\n")
        # print(answer_content)

        self.finished_signal.emit()  # 发送完成思考和回答的信号
