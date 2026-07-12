import os
import time
import hashlib
import threading
from typing import Callable, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)


class FileWatchHandler(FileSystemEventHandler):
    """
    Handler xử lý sự kiện thay đổi file system của thư mục chứa tài liệu chỉnh sửa.
    """

    def __init__(
        self, file_path: str, on_change: Callable[[str, int, str], None], service
    ):
        super().__init__()
        self.file_path = os.path.abspath(file_path)
        self.dir_name = os.path.dirname(self.file_path)
        self.base_name = os.path.basename(self.file_path)
        self.on_change = on_change
        self.service = service
        self.triggered = False

        # Precompute file khóa tạm của Word/LibreOffice để theo dõi
        if len(self.base_name) > 2:
            self.word_lock_name = "~$" + self.base_name[2:]
        else:
            self.word_lock_name = "~$"
        self.word_lock_path = os.path.abspath(
            os.path.join(self.dir_name, self.word_lock_name)
        )
        self.libre_lock_path = os.path.abspath(
            os.path.join(self.dir_name, ".~lock." + self.base_name + "#")
        )

    def on_any_event(self, event):
        if self.triggered:
            return

        # Check xem các file khóa tạm thời còn tồn tại không
        has_lock = os.path.exists(self.word_lock_path) or os.path.exists(
            self.libre_lock_path
        )
        if not has_lock:
            # File chính tồn tại và có thể ghi được (đã được giải phóng bởi editor)
            if os.path.exists(self.file_path) and self.service._is_file_writable(
                self.file_path
            ):
                self.triggered = True
                # Chờ 0.5s để chắc chắn OS đã hoàn thành đóng file và giải phóng handle
                time.sleep(0.5)
                new_hash = self.service._get_file_hash(self.file_path)
                size = os.path.getsize(self.file_path)
                logger.info(f"File system event trigger fired for: {self.file_path}")
                self.on_change(self.file_path, size, new_hash)


class FileWatcherService:
    """
    Dịch vụ theo dõi file dựa trên sự kiện hệ điều hành (watchdog) thay vì quét định kỳ (polling).
    Giảm thiểu tối đa CPU, loại bỏ lãng phí tài nguyên hệ thống và tối ưu trải nghiệm tương tác.
    """

    def __init__(self):
        self._observers: Dict[str, Any] = {}
        self._handlers: Dict[str, Any] = {}

    def _get_file_hash(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return ""
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""

    def _is_file_writable(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False
        try:
            with open(file_path, "a+"):
                pass
            return True
        except IOError:
            return False

    def start_watching(
        self, file_path: str, on_change: Callable[[str, int, str], None]
    ):
        file_path_abs = os.path.abspath(file_path)
        self.stop_watching(file_path_abs)

        dir_to_watch = os.path.dirname(file_path_abs)

        handler = FileWatchHandler(file_path_abs, on_change, self)
        observer = Observer()
        observer.schedule(handler, path=dir_to_watch, recursive=False)
        observer.start()

        self._observers[file_path_abs] = observer
        self._handlers[file_path_abs] = handler
        logger.info(f"Started event-driven file watch for: {file_path_abs}")

    def stop_watching(self, file_path: str):
        file_path_abs = os.path.abspath(file_path)
        observer = self._observers.pop(file_path_abs, None)
        if observer:
            observer.stop()
            # ⚠️ Tránh RuntimeError: cannot join current thread
            if observer != threading.current_thread():
                observer.join(timeout=1.0)
            logger.info(f"Stopped event-driven file watch for: {file_path_abs}")
        self._handlers.pop(file_path_abs, None)
