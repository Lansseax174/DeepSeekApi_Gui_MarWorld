import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QGridLayout

from gui import WindowGui
from button import Button
from core import CallAlibabaApi
from worker_thread import WorkerThread

# 创建一个应用程序对象,所有元素的依赖实例
app = QApplication(sys.argv)

# 实例化阿里云api的调用类
call_alibaba_api = CallAlibabaApi()

# 实例化整个窗口的GUI
main_window = WindowGui(call_alibaba_api)
main_window.show()

# # 通过线程异步运行阿里云api的调用类
# thread_caa = WorkerThread(call_alibaba_api)
# thread_caa.start()

# 启用事件循环,相当于可以智能的结束循环并退出程序的While True
sys.exit(app.exec())
