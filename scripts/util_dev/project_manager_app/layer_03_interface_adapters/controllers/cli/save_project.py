from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.save_project.save_project_interactor import SaveProjectInteractor, SaveProjectInput

class CliSaveProjectController:
    def __init__(self, interactor: SaveProjectInteractor):
        self._interactor = interactor
        
    def execute(self, project_name: str, src_path: str, tests_path: str) -> bool:
        return self._interactor.execute(SaveProjectInput(project_name, src_path, tests_path))
