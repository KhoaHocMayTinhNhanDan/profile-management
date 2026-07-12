import asyncio
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from src.layer_03_interface_adapters.controllers.desktop.checkin_document import (
    CheckinDocumentController,
)
from src.layer_04_infrastructure.services.file_watcher import FileWatcherService
from .use_async import UseAsync


class UseCheckinDocument(QObject):
    """
    Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng CheckinDocument.
    """

    finished = pyqtSignal(dict)
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)
    document_saved_signal = pyqtSignal(
        str, str, str
    )  # profile_id, document_id, temp_file_path

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self._controller = context.container.resolve(CheckinDocumentController)
        self.watcher = FileWatcherService(self)
        self._async_helper = UseAsync(self)
        self._async_helper.loading.connect(self.loading.emit)
        self._async_helper.finished.connect(self._on_async_finished)

        # Kết nối tín hiệu an toàn đa luồng (QueuedConnection) về Main UI Thread
        getattr(self.document_saved_signal, "connect")(
            self._on_document_saved, Qt.ConnectionType.QueuedConnection
        )

    def start_watching(
        self, profile_id: str, document_id: str, temp_file_path: str, original_path: str
    ):
        self.watcher.start_watching(
            temp_file_path,
            lambda path, size, checksum: getattr(self.document_saved_signal, "emit")(
                profile_id, document_id, temp_file_path
            ),
        )

    def force_unlock(self, profile_id: str, document_id: str):
        req = {
            "profile_id": profile_id,
            "document_id": document_id,
            "user_id": "user_dong",
        }
        self._async_helper.execute(self._run_checkin, req)

    def stop_watching(self, temp_file_path: str):
        self.watcher.stop_watching(temp_file_path)

    def _on_document_saved(
        self, profile_id: str, document_id: str, temp_file_path: str
    ):
        self.watcher.stop_watching(temp_file_path)
        req = {
            "profile_id": profile_id,
            "document_id": document_id,
            "user_id": "user_dong",
        }
        self._async_helper.execute(self._run_checkin, req)

    def _run_checkin(self, req: dict) -> dict:
        return asyncio.run(self._controller.handle_request(req))

    def _on_async_finished(self, success: bool, result: object, error_msg: str):
        if not success:
            self.error.emit(error_msg)
        elif isinstance(result, dict):
            if result.get("status") == "success":
                self.finished.emit(result)
            else:
                self.error.emit(result.get("message", "Lỗi checkin không xác định"))
        else:
            self.error.emit("Kết quả trả về không hợp lệ")

    def cleanup(self):
        if hasattr(self, "_async_helper"):
            self._async_helper.cleanup()
        # QFileSystemWatcher tự động giải phóng khi parent bị hủy,
        # nhưng chúng ta vẫn chủ động gỡ bỏ các thư mục theo dõi
        for dir_path in list(self.watcher._watch_configs.keys()):
            self.watcher._watcher.removePath(dir_path)
        self.watcher._watch_configs.clear()
