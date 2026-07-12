import os
import hashlib
from typing import Callable, Dict, Any
from PyQt6.QtCore import QFileSystemWatcher, QObject, pyqtSlot
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)


class FileWatcherService(QObject):
    """
    Dịch vụ theo dõi file sử dụng QFileSystemWatcher của PyQt6.
    Không tạo thêm luồng phụ (no threading/QThread), loại bỏ hoàn toàn mọi rủi ro
    deadlock, rò rỉ bộ nhớ luồng, và hoàn toàn tích hợp vào Qt Event Loop gốc.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._watcher = QFileSystemWatcher(self)
        self._watcher.directoryChanged.connect(self._on_directory_changed)

        # Cấu hình theo dõi: dir_path -> list of config dicts
        self._watch_configs: Dict[str, list] = {}

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
        base_name = os.path.basename(file_path_abs)

        # Tính toán tên file khóa tạm của Word/LibreOffice
        if len(base_name) > 2:
            word_lock_name = "~$" + base_name[2:]
        else:
            word_lock_name = "~$"
        word_lock_path = os.path.abspath(os.path.join(dir_to_watch, word_lock_name))
        libre_lock_path = os.path.abspath(
            os.path.join(dir_to_watch, ".~lock." + base_name + "#")
        )

        config = {
            "file_path": file_path_abs,
            "word_lock_path": word_lock_path,
            "libre_lock_path": libre_lock_path,
            "on_change": on_change,
            "triggered": False,
        }

        if dir_to_watch not in self._watch_configs:
            self._watch_configs[dir_to_watch] = []
            self._watcher.addPath(dir_to_watch)

        self._watch_configs[dir_to_watch].append(config)
        logger.info(
            f"Started native QFileSystemWatcher for directory: {dir_to_watch} (file: {base_name})"
        )

    def stop_watching(self, file_path: str):
        file_path_abs = os.path.abspath(file_path)
        dir_path = os.path.dirname(file_path_abs)

        if dir_path in self._watch_configs:
            self._watch_configs[dir_path] = [
                c
                for c in self._watch_configs[dir_path]
                if c["file_path"] != file_path_abs
            ]
            if not self._watch_configs[dir_path]:
                self._watch_configs.pop(dir_path)
                self._watcher.removePath(dir_path)
                logger.info(
                    f"Stopped native QFileSystemWatcher for directory: {dir_path}"
                )

    @pyqtSlot(str)
    def _on_directory_changed(self, path: str):
        dir_path = os.path.abspath(path)
        if dir_path not in self._watch_configs:
            return

        # Sử dụng list() để copy danh sách cấu hình, tránh lỗi sửa đổi list khi đang lặp (RuntimeError)
        # do hàm callback on_change có thể gọi stop_watching làm thay đổi size của list.
        for config in list(self._watch_configs[dir_path]):
            if config["triggered"]:
                continue

            # Kiểm tra xem các file khóa tạm thời còn tồn tại không
            has_lock = os.path.exists(config["word_lock_path"]) or os.path.exists(
                config["libre_lock_path"]
            )
            if not has_lock:
                file_path = config["file_path"]
                if os.path.exists(file_path) and self._is_file_writable(file_path):
                    config["triggered"] = True

                    new_hash = self._get_file_hash(file_path)
                    size = os.path.getsize(file_path)
                    logger.info(f"QFileSystemWatcher trigger fired for: {file_path}")
                    # Gọi callback trực tiếp trên main thread
                    config["on_change"](file_path, size, new_hash)
