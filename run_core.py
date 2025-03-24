import sys
from PyQt6.QtWidgets import QApplication


from worker_thread import WorkerThread
from core import CallAlibabaApi
from gui import WindowGui
from log_dialogue import LogContext
from settings import Setting

setting = Setting()

# 创建一个应用程序对象,所有元素的依赖实例
app = QApplication(sys.argv)

# 实例化阿里云api的调用类
call_alibaba_api_instance = CallAlibabaApi()

# 实例化一个log记录功能的对象
log_object = LogContext(call_alibaba_api_instance)

# 实例化整个窗口的GUI
main_window = WindowGui(call_alibaba_api_instance, setting)
main_window.show()

# 启用事件循环,相当于可以智能的结束循环并退出程序的While True
sys.exit(app.exec())
