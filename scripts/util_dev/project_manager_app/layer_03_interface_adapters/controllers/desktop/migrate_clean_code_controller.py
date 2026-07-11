from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.migrate_clean_code.migrate_clean_code_interactor import (
    MigrateCleanCodeInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.migrate_clean_code.migrate_clean_code_dto import (
    MigrateCleanCodeInput,
    MigrateCleanCodeOutput,
)


class DesktopMigrateCleanCodeController:
    def __init__(self, interactor: MigrateCleanCodeInteractor):
        self._interactor = interactor

    def execute(self, project_root: str) -> MigrateCleanCodeOutput:
        input_dto = MigrateCleanCodeInput(project_root=project_root)
        return self._interactor.execute(input_dto)
