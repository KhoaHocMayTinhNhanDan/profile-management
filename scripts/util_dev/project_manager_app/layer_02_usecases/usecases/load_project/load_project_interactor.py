from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import (
    IProjectRepository,
)
from dataclasses import dataclass


@dataclass
class LoadProjectInput:
    project_name: str
    dest_src_path: str
    dest_tests_path: str


class LoadProjectInteractor:
    def __init__(self, repo: IProjectRepository):
        self._repo = repo

    def execute(self, input_data: LoadProjectInput) -> bool:
        return self._repo.load_project(
            input_data.project_name,
            input_data.dest_src_path,
            input_data.dest_tests_path,
        )
