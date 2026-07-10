from scripts.util_dev.project_manager_app.layer_05_bootstrap.di_container import DIContainer

from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import IProjectRepository
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.inbound.project_repository import ProjectRepository
from scripts.util_dev.project_manager_app.layer_04_infrastructure.databases.local.file_system_project_data_source import FileSystemProjectDataSource

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.save_project.save_project_interactor import SaveProjectInteractor
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.load_project.load_project_interactor import LoadProjectInteractor
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.list_projects.list_projects_interactor import ListProjectsInteractor
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.reset_workspace.reset_workspace_interactor import ResetWorkspaceInteractor

from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.save_project import CliSaveProjectController
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.load_project import CliLoadProjectController
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.list_projects import CliListProjectsController
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.reset_workspace import CliResetWorkspaceController
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.generate_feature_controller import GenerateFeatureController
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.check_imports_controller import CliCheckImportsController

from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_file_repository import IFileRepository
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.outbound.i_file_data_source import IFileDataSource
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.inbound.file_repository import FileRepository
from scripts.util_dev.project_manager_app.layer_04_infrastructure.databases.local.file_data_source import FileDataSource

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_interactor import GenerateFeatureInteractor
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.check_imports.check_imports_interactor import CheckImportsInteractor

class AppContextCLI:
    def __init__(self, project_root: str):
        self.container = DIContainer()
        self.project_root = project_root
        
        # Data Sources & Repositories
        project_data_source = FileSystemProjectDataSource()
        project_repo = ProjectRepository(project_data_source)
        self.container.register(IProjectRepository, project_repo)
        
        file_data_source = FileDataSource()
        file_repo = FileRepository(file_data_source)
        self.container.register(IFileRepository, file_repo)
        
        # Interactors
        self.save_interactor = SaveProjectInteractor(project_repo)
        self.load_interactor = LoadProjectInteractor(project_repo)
        self.list_interactor = ListProjectsInteractor(project_repo)
        self.reset_interactor = ResetWorkspaceInteractor(project_repo, project_root)
        self.generate_feature_interactor = GenerateFeatureInteractor(file_repo)
        self.check_imports_interactor = CheckImportsInteractor(file_repo)
        
        # Controllers
        self.save_controller = CliSaveProjectController(self.save_interactor)
        self.load_controller = CliLoadProjectController(self.load_interactor)
        self.list_controller = CliListProjectsController(self.list_interactor)
        self.reset_controller = CliResetWorkspaceController(self.reset_interactor)
        self.generate_feature_controller = GenerateFeatureController(self.generate_feature_interactor)
        self.check_imports_controller = CliCheckImportsController(self.check_imports_interactor)
