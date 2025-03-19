from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QVBoxLayout, QTextEdit


class QuitButton(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        QToolTip.setFont(QFont('SansSerif', 10))
        # QToolTip.setFont(QFont('华文琥珀', 10))
        # 创建QPushButton
        self.btn = QPushButton('退出MarWorld', self)

        # 字体设置为Arial，大小为14
        self.btn.setFont(QFont('华文琥珀', 15))

        # 绑定按钮作用
        self.btn.clicked.connect(QApplication.quit)

        # 鼠标挪上去显示个提示
        self.btn.setToolTip('退出按钮')

        # 设置按钮固定大小
        self.btn.setFixedSize(135, 60)


class ModelAndApiSelectWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("模型和API选择")
        self.resize(500, 300)  # 设置子窗口的大小
        self.init_ui()

    def init_ui(self):
        # 创建一个中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowModality(Qt.WindowModality.WindowModal)  # 设置为窗口模态
        # 创建一个布局
        layout = QVBoxLayout()

        # 添加一些控件（示例：一个文本编辑框和一个按钮）
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入内容...")
        layout.addWidget(self.text_edit)

        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)  # 点击按钮关闭窗口
        layout.addWidget(self.close_button)

        # 设置布局
        central_widget.setLayout(layout)


class ModelAndApiSelectButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_api_window = None

        QToolTip.setFont(QFont('SansSerif', 10))
        self.btn = QPushButton('Api-Model', self)
        font = QFont('华文琥珀', 13)  # 字体设置为Arial，大小为14
        self.btn.setFont(font)
        self.btn.clicked.connect(self.open_model_api_window)
        self.btn.setFixedSize(100, 50)

    def open_model_api_window(self):
        parent = self.parent()
        self.model_api_window = ModelAndApiSelectWindow(parent)
        self.model_api_window.show()

class InputTextEditButton(QWidget):
    def __init__(self):
        super().__init__()

        QToolTip.setFont(QFont('SansSerif', 10))
        # QToolTip.setFont(QFont('华文琥珀', 10))
        # 创建QPushButton
        self.btn = QPushButton('发送', self)

        # 字体设置为Arial，大小为14
        self.btn.setFont(QFont('华文琥珀', 15))

        # 绑定按钮作用
        self.btn.clicked.connect(self.process_input_text)

        # 鼠标挪上去显示个提示
        self.btn.setToolTip('man!')

        # 设置按钮固定大小
        self.btn.setFixedSize(135, 60)

    def process_input_text(self):
        print('aaaaaaa!')