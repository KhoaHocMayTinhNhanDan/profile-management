from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.rename_module.rename_module_interactor import (
    RenameModuleInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.rename_module.rename_module_dto import (
    RenameModuleInput,
    RenameModuleOutput,
)


class CliRenameModuleController:
    def __init__(self, interactor: RenameModuleInteractor):
        self._interactor = interactor

    def execute(self, target_path: str, new_name: str) -> RenameModuleOutput:
        input_dto = RenameModuleInput(target_path=target_path, new_name=new_name)
        return self._interactor.execute(input_dto)
