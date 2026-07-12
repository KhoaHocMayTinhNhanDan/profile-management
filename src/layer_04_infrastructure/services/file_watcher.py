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

    Cơ chế giám sát kép (Dual-Watching):
    - Giám sát thư mục chứa (Directory Watch): Bắt sự kiện xóa/đổi tên tạm thời khi MS Word thực hiện save (safe-save).
    - Giám sát tệp tin trực tiếp (File Watch): Bắt sự kiện ghi đè trực tiếp (in-place write) của các phần mềm khác (Notepad, VS Code...).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._watcher = QFileSystemWatcher(self)
        self._watcher.directoryChanged.connect(self._on_path_changed)
        self._watcher.fileChanged.connect(self._on_path_changed)

        # Cấu hình theo dõi: file_path_abs -> config dict
        self._watch_configs: Dict[str, dict] = {}

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
            "dir_path": dir_to_watch,
            "word_lock_path": word_lock_path,
            "libre_lock_path": libre_lock_path,
            "on_change": on_change,
            "triggered": False,
        }

        # Đăng ký giám sát kép với QFileSystemWatcher
        try:
            self._watcher.addPath(dir_to_watch)
            if os.path.exists(file_path_abs):
                self._watcher.addPath(file_path_abs)
        except Exception as e:
            logger.error(f"Error registering paths to QFileSystemWatcher: {e}")

        self._watch_configs[file_path_abs] = config
        logger.info(
            f"Started dual-watching native QFileSystemWatcher for: {file_path_abs}"
        )

    def stop_watching(self, file_path: str):
        file_path_abs = os.path.abspath(file_path)
        config = self._watch_configs.pop(file_path_abs, None)
        if config:
            dir_path = config["dir_path"]

            # Kiểm tra xem có file nào khác đang cần giám sát thư mục này không
            dir_still_needed = any(
                c["dir_path"] == dir_path for c in self._watch_configs.values()
            )
            if not dir_still_needed:
                try:
                    self._watcher.removePath(dir_path)
                except Exception:
                    pass

            # Kiểm tra xem file này có còn cần giám sát trực tiếp không
            file_still_needed = any(
                c["file_path"] == file_path_abs for c in self._watch_configs.values()
            )
            if not file_still_needed:
                try:
                    self._watcher.removePath(file_path_abs)
                except Exception:
                    pass

            logger.info(
                f"Stopped dual-watching native QFileSystemWatcher for: {file_path_abs}"
            )

    @pyqtSlot(str)
    def _on_path_changed(self, path: str):
        changed_path = os.path.abspath(path)

        # Lọc danh sách các cấu hình cần kiểm tra dựa trên đường dẫn thay đổi
        configs_to_check = []
        for config in list(self._watch_configs.values()):
            if config["triggered"]:
                continue
            if (
                config["file_path"] == changed_path
                or config["dir_path"] == changed_path
            ):
                configs_to_check.append(config)

        for config in configs_to_check:
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
                    logger.info(
                        f"QFileSystemWatcher trigger fired for: {file_path} (via change on: {changed_path})"
                    )
                    # Gọi callback trực tiếp trên main thread
                    config["on_change"](file_path, size, new_hash)
