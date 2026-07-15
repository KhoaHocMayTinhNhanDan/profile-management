from abc import ABC, abstractmethod
from typing import List


class IFileDataSource(ABC):
    @abstractmethod
    def read(self, path: str) -> str:
        pass

    @abstractmethod
    def write(self, path: str, content: str) -> None:
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        pass

    @abstractmethod
    def delete(self, path: str) -> None:
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
