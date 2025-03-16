import sys
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication
from PyQt6.QtGui import QFont


class Button(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_UI()

    def init_UI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        # QToolTip.setFont(QFont('华文琥珀', 10))

        btn = QPushButton('Quit', self)
        btn.clicked.connect(QApplication.quit)
        btn.setToolTip('This is a <b>QuitButton</b> widget')
        btn.resize(90, 30)
        btn.move(100, 150)
