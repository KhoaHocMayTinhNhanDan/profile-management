from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.load_project.load_project_interactor import LoadProjectInteractor, LoadProjectInput

class CliLoadProjectController:
    def __init__(self, interactor: LoadProjectInteractor):
        self._interactor = interactor
        
    def execute(self, project_name: str, dest_src: str, dest_tests: str) -> bool:
        return self._interactor.execute(LoadProjectInput(project_name, dest_src, dest_tests))
