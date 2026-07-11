from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.list_projects.list_projects_interactor import (
    ListProjectsInteractor,
)


class CliListProjectsController:
    def __init__(self, interactor: ListProjectsInteractor):
        self._interactor = interactor

    def execute(self) -> list:
        return self._interactor.execute()
