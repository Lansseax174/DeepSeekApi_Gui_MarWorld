from PyQt6.QtCore import QThread

class WorkerThread(QThread):
    def __init__(self, api_instance):
        super().__init__()
        self.api_instance = api_instance

    def run(self):
        self.api_instance.call_alibaba_api()