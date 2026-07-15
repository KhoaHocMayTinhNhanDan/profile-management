from scripts.util_dev.project_manager_app.layer_05_bootstrap.di_container import (
    DIContainer,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import (
    IProjectRepository,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.inbound.project_repository import (
    ProjectRepository,
)
from scripts.util_dev.project_manager_app.layer_04_infrastructure.databases.local.file_system_project_data_source import (
    FileSystemProjectDataSource,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.save_project.save_project_interactor import (
    SaveProjectInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.load_project.load_project_interactor import (
    LoadProjectInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.list_projects.list_projects_interactor import (
    ListProjectsInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.reset_workspace.reset_workspace_interactor import (
    ResetWorkspaceInteractor,
)

from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.save_project import (
    CliSaveProjectController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.load_project import (
    CliLoadProjectController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.list_projects import (
    CliListProjectsController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.reset_workspace import (
    CliResetWorkspaceController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.generate_feature_controller import (
    GenerateFeatureController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.check_imports_controller import (
    CliCheckImportsController,
)

# New imports
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.rename_module.rename_module_interactor import (
    RenameModuleInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.rename_module_controller import (
    CliRenameModuleController,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.move_module.move_module_interactor import (
    MoveModuleInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.move_module_controller import (
    CliMoveModuleController,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.migrate_clean_code.migrate_clean_code_interactor import (
    MigrateCleanCodeInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.migrate_clean_code_controller import (
    CliMigrateCleanCodeController,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.setup_environment.setup_environment_interactor import (
    SetupEnvironmentInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.setup_environment_controller import (
    CliSetupEnvironmentController,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.delete_project.delete_project_interactor import (
    DeleteProjectInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.cli.delete_project import (
    CliDeleteProjectController,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_file_repository import (
    IFileRepository,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.outbound.i_file_data_source import (
    IFileDataSource,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.inbound.file_repository import (
    FileRepository,
)
from scripts.util_dev.project_manager_app.layer_04_infrastructure.databases.local.file_data_source import (
    FileDataSource,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_interactor import (
    GenerateFeatureInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.check_imports.check_imports_interactor import (
    CheckImportsInteractor,
)


class AppContextCLI:
    def __init__(self, project_root: str):
        self.container = DIContainer()
        self.project_root = project_root

        # Data Sources & Repositories
        import os

        project_data_source = FileSystemProjectDataSource(
            os.path.join(project_root, ".projects")
        )
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
        self.delete_interactor = DeleteProjectInteractor(project_repo)
        self.generate_feature_interactor = GenerateFeatureInteractor(file_repo)
        self.check_imports_interactor = CheckImportsInteractor(file_repo)

        self.rename_module_interactor = RenameModuleInteractor()
        self.move_module_interactor = MoveModuleInteractor()
        self.migrate_clean_code_interactor = MigrateCleanCodeInteractor(file_repo)
        self.setup_environment_interactor = SetupEnvironmentInteractor()

        # Controllers
        self.save_controller = CliSaveProjectController(self.save_interactor)
        self.load_controller = CliLoadProjectController(self.load_interactor)
        self.list_controller = CliListProjectsController(self.list_interactor)
        self.reset_controller = CliResetWorkspaceController(self.reset_interactor)
        self.delete_controller = CliDeleteProjectController(self.delete_interactor)
        self.generate_feature_controller = GenerateFeatureController(
            self.generate_feature_interactor
        )
        self.check_imports_controller = CliCheckImportsController(
            self.check_imports_interactor
        )

        self.rename_module_controller = CliRenameModuleController(
            self.rename_module_interactor
        )
        self.move_module_controller = CliMoveModuleController(
            self.move_module_interactor
        )
        self.migrate_clean_code_controller = CliMigrateCleanCodeController(
            self.migrate_clean_code_interactor
        )
        self.setup_environment_controller = CliSetupEnvironmentController(
            self.setup_environment_interactor
        )
