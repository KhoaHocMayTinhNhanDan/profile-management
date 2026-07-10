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

    def _watch_loop(self, file_path: str, stop_event: threading.Event, on_change: Callable[[str, int, str], None]):
        initial_hash = self._get_file_hash(file_path)
        last_modified = os.path.getmtime(file_path) if os.path.exists(file_path) else 0
        
        logger.info(f"Started watching file: {file_path}")
        
        while not stop_event.is_set():
            time.sleep(1.0)
            if not os.path.exists(file_path):
                continue
                
            curr_modified = os.path.getmtime(file_path)
            if curr_modified != last_modified:
                # File modified, check if it's unlocked/writable
                if self._is_file_writable(file_path):
                    new_hash = self._get_file_hash(file_path)
                    if new_hash != initial_hash:
                        logger.info(f"File modified and unlocked: {file_path}")
                        size = os.path.getsize(file_path)
                        # Fire callback
                        on_change(file_path, size, new_hash)
                        # Update state
                        initial_hash = new_hash
                        last_modified = curr_modified

    def start_watching(self, file_path: str, on_change: Callable[[str, int, str], None]):
        self.stop_watching(file_path)
        
        stop_event = threading.Event()
        self._stop_events[file_path] = stop_event
        
        thread = threading.Thread(
            target=self._watch_loop, 
            args=(file_path, stop_event, on_change), 
            daemon=True
        )
        self._watch_threads[file_path] = thread
        thread.start()

    def stop_watching(self, file_path: str):
        if file_path in self._stop_events:
            self._stop_events[file_path].set()
            thread = self._watch_threads.pop(file_path, None)
            if thread:
                thread.join(timeout=1.0)
            self._stop_events.pop(file_path, None)
            logger.info(f"Stopped watching file: {file_path}")
