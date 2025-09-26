from PyQt6.QtCore import QThread, pyqtSignal


class WorkerThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, api_instance, input_text):
        super().__init__()
        self.api_instance = api_instance
        self.input_text = input_text
    def run(self):
        self.api_instance.call_alibaba_api(self.input_text)
        self.finished_signal.emit()