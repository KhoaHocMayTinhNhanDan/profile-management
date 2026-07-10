from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import IProjectRepository

class ResetWorkspaceInteractor:
    def __init__(self, repo: IProjectRepository, root_dir: str):
        self._repo = repo
        self._root_dir = root_dir
        
    def execute(self) -> bool:
        return self._repo.reset_workspace(self._root_dir)
