class Setting:

    def __init__(self):

        self.resize = (1500, 900)  # 主窗口宽度,高度
        self.move = (350, 150)  # 窗口打开时的x和y轴的位置，左上角是(0,0)坐标
        self.input_text_edit = (1000, 190)  # 用户输入文本框的宽度,高度
        self.text_show_reasoning_content = (300, 700)  # 思考内容显示窗口的宽度,高度
        self.chat_window = (1000, 600)  # 对话框的宽度,高度


        # 让气泡内的文本可以被选中操作
        self.message_MaximumSize = (800, 15000000)  # 对话框气泡的最大宽度和高度
        self.message_MinimumSize = (0, 0)   # 对话框气泡的最小宽度和高度

