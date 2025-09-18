import sys

from PyQt6.QtWidgets import QApplication

from core import CallAlibabaApi
from dialogue_id import DialogueID
from gui import WindowGui
from log_dialogue import LogContext
from settings import Setting

# 解决窗口标题栏图标
import sys, os
from PyQt6.QtGui import QIcon

if getattr(sys, 'frozen', False):
    """
    PyInstaller 打包后，运行 exe 时，Python 解释器会在 sys 模块里注入一个属性：sys.frozen = True
    PyInstaller 会把所有依赖的资源（图片、ico、数据文件…）解压到一个临时目录runtime临时文件夹
    运行 exe 时，Python 解释器就会在那个临时目录里找资源
    这个临时目录路径，PyInstaller 会存放在 sys._MEIPASS里
    """
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath('.') # 返回当前工作目录

icon_path = os.path.join(base_path, 'mar.ico')

setting = Setting()

# 创建一个应用程序对象,所有元素的依赖实例
app = QApplication(sys.argv)

# 实例化dialogue_ID功能对象
dialogue_id1 = DialogueID()

# 实例化阿里云api的调用类
call_alibaba_api_instance = CallAlibabaApi()

# 实例化log记录功能对象
log_object = LogContext(call_alibaba_api_instance, dialogue_id1)


# 实例化整个窗口的GUI
main_window = WindowGui(call_alibaba_api_instance, setting, log_object, dialogue_id1, log_object)
main_window.setWindowIcon(QIcon(icon_path))
main_window.show()


# 启用事件循环,相当于可以智能的结束循环并退出程序的While True
sys.exit(app.exec())
