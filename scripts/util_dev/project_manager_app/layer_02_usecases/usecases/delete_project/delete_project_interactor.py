from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import (
    IProjectRepository,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.delete_project.delete_project_dto import (
    DeleteProjectInput,
)


class DeleteProjectInteractor:
    def __init__(self, repo: IProjectRepository):
        self._repo = repo

    def execute(self, input_data: DeleteProjectInput) -> bool:
        return self._repo.delete_project(input_data.project_name)
