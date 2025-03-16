import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QGridLayout

from gui import WindowGui
from button import Button
from core import CallAlibabaApi
from worker_thread import WorkerThread


app = QApplication(sys.argv)

call_alibaba_api = CallAlibabaApi()

main_window = WindowGui(call_alibaba_api)
main_window.show()

# thread_caa = WorkerThread(call_alibaba_api)
# thread_caa.start()



sys.exit(app.exec())
