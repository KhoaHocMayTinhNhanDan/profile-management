from abc import ABC, abstractmethod
from typing import List


class IProjectRepository(ABC):
    @abstractmethod
    def save_project(self, project_name: str, src_path: str, tests_path: str) -> bool:
        pass

    @abstractmethod
    def load_project(
        self, project_name: str, dest_src_path: str, dest_tests_path: str
    ) -> bool:
        pass

    @abstractmethod
    def list_projects(self) -> List[str]:
        pass

    @abstractmethod
    def reset_workspace(self, root_dir: str) -> bool:
        pass

    @abstractmethod
    def delete_project(self, project_name: str) -> bool:
        pass
