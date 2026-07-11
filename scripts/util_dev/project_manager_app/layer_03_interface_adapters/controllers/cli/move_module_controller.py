from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.move_module.move_module_interactor import (
    MoveModuleInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.move_module.move_module_dto import (
    MoveModuleInput,
    MoveModuleOutput,
)


class CliMoveModuleController:
    def __init__(self, interactor: MoveModuleInteractor):
        self._interactor = interactor

    def execute(self, source_path: str, destination_dir: str) -> MoveModuleOutput:
        input_dto = MoveModuleInput(
            source_path=source_path, destination_dir=destination_dir
        )
        return self._interactor.execute(input_dto)
