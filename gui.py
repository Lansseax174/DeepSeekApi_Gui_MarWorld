from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QTextEdit, QGridLayout, QMainWindow, QVBoxLayout
from PyQt6.QtCore import QDate, QDateTime, Qt, QTime
import button

from chat_display_screen import ChatWindow
from dialogue_id_list_window import DialogueIdListWinodw


class WindowGui(QMainWindow):
    def __init__(self, api, setting, log_object, dialogue_id1, log_dialogue):
        super().__init__()
        # 定义一些后面要用的变量
        self.log_dialogue = log_dialogue
        self.make_new_chat_button = None
        self.dialogue_list = None
        self.dialogueID_window = None
        self.log_object = log_object
        self.input_text_edit_button = None
        self.input_text_edit = None
        self.setting = setting
        self.time_show = None
        self.text = None
        self.timer = None
        self.show_text = None
        self.button = None
        self.text_show_reasoning_content = None

        self.dialogue_id1 = dialogue_id1
        self.api = api
        self.reasoning_text = self.api.reasoning_content_output_spread
        self.init_window()

        # reasoning_content_updated_signal作为激活信号激活self.update_reasoning_text
        # 并将信号的内容传入到self.update_reasoning_text
        self.api.reasoning_content_updated_signal.connect(self.update_reasoning_text)

        # answer_content_updated_signal作为激活信号激活self.update_answer_text
        # 并将信号的内容传入到self.update_answer_text
        self.api.answer_content_updated_signal.connect(self.update_answer_text)

        # 监听思考和回答完成信号
        self.api.finished_signal.connect(self.output_token_ends)

    def init_window(self):
        self.resize(*self.setting.resize)  # 主窗口宽度和高度
        self.move(*self.setting.move)  # 窗口打开时的位置，左上角是(0,0)
        # self.setFixedSize(300, 300)

        self.setWindowTitle("MarWorld")

        # 创建显示所有对话列表的窗口
        self.dialogue_list = DialogueIdListWinodw(self.log_dialogue, self.dialogue_id1)
        self.dialogue_list.update_dialogueID_window.connect(self.update_dialogueID_window)
        # 退出按钮实例化
        quit_button = button.QuitButton(self)

        # 切换模型和api的窗口的打开按钮的实例化
        model_api_button = button.ModelAndApiSelectButton(self)

        # 初始化状态栏内容
        self.statusBar().showMessage('Ready.')

        # 创建一个显示模型的回答内容的显示框
        chat_window = ChatWindow(self.api, self.setting, self.dialogue_id1, self.dialogue_list)
        chat_window.setFixedSize(*self.setting.chat_window)

        # 创建一个显示模型的思考内容的显示框
        self.make_text_show_reasoning_content()

        # 创建用户输入内容的文本框
        self.make_input_text_edit()

        # 创建显示本次对话的ID的显示窗口
        self.make_dialogueID_window()

        # 创建一个显示时间的显示框
        self.make_time_show()

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_text)
        # self.timer.start(1000)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # 实例化[发送]按钮, 同时将[input_text_edit]整个传给按钮
        self.input_text_edit_button = button.InputTextEditButton(
            self.input_text_edit, self.api, chat_window, self.log_object)

        # 实例化[新聊天]按钮
        self.make_new_chat_button = button.MakeNewChatButton()

        # 最右侧按钮列表垂直布局
        button_container = QWidget()
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.time_show)
        button_layout.addWidget(self.dialogueID_window)
        button_layout.addWidget(quit_button)
        button_layout.addWidget(model_api_button)
        button_container.setLayout(button_layout)

        # 设置垂直布局👆👆👆按钮间距为 0，确保它们上下挨着
        button_layout.setSpacing(0)

        # 使用吊炸天的网格布局来管理元素大小和位置
        layout = QGridLayout()  # ...(添加对象,Y轴,X轴)
        layout.addWidget(self.dialogue_list, 0, 0, 2, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(chat_window, 0, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.text_show_reasoning_content, 0, 2, 2, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(button_container, 0, 3, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.input_text_edit, 1, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.input_text_edit_button, 1, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.make_new_chat_button, 1, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        # 防止AlignmentFlag.AlignLeft导致quit_button的大小被挤成0,0直接vanish
        quit_button.setMinimumSize(135, 60)
        self.dialogue_list.setFixedSize(200, 830)
        self.input_text_edit_button.setMinimumSize(135, 60)
        self.make_new_chat_button.setMinimumSize(135, 60)
        model_api_button.setMinimumSize(100, 50)

        # 使用QWidet来设置布局
        central_widget = QWidget(self)
        # 将网格布局设置为central_widget的布局管理器
        central_widget.setLayout(layout)
        # 设置中心布局为central_widget
        self.setCentralWidget(central_widget)

    def update_reasoning_text(self, text):
        self.reasoning_text = text
        self.text_show_reasoning_content.setText(self.reasoning_text)
        self.statusBar().showMessage('正在输出思考内容...')

    def update_answer_text(self, text):
        self.statusBar().showMessage('正在输出回答内容...')

    def output_token_ends(self):
        self.statusBar().showMessage("Ready.")

    def make_text_show_reasoning_content(self):
        # 创建一个显示模型的思考内容的显示窗口
        self.text_show_reasoning_content = QTextEdit()
        self.text_show_reasoning_content.setText(self.reasoning_text)
        self.text_show_reasoning_content.setFont(QFont(""))
        self.text_show_reasoning_content.setReadOnly(True)  # 只读，不可输入内容
        self.text_show_reasoning_content.setFixedSize(*self.setting.text_show_reasoning_content)

    def make_dialogueID_window(self):
        # 创建显示本次对话的ID的显示窗口
        self.dialogueID_window = QTextEdit()
        temp_text = '当前对话ID:' + '\n' + str(self.dialogue_id1.dialogue_id)
        self.dialogueID_window.setText(temp_text)
        self.dialogueID_window.setReadOnly(True)
        self.dialogueID_window.setFont(QFont(*self.setting.dialogueID_window_Font))
        self.dialogueID_window.setFixedSize(*self.setting.dialogueID_window)

    def update_dialogueID_window(self,text):
        temp_text = '当前对话ID:' + '\n' + str(text)
        self.dialogueID_window.setText(temp_text)

    def make_input_text_edit(self):
        # 创建用户输入内容的文本框
        self.input_text_edit = QTextEdit()
        self.input_text_edit.installEventFilter(self)
        self.input_text_edit.setPlaceholderText("在这里输入内容...")
        self.input_text_edit.setFont(QFont("微软雅黑", 15))
        self.input_text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.input_text_edit.setFixedSize(*self.setting.input_text_edit)

    def make_time_show(self):
        date = QDate.currentDate()
        date = date.toString(Qt.DateFormat.ISODate)

        now_time = QTime.currentTime()
        now_time = now_time.toString(Qt.DateFormat.RFC2822Date)

        self.show_text = date + '\n' + now_time

        self.time_show = QTextEdit()
        self.time_show.setReadOnly(True)
        self.time_show.setFixedSize(*self.setting.time_show_window)

        font = QFont("微软雅黑", 15)  # 设置字体为 Arial，大小为 12
        font.setBold(True)
        self.time_show.setFont(font)

        self.time_show.setText(self.show_text)

    def update_time(self):
        date = QDate.currentDate()
        date = date.toString(Qt.DateFormat.ISODate)

        now_time = QTime.currentTime()
        now_time = now_time.toString(Qt.DateFormat.RFC2822Date)

        self.show_text = date + '\n' + now_time

        font = QFont("微软雅黑", 15)  # 设置字体为 Arial，大小为 12
        font.setBold(True)
        self.time_show.setFont(font)

        self.time_show.setText(self.show_text)

    def eventFilter(self, obj, event):
        # 检测文本框是否有内容和是否有按键判定
        if obj == self.input_text_edit and event.type() == event.Type.KeyPress:
            # 判定按键
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                # Shift+Enter 换行,只按下Enter则发送文本
                if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                    self.input_text_edit.insertPlainText("\n")
                    return True
                else:
                    self.input_text_edit_button.process_input_text()
                    return True
        return super().eventFilter(obj, event)
