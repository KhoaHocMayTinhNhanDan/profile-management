from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.setup_environment.setup_environment_interactor import (
    SetupEnvironmentInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.setup_environment.setup_environment_dto import (
    SetupEnvironmentInput,
    SetupEnvironmentOutput,
)


class CliSetupEnvironmentController:
    def __init__(self, interactor: SetupEnvironmentInteractor):
        self._interactor = interactor

    def execute(self, log_callback=None) -> SetupEnvironmentOutput:
        input_dto = SetupEnvironmentInput(log_callback=log_callback)
        return self._interactor.execute(input_dto)
