from abc import ABC, abstractmethod
from typing import List


class IFileRepository(ABC):
    @abstractmethod
    def read_file(self, path: str) -> str:
        pass

    @abstractmethod
    def write_file(self, path: str, content: str) -> None:
        pass

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        pass

    @abstractmethod
    def delete_file(self, path: str) -> None:
        pass

    @abstractmethod
    def make_dir(self, path: str) -> None:
        pass

    @abstractmethod
    def dir_exists(self, path: str) -> bool:
        pass

    @abstractmethod
    def list_dir_recursive(self, path: str, pattern: str = "*") -> List[str]:
        pass
