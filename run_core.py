import sys
from PyQt6.QtWidgets import QApplication


from worker_thread import WorkerThread
from core import CallAlibabaApi
from gui import WindowGui
from log_dialogue import LogContext


# 创建一个应用程序对象,所有元素的依赖实例
app = QApplication(sys.argv)

# 实例化阿里云api的调用类
call_alibaba_api = CallAlibabaApi()

# 实例化一个log记录功能的对象
log_object = LogContext(call_alibaba_api)

# 实例化整个窗口的GUI
main_window = WindowGui(call_alibaba_api)
main_window.show()


# 通过线程异步运行阿里云api的调用类
thread_caa = WorkerThread(call_alibaba_api)
thread_caa.start()

# 启用事件循环,相当于可以智能的结束循环并退出程序的While True
sys.exit(app.exec())
