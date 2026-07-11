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

from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.save_project import (
    DesktopSaveProjectController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.load_project import (
    DesktopLoadProjectController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.list_projects import (
    DesktopListProjectsController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.reset_workspace import (
    DesktopResetWorkspaceController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.generate_feature_controller import (
    DesktopGenerateFeatureController,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.check_imports_controller import (
    DesktopCheckImportsController,
)

# New Imports for Desktop Controllers
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.rename_module.rename_module_interactor import (
    RenameModuleInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.rename_module_controller import (
    DesktopRenameModuleController,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.move_module.move_module_interactor import (
    MoveModuleInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.move_module_controller import (
    DesktopMoveModuleController,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.migrate_clean_code.migrate_clean_code_interactor import (
    MigrateCleanCodeInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.migrate_clean_code_controller import (
    DesktopMigrateCleanCodeController,
)

from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.setup_environment.setup_environment_interactor import (
    SetupEnvironmentInteractor,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.controllers.desktop.setup_environment_controller import (
    DesktopSetupEnvironmentController,
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

from scripts.util_dev.project_manager_app.layer_04_infrastructure.ui.desktop_qt6.services.theme.theme_manager import (
    ThemeManager,
)
from scripts.util_dev.project_manager_app.layer_04_infrastructure.ui.desktop_qt6.services.i18n.i18n_manager import (
    I18nManager,
)
from scripts.util_dev.project_manager_app.layer_04_infrastructure.ui.desktop_qt6.services.light_dark_mode_manager import (
    LightDarkModeManager,
)


class AppContextDesktop:
    def __init__(self, project_root: str):
        self.container = DIContainer()
        self.project_root = project_root

        # UI Presentation services (Theme and I18n)
        self.mode_manager = LightDarkModeManager("dark")
        self.theme_manager = ThemeManager(self.mode_manager, "classic")
        self.i18n_manager = I18nManager("en")

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

        self.rename_module_interactor = RenameModuleInteractor()
        self.move_module_interactor = MoveModuleInteractor()
        self.migrate_clean_code_interactor = MigrateCleanCodeInteractor(file_repo)
        self.setup_environment_interactor = SetupEnvironmentInteractor()

        # Controllers
        self.save_controller = DesktopSaveProjectController(self.save_interactor)
        self.load_controller = DesktopLoadProjectController(self.load_interactor)
        self.list_controller = DesktopListProjectsController(self.list_interactor)
        self.reset_controller = DesktopResetWorkspaceController(self.reset_interactor)
        self.generate_feature_controller = DesktopGenerateFeatureController(
            self.generate_feature_interactor
        )
        self.check_imports_controller = DesktopCheckImportsController(
            self.check_imports_interactor
        )

        self.rename_module_controller = DesktopRenameModuleController(
            self.rename_module_interactor
        )
        self.move_module_controller = DesktopMoveModuleController(
            self.move_module_interactor
        )
        self.migrate_clean_code_controller = DesktopMigrateCleanCodeController(
            self.migrate_clean_code_interactor
        )
        self.setup_environment_controller = DesktopSetupEnvironmentController(
            self.setup_environment_interactor
        )
