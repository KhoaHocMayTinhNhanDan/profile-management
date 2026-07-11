from abc import ABC, abstractmethod
from typing import List


class IProjectDataSource(ABC):
    @abstractmethod
    def backup_folder(self, folder_path: str, backup_name: str) -> bool:
        pass

    @abstractmethod
    def restore_folder(self, backup_name: str, dest_path: str) -> bool:
        pass

    @abstractmethod
    def get_backup_list(self) -> List[str]:
        pass

    @abstractmethod
    def clear_folder(self, folder_path: str) -> bool:
        pass
