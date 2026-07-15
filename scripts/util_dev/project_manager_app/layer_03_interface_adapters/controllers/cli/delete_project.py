from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.delete_project.delete_project_interactor import (
    DeleteProjectInteractor,
    DeleteProjectInput,
)


class CliDeleteProjectController:
    def __init__(self, interactor: DeleteProjectInteractor):
        self._interactor = interactor

    def execute(self, project_name: str) -> bool:
        return self._interactor.execute(DeleteProjectInput(project_name))
