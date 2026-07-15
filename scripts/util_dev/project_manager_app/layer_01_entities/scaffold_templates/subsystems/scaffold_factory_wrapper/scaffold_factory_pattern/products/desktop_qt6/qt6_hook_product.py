from ..abstract.i_hook_product import AbstractHook


class Qt6Hook(AbstractHook):
    """
    GoF Role: ConcreteProduct
    """

    def get_async_template(self) -> str:
        return '''from PyQt6.QtCore import QObject, pyqtSignal, QThread

class AsyncWorker(QThread):
    """
    Luồng chạy ngầm tổng quát hóa để chạy bất kỳ hàm Python callable nào.
    """
    finished = pyqtSignal(bool, object, str)  # success, result, error_msg

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            res = self.fn(*self.args, **self.kwargs)
            self.finished.emit(True, res, "")
        except Exception as e:
            self.finished.emit(False, None, str(e))

class UseAsync(QObject):
    """
    Custom Hook tổng quát hóa hỗ trợ chạy bất đồng bộ mọi tác vụ IO/CPU nặng trên PyQt6.
    """
    finished = pyqtSignal(bool, object, str)
    loading = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None

    def execute(self, fn, *args, **kwargs) -> bool:
        if self.worker and self.worker.isRunning():
            return False
        self.loading.emit(True)
        self.worker = AsyncWorker(fn, *args, **kwargs)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()
        return True

    def _on_finished(self, success, result, error_msg):
        self.loading.emit(False)
        self.finished.emit(success, result, error_msg)
'''

    def get_feature_template(self, pascal_name: str, snake_name: str) -> str:
        return f'''from PyQt6.QtCore import QObject, pyqtSignal
from src.layer_03_interface_adapters.controllers.desktop_qt6.{snake_name} import {pascal_name}Controller

class Use{pascal_name}(QObject):
    """
    Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng {pascal_name}.
    """
    data_changed = pyqtSignal(dict)
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
'''
