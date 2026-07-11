from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.reset_workspace.reset_workspace_interactor import (
    ResetWorkspaceInteractor,
)


class DesktopResetWorkspaceController:
    def __init__(self, interactor: ResetWorkspaceInteractor):
        self._interactor = interactor

    def execute(self) -> bool:
        return self._interactor.execute()
