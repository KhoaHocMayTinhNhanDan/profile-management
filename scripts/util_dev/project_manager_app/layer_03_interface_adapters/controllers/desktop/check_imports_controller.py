from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.check_imports.check_imports_interactor import (
    CheckImportsInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.check_imports.check_imports_dto import (
    CheckImportsInput,
)


class DesktopCheckImportsController:
    def __init__(self, interactor: CheckImportsInteractor):
        self._interactor = interactor

    def execute(self, project_root: str):
        input_dto = CheckImportsInput(project_root_dir=project_root)
        return self._interactor.execute(input_dto)
