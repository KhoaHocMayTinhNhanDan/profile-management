import fnmatch
from typing import List
from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_file_repository import (
    IFileRepository,
)


class MockFileRepository(IFileRepository):
    def __init__(self):
        self.files = {}
        self.dirs = set()

    def read_file(self, path: str) -> str:
        p = path.replace("\\", "/")
        if p not in self.files:
            raise FileNotFoundError(f"File not found: {path}")
        return self.files[p]

    def write_file(self, path: str, content: str) -> None:
        p = path.replace("\\", "/")
        self.files[p] = content
        # Add parent directories to self.dirs
        parts = p.split("/")
        for i in range(1, len(parts)):
            parent = "/".join(parts[:i])
            if parent:
                self.dirs.add(parent)

    def file_exists(self, path: str) -> bool:
        p = path.replace("\\", "/")
        return p in self.files

    def delete_file(self, path: str) -> None:
        p = path.replace("\\", "/")
        if p in self.files:
            del self.files[p]

    def make_dir(self, path: str) -> None:
        p = path.replace("\\", "/")
        self.dirs.add(p)

    def dir_exists(self, path: str) -> bool:
        p = path.replace("\\", "/")
        return p in self.dirs or any(d.startswith(p + "/") for d in self.dirs)

    def list_dir_recursive(self, path: str, pattern: str = "*") -> List[str]:
        p = path.replace("\\", "/").rstrip("/")
        prefix = p + "/"
        matched_files = []
        for file_path in self.files:
            if file_path.startswith(prefix):
                filename = file_path.split("/")[-1]
                if fnmatch.fnmatch(filename, pattern):
                    matched_files.append(file_path)
        return matched_files
