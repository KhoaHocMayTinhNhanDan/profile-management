from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import (
    IProjectRepository,
)
from dataclasses import dataclass


@dataclass
class SaveProjectInput:
    project_name: str
    src_path: str
    tests_path: str


class SaveProjectInteractor:
    def __init__(self, repo: IProjectRepository):
        self._repo = repo

    def execute(self, input_data: SaveProjectInput) -> bool:
        return self._repo.save_project(
            input_data.project_name, input_data.src_path, input_data.tests_path
        )
