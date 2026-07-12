import os
import time
import threading
import hashlib
from typing import Callable
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)


class FileWatcherService:
    def __init__(self):
        self._watch_threads = {}
        self._stop_events = {}

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
        """
        Checks if the file is writable (not locked by MS Word/Excel).
        """
        if not os.path.exists(file_path):
            return False
        try:
            # Try to open in append mode to check if it's locked by another process
            with open(file_path, "a+"):
                pass
            return True
        except IOError:
            return False

    def _is_editor_lock_present(self, file_path: str) -> bool:
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)

        # Word owner/lock file: replaces the first 2 characters of the filename with ~$
        if len(base_name) > 2:
            word_lock_name = "~$" + base_name[2:]
        else:
            word_lock_name = "~$"

        word_lock = os.path.join(dir_name, word_lock_name)
        # LibreOffice lock file e.g., .~lock.Document.docx#
        libre_lock = os.path.join(dir_name, ".~lock." + base_name + "#")

        return os.path.exists(word_lock) or os.path.exists(libre_lock)

    def _watch_loop(
        self,
        file_path: str,
        stop_event: threading.Event,
        on_change: Callable[[str, int, str], None],
    ):
        initial_hash = self._get_file_hash(file_path)
        last_modified = os.path.getmtime(file_path) if os.path.exists(file_path) else 0
        seen_lock = False
        waiting_for_lock = True
        lock_absent_count = 0
        import time

        start_time = time.time()

        logger.info(f"Started watching file: {file_path}")

        while not stop_event.is_set():
            time.sleep(0.5)
            if not os.path.exists(file_path):
                continue

            has_lock = self._is_editor_lock_present(file_path)
            if has_lock:
                seen_lock = True
                waiting_for_lock = False

            # Timeout after 10 seconds waiting for lock file to appear (for non-Word editors)
            if waiting_for_lock and (time.time() - start_time > 10.0):
                waiting_for_lock = False
                logger.info(
                    f"Timeout waiting for lock file of: {file_path}. Falling back to modification time checks."
                )

            if waiting_for_lock:
                continue

            trigger = False
            if seen_lock:
                if has_lock:
                    lock_absent_count = 0
                else:
                    lock_absent_count += 1
                    # Debounce: require lock file to be absent for 3 consecutive checks (1.5 seconds)
                    # to prevent premature triggers during Word's startup/temp file re-creation sequence.
                    if lock_absent_count >= 3:
                        trigger = True
            else:
                curr_modified = os.path.getmtime(file_path)
                if curr_modified != last_modified:
                    trigger = True

            if trigger:
                # Wait 0.5s to let the OS release any remaining handles
                time.sleep(0.5)
                if self._is_file_writable(file_path):
                    new_hash = self._get_file_hash(file_path)
                    size = os.path.getsize(file_path)
                    logger.info(f"File watch trigger fired for: {file_path}")
                    on_change(file_path, size, new_hash)
                    break

    def start_watching(
        self, file_path: str, on_change: Callable[[str, int, str], None]
    ):
        self.stop_watching(file_path)

        stop_event = threading.Event()
        self._stop_events[file_path] = stop_event

        thread = threading.Thread(
            target=self._watch_loop,
            args=(file_path, stop_event, on_change),
            daemon=True,
        )
        self._watch_threads[file_path] = thread
        thread.start()

    def stop_watching(self, file_path: str):
        if file_path in self._stop_events:
            self._stop_events[file_path].set()
            thread = self._watch_threads.pop(file_path, None)
            if thread and thread != threading.current_thread():
                thread.join(timeout=1.0)
            self._stop_events.pop(file_path, None)
            logger.info(f"Stopped watching file: {file_path}")
