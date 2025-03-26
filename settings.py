class Setting:

    def __init__(self):
        # 主窗口-宽度,高度
        self.resize = (1500, 900)

        # 窗口打开时的x和y轴的位置，左上角是(0,0)坐标
        self.move = (350, 100)

        # 用户输入文本框-宽度,高度
        self.input_text_edit = (900, 220)

        # 思考内容显示窗口-宽度,高度
        self.text_show_reasoning_content = (400, 900)

        # 对话窗口-宽度,高度
        self.chat_window = (900, 600)

        # 时间显示小窗-宽度,高度
        self.time_show_window = (133, 65)

        # 对话ID显示窗口-宽度,高度,字体,字号
        self.dialogueID_window = (133, 50)
        self.dialogueID_window_Font = ('黑体', 15)

        # 退出按钮的宽度,高度,字体,字号
        self.quit_button = (135, 60)
        self.quit_button_Font = ('华文琥珀', 15)

        # 模型和api选择窗口-[打开按钮]-宽度,高度
        self.model_api_select_button = (100, 50)

        # 模型和api选择窗口-宽度,高度
        self.model_api_select_window = (500, 300)

        # 发送按钮功能-宽度,高度,字体,字号
        self.input_text_edit_button = (135, 60)
        self.input_text_edit_button_Font = ('华文琥珀', 15)

        # [对话窗口]对话框气泡-最大宽度,高度
        self.message_MaximumSize = (800, 15000000)
        # [对话窗口]对话框气泡-最小宽度,高度
        self.message_MinimumSize = (0, 0)

        # 对话ID-起始ID
        self.start_number_dialogue_id = 1000