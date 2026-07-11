from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import (
    IProjectRepository,
)


class ListProjectsInteractor:
    def __init__(self, repo: IProjectRepository):
        self._repo = repo

    def execute(self) -> list:
        return self._repo.list_projects()
