import os
import re
import json
from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_file_repository import (
    IFileRepository,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_dto import (
    GenerateFeatureInput,
    GenerateFeatureOutput,
)
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates import (
    CleanArchitectureTemplate as tp,
)
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates import (
    CleanArchitecturePaths as paths,
)


def to_snake_case(name: str) -> str:
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def to_pascal_case(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    return "".join(word.title() for word in name.split("_") if word)


class GenerateFeatureInteractor:
    def __init__(self, file_repo: IFileRepository):
        self._file_repo = file_repo
        self._color_palette = "Catppuccin_Mocha"
        self._root = ""

    def execute(self, input_data: GenerateFeatureInput) -> GenerateFeatureOutput:
        self._color_palette = input_data.color_palette
        self._root = input_data.project_root_dir

        # Initialize ThemeContext for GoF Theme Strategy Pattern
        from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.theme_strategy_pattern.context.theme_context import (
            ThemeContext,
        )

        self._theme_context = ThemeContext(
            self._root, input_data.theme, self._color_palette
        )

        snake = to_snake_case(input_data.feature_name)
        pascal = to_pascal_case(snake)
        root = input_data.project_root_dir
        group = (
            to_snake_case(input_data.group_name)
            if input_data.group_name.strip()
            else ""
        )

        try:
            self._ensure_common_infra(root)

            # Nếu chỉ là khởi tạo dự án rỗng
            if not input_data.feature_name.strip():
                # 1. Khởi tạo cấu trúc nền tảng trước
                self._generate_ui_pages(
                    root,
                    "",
                    "",
                    input_data.platforms,
                    input_data.project_name,
                    color_palette=input_data.color_palette,
                )
                self._update_app_contexts(
                    root, "", "", input_data.platforms, input_data.db_techs, group
                )

                # 2. Tự động sinh feature ColorPaletteDemo làm demo giao diện mẫu mặc định
                demo_input = GenerateFeatureInput(
                    feature_name="ColorPaletteDemo",
                    platforms=input_data.platforms,
                    db_techs=input_data.db_techs,
                    project_root_dir=input_data.project_root_dir,
                    project_name=input_data.project_name,
                    color_palette=input_data.color_palette,
                    theme=input_data.theme,
                )
                self.execute(demo_input)

                return GenerateFeatureOutput(
                    "ok",
                    "Project structured and ColorPaletteDemo showcase feature scaffolded successfully.",
                )

            self._generate_layer_02(root, pascal, snake, group)
            self._generate_layer_03(root, pascal, snake, input_data.platforms, group)
            self._generate_layer_04_repositories(
                root, pascal, snake, input_data.db_techs
            )
            self._generate_ui_pages(
                root,
                pascal,
                snake,
                input_data.platforms,
                input_data.project_name,
                color_palette=input_data.color_palette,
            )
            if (
                any("web" in p for p in input_data.platforms)
                or not input_data.platforms
            ):
                self._generate_fastapi_router(root, pascal, snake, group)
            self._generate_tests(root, pascal, snake, group)
            self._update_app_contexts(
                root, pascal, snake, input_data.platforms, input_data.db_techs, group
            )
            return GenerateFeatureOutput(
                "ok", f"Feature '{pascal}' generated successfully."
            )
        except Exception as e:
            return GenerateFeatureOutput("error", str(e))

    def _ensure_common_infra(self, root):
        # Ensure root packages have __init__.py for proper Python import and refactoring path resolution
        for pkg_dir in [
            paths.SRC,
            os.path.join(paths.SRC, paths.LAYER_01),
            os.path.join(paths.SRC, paths.LAYER_02),
            os.path.join(paths.SRC, paths.LAYER_02, paths.USECASES),
            os.path.join(paths.SRC, paths.LAYER_03),
            os.path.join(paths.SRC, paths.LAYER_05),
            paths.TESTS,
            os.path.join(paths.TESTS, "unit"),
            os.path.join(paths.TESTS, "unit", paths.LAYER_02),
        ]:
            full_dir = os.path.join(root, pkg_dir)
            os.makedirs(full_dir, exist_ok=True)
            init_file = os.path.join(full_dir, "__init__.py")
            if not self._file_repo.file_exists(init_file):
                self._write(init_file, "")

        # Automate layer_04_infrastructure standard directories scaffolding (Self-Documenting Structure)
        infra_subdirs = {
            paths.DATABASES: "# Clean Architecture Layer 4: Databases (SQLite, Postgres, MongoDB, etc.)\n",
            paths.DEVICES: "# Clean Architecture Layer 4: Devices & Hardware Drivers\n",
            paths.EXTERNAL_SERVICES: "# Clean Architecture Layer 4: External Services (Email, SMS, Payment Gateways etc.)\n",
            paths.UI: "# Clean Architecture Layer 4: User Interfaces (Desktop, CLI, Web, etc.)\n",
            paths.WEB_DRIVERS: "# Clean Architecture Layer 4: Web Servers & API Client Drivers\n",
        }
        for subdir, desc in infra_subdirs.items():
            dir_path = os.path.join(root, paths.SRC, paths.LAYER_04, subdir)
            os.makedirs(dir_path, exist_ok=True)
            init_file_path = os.path.join(dir_path, "__init__.py")
            if not self._file_repo.file_exists(init_file_path):
                self._write(init_file_path, desc)
            gitkeep_path = os.path.join(dir_path, ".gitkeep")
            if not self._file_repo.file_exists(gitkeep_path):
                self._write(
                    gitkeep_path,
                    "# Gitkeep to preserve self-documenting directory structure\n",
                )

        logger_path = os.path.join(root, paths.SRC, "shared", "logger", "app_logger.py")
        if not self._file_repo.file_exists(logger_path):
            os.makedirs(os.path.dirname(logger_path), exist_ok=True)
            self._write(os.path.join(root, paths.SRC, "shared", "__init__.py"), "")
            self._write(
                os.path.join(root, paths.SRC, "shared", "logger", "__init__.py"), ""
            )
            self._write(logger_path, tp.get_app_logger_template())

        config_path = os.path.join(root, paths.SRC, "config.py")
        if not self._file_repo.file_exists(config_path):
            self._write(config_path, tp.get_config_template())

        # Tự động sinh Dockerfile nếu chưa tồn tại
        dockerfile_path = os.path.join(root, "Dockerfile")
        if not self._file_repo.file_exists(dockerfile_path):
            self._write(dockerfile_path, tp.get_dockerfile_template())

        # Tự động sinh .dockerignore nếu chưa tồn tại
        dockerignore_path = os.path.join(root, ".dockerignore")
        if not self._file_repo.file_exists(dockerignore_path):
            self._write(dockerignore_path, tp.get_dockerignore_template())

        # Tự động sinh GitHub Actions CI/CD nếu chưa tồn tại
        github_workflow_dir = os.path.join(root, ".github", "workflows")
        os.makedirs(github_workflow_dir, exist_ok=True)
        ci_path = os.path.join(github_workflow_dir, "ci.yml")
        if not self._file_repo.file_exists(ci_path):
            self._write(ci_path, tp.get_github_actions_ci_template())

        # Tự động tạo linter kiểm soát Magic Value ngoài token cho dự án mới
        ui_test_dir = os.path.join(root, "tests", "unit", "ui")
        os.makedirs(ui_test_dir, exist_ok=True)
        self._write(os.path.join(ui_test_dir, "__init__.py"), "")

        linter_impl = os.path.join(ui_test_dir, "design_token_linter.py")
        if not self._file_repo.file_exists(linter_impl):
            self._write(linter_impl, tp.get_design_token_linter_template())

        linter_test = os.path.join(ui_test_dir, "test_theme_tokens_linter.py")
        if not self._file_repo.file_exists(linter_test):
            self._write(linter_test, tp.get_test_theme_tokens_linter_template())

    def _write(self, path: str, content: str):
        if not self._file_repo.file_exists(path):
            if hasattr(self, "_theme_context") and self._theme_context:
                content = self._theme_context.compile(path, content)
            self._file_repo.write_file(path, content.strip() + "\n")
            print(f"Created: {path}")

    def _generate_layer_02(self, root, pascal, snake, group=""):
        if group:
            usecase_dir = os.path.join(
                root, paths.SRC, paths.LAYER_02, paths.USECASES, group, snake
            )
            os.makedirs(os.path.dirname(usecase_dir), exist_ok=True)
            group_init = os.path.join(
                root, paths.SRC, paths.LAYER_02, paths.USECASES, group, "__init__.py"
            )
            if not self._file_repo.file_exists(group_init):
                self._write(group_init, "")
        else:
            usecase_dir = os.path.join(
                root, paths.SRC, paths.LAYER_02, paths.USECASES, snake
            )
        self._write(
            os.path.join(usecase_dir, f"{snake}_interactor.py"),
            tp.get_usecase_interactor_template(pascal, snake),
        )
        self._write(
            os.path.join(usecase_dir, f"{snake}_dto.py"),
            tp.get_usecase_dto_template(pascal),
        )
        self._write(os.path.join(usecase_dir, "__init__.py"), "")

        gw_interface_dir = os.path.join(
            root, paths.SRC, paths.LAYER_02, paths.GATEWAYS_INTERFACE
        )
        self._write(
            os.path.join(gw_interface_dir, f"i_{snake}_repository.py"),
            tp.get_usecase_repository_interface_template(pascal),
        )

    def _generate_layer_03(self, root, pascal, snake, platforms, group=""):
        for plat in platforms:
            c_dir = os.path.join(
                root, paths.SRC, paths.LAYER_03, paths.CONTROLLERS, plat
            )
            self._write(
                os.path.join(c_dir, f"{snake}.py"),
                tp.get_controller_template(pascal, snake, plat, group),
            )

            p_dir = os.path.join(
                root, paths.SRC, paths.LAYER_03, paths.PRESENTERS, plat
            )
            self._write(
                os.path.join(p_dir, f"{snake}.py"),
                tp.get_presenter_template(pascal, snake, group),
            )

        gw_dir = os.path.join(root, paths.SRC, paths.LAYER_03, paths.GATEWAYS)
        self._write(
            os.path.join(gw_dir, paths.GATEWAYS_OUTBOUND, f"i_{snake}_data_source.py"),
            tp.get_outbound_data_source_interface_template(pascal),
        )
        self._write(
            os.path.join(gw_dir, paths.GATEWAYS_INBOUND, f"{snake}_repository.py"),
            tp.get_repository_template(pascal, snake),
        )

    def _generate_layer_04_repositories(self, root, pascal, snake, db_techs):
        for db in db_techs:
            db_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.DATABASES, db)
            self._write(
                os.path.join(db_dir, f"{snake}_data_source.py"),
                tp.get_data_source_impl_template(pascal, snake, db),
            )

    def _generate_ui_pages(
        self,
        root,
        pascal,
        snake,
        platforms,
        project_name: str = "",
        color_palette="Catppuccin_Mocha",
    ):
        if any("desktop_qt6" in p for p in platforms):
            qt6_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "desktop_qt6"
            )
            main_win_path = os.path.join(qt6_dir, "main_window.py")

            # Chỉ sinh bộ khung UI lần đầu tiên (nếu main_window.py chưa tồn tại)
            if not self._file_repo.file_exists(main_win_path):
                # Sinh bộ dịch vụ theme/i18n cục bộ cho Desktop PyQt6
                self._ensure_presentation_services(
                    root, qt6_dir, color_palette=color_palette
                )

                # Create Atomic Design directories & Hooks directory
                for sub in [
                    "level_01_atoms",
                    "level_02_molecules",
                    "level_03_organisms",
                    "level_04_templates",
                    "level_05_pages",
                    "hooks",
                ]:
                    d = os.path.join(qt6_dir, sub)
                    os.makedirs(d, exist_ok=True)
                    self._write(os.path.join(d, "__init__.py"), "")

                # Create Assets subdirectories
                for asset_sub in ["images", "fonts", "icons"]:
                    os.makedirs(
                        os.path.join(qt6_dir, "assets", asset_sub), exist_ok=True
                    )
                self._write(
                    os.path.join(qt6_dir, "assets", "icons", "check.svg"),
                    '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
                )

                self._write(os.path.join(qt6_dir, "__init__.py"), "")

                # Ensure PyQt6 BasePageTemplate exists (colocated under level_04_templates/page_template/)
                page_tpl_dir = os.path.join(
                    qt6_dir, "level_04_templates", "page_template"
                )
                os.makedirs(page_tpl_dir, exist_ok=True)
                self._write(
                    os.path.join(page_tpl_dir, "__init__.py"),
                    "from .page_template import BasePageTemplate\n",
                )
                self._file_repo.write_file(
                    os.path.join(qt6_dir, "level_04_templates", "__init__.py"),
                    "from .page_template import BasePageTemplate\n",
                )
                page_tpl_path = os.path.join(page_tpl_dir, "page_template.py")
                if not self._file_repo.file_exists(page_tpl_path):
                    self._write(page_tpl_path, tp.get_ui_pyqt6_base_page_template())
                    self._write(os.path.join(page_tpl_dir, "page_template.qss"), "")

                # Write base atomic components (Colocated folder format)
                # Buttons
                buttons_dir = os.path.join(qt6_dir, "level_01_atoms", "buttons")
                os.makedirs(buttons_dir, exist_ok=True)
                os.makedirs(os.path.join(buttons_dir, "assets", "icons"), exist_ok=True)
                self._write(
                    os.path.join(buttons_dir, "assets", "icons", ".gitkeep"), ""
                )
                self._write(
                    os.path.join(buttons_dir, "__init__.py"),
                    "from .buttons import PrimaryButton, SecondaryButton, DangerButton\n",
                )
                self._write(
                    os.path.join(buttons_dir, "buttons.py"),
                    tp.get_ui_pyqt6_atom_buttons_template(),
                )
                self._write(
                    os.path.join(buttons_dir, "buttons.qss"),
                    tp.get_ui_pyqt6_atom_buttons_qss_template(),
                )

                # Inputs
                inputs_dir = os.path.join(qt6_dir, "level_01_atoms", "inputs")
                os.makedirs(inputs_dir, exist_ok=True)
                os.makedirs(os.path.join(inputs_dir, "assets", "icons"), exist_ok=True)
                self._write(os.path.join(inputs_dir, "assets", "icons", ".gitkeep"), "")
                self._write(
                    os.path.join(inputs_dir, "__init__.py"),
                    "from .inputs import FormLineEdit, FormComboBox\n",
                )
                self._write(
                    os.path.join(inputs_dir, "inputs.py"),
                    tp.get_ui_pyqt6_atom_inputs_template(),
                )
                self._write(
                    os.path.join(inputs_dir, "inputs.qss"),
                    tp.get_ui_pyqt6_atom_inputs_qss_template(),
                )

                # Labels
                labels_dir = os.path.join(qt6_dir, "level_01_atoms", "labels")
                os.makedirs(labels_dir, exist_ok=True)
                os.makedirs(os.path.join(labels_dir, "assets", "icons"), exist_ok=True)
                self._write(os.path.join(labels_dir, "assets", "icons", ".gitkeep"), "")
                self._write(
                    os.path.join(labels_dir, "__init__.py"),
                    "from .labels import HeaderLabel, BodyLabel\n",
                )
                self._write(
                    os.path.join(labels_dir, "labels.py"),
                    tp.get_ui_pyqt6_atom_labels_template(),
                )
                self._write(
                    os.path.join(labels_dir, "labels.qss"),
                    tp.get_ui_pyqt6_atom_labels_qss_template(),
                )

                # Level 1 Atoms root facade
                self._file_repo.write_file(
                    os.path.join(qt6_dir, "level_01_atoms", "__init__.py"),
                    "from .buttons import PrimaryButton, SecondaryButton, DangerButton\n"
                    "from .inputs import FormLineEdit, FormComboBox\n"
                    "from .labels import HeaderLabel, BodyLabel\n",
                )

                # Write UI inspector (colocated under level_02_molecules/ui_inspector/)
                inspector_dir = os.path.join(
                    qt6_dir, "level_02_molecules", "ui_inspector"
                )
                os.makedirs(inspector_dir, exist_ok=True)
                self._write(
                    os.path.join(inspector_dir, "__init__.py"),
                    "from .ui_inspector import UIInspector\n",
                )
                self._file_repo.write_file(
                    os.path.join(qt6_dir, "level_02_molecules", "__init__.py"),
                    "from .ui_inspector import UIInspector\n",
                )
                self._write(
                    os.path.join(inspector_dir, "ui_inspector.py"),
                    tp.get_ui_pyqt6_ui_inspector_template(),
                )
                self._write(os.path.join(inspector_dir, "ui_inspector.qss"), "")

                # Write base hooks
                self._write(
                    os.path.join(qt6_dir, "hooks", "use_async.py"),
                    tp.get_ui_pyqt6_use_async_template(),
                )

                # Write welcome_page.py
                self._write(
                    os.path.join(qt6_dir, "level_05_pages", "welcome_page.py"),
                    tp.get_ui_pyqt6_page_template("Welcome", "welcome"),
                )

                # Write main_window.py
                self._write(
                    main_win_path, tp.get_ui_pyqt6_main_window_template(project_name)
                )

            # Sinh trang con & Hook cụ thể cho từng feature (nếu có snake name)
            if snake:
                self._write(
                    os.path.join(qt6_dir, "level_05_pages", f"{snake}_page.py"),
                    tp.get_ui_pyqt6_page_template(pascal, snake),
                )
                self._write(
                    os.path.join(qt6_dir, "hooks", f"use_{snake}.py"),
                    tp.get_ui_pyqt6_feature_hook_template(pascal, snake),
                )

        if any("desktop_tauri" in p for p in platforms):
            tauri_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "desktop_tauri"
            )
            src_tauri_dir = os.path.join(tauri_dir, "src-tauri")
            conf_path = os.path.join(src_tauri_dir, "tauri.conf.json")
            if not self._file_repo.file_exists(conf_path):
                from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.factory.desktop_tauri_factory import (
                    DesktopTauriFactory,
                )

                fact = DesktopTauriFactory()

                # Create directory structure
                os.makedirs(os.path.join(src_tauri_dir, "src"), exist_ok=True)
                os.makedirs(os.path.join(src_tauri_dir, "icons"), exist_ok=True)

                # Write placeholder icons to pass builder validation
                for icon_name in [
                    "32x32.png",
                    "128x128.png",
                    "128x128@2x.png",
                    "icon.icns",
                    "icon.ico",
                ]:
                    self._write(os.path.join(src_tauri_dir, "icons", icon_name), "")

                # Write Tauri Rust wrapper files
                self._write(
                    os.path.join(src_tauri_dir, "Cargo.toml"),
                    fact.create_cargo(project_name),
                )
                self._write(conf_path, fact.create_tauri_conf(project_name))
                self._write(
                    os.path.join(src_tauri_dir, "src", "main.rs"), fact.create_main_rs()
                )

        if any("desktop_qt5" in p for p in platforms):
            qt_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "desktop_qt5", "pages"
            )
            welcome_path = os.path.join(qt_dir, "welcome_page.py")
            if not self._file_repo.file_exists(welcome_path):
                os.makedirs(qt_dir, exist_ok=True)
                self._write(os.path.join(qt_dir, "__init__.py"), "")
                self._write(
                    welcome_path, tp.get_ui_pyqt5_template("Welcome", "welcome")
                )

        if any("desktop_tkinter" in p for p in platforms):
            tk_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "desktop_tkinter", "pages"
            )
            welcome_path = os.path.join(tk_dir, "welcome_page.py")
            if not self._file_repo.file_exists(welcome_path):
                os.makedirs(tk_dir, exist_ok=True)
                self._write(os.path.join(tk_dir, "__init__.py"), "")
                self._write(
                    welcome_path, tp.get_ui_tkinter_template("Welcome", "welcome")
                )

        if any("mobile_kivy" in p for p in platforms):
            kv_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "mobile_kivy"
            )
            welcome_path = os.path.join(kv_dir, "level_05_pages", "welcome_page.py")
            if not self._file_repo.file_exists(welcome_path):
                # Sinh bộ dịch vụ theme/i18n cục bộ cho Mobile Kivy
                self._ensure_presentation_services(
                    root, kv_dir, color_palette=color_palette
                )

                for sub in [
                    "level_01_atoms",
                    "level_02_molecules",
                    "level_03_organisms",
                    "level_04_templates",
                    "level_05_pages",
                    "hooks",
                ]:
                    d = os.path.join(kv_dir, sub)
                    os.makedirs(d, exist_ok=True)
                    self._write(os.path.join(d, "__init__.py"), "")

                # Create Assets subdirectories
                for asset_sub in ["images", "fonts", "icons"]:
                    os.makedirs(
                        os.path.join(kv_dir, "assets", asset_sub), exist_ok=True
                    )

                self._write(os.path.join(kv_dir, "__init__.py"), "")

                # Write base Kivy atomic components
                self._write(
                    os.path.join(kv_dir, "level_01_atoms", "buttons.py"),
                    tp.get_ui_kivy_atom_buttons_template(),
                )
                self._write(
                    os.path.join(kv_dir, "level_01_atoms", "inputs.py"),
                    tp.get_ui_kivy_atom_inputs_template(),
                )
                self._write(
                    os.path.join(kv_dir, "level_01_atoms", "labels.py"),
                    tp.get_ui_kivy_atom_labels_template(),
                )

                # Write base hooks
                self._write(
                    os.path.join(kv_dir, "hooks", "use_async.py"),
                    tp.get_ui_kivy_use_async_template(),
                )

                # Write page
                self._write(welcome_path, tp.get_ui_kivy_template("Welcome", "welcome"))

                # Write UI Inspector for Kivy
                inspector_dir = os.path.join(
                    kv_dir, "level_02_molecules", "ui_inspector"
                )
                os.makedirs(inspector_dir, exist_ok=True)
                self._write(
                    os.path.join(inspector_dir, "__init__.py"),
                    "from .ui_inspector import UIInspector\n",
                )
                self._write(
                    os.path.join(inspector_dir, "ui_inspector.py"),
                    tp.get_ui_kivy_ui_inspector_template(),
                )
                self._write(
                    os.path.join(kv_dir, "level_02_molecules", "__init__.py"),
                    "from .ui_inspector import UIInspector\n",
                )

                # Write Main Window for Kivy
                self._write(
                    os.path.join(kv_dir, "main_window.py"),
                    tp.get_ui_kivy_main_window_template(project_name),
                )

            # Sinh trang con & Hook cụ thể cho từng feature (nếu có snake name)
            if snake:
                self._write(
                    os.path.join(kv_dir, "level_05_pages", f"{snake}_page.py"),
                    tp.get_ui_kivy_template(pascal, snake),
                )
                self._write(
                    os.path.join(kv_dir, "hooks", f"use_{snake}.py"),
                    tp.get_ui_kivy_feature_hook_template(pascal, snake),
                )

        if any("mobile_flutter" in p for p in platforms):
            fl_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "mobile_flutter"
            )
            welcome_path = os.path.join(
                fl_dir, "lib", "level_05_pages", "welcome_page.dart"
            )
            if not self._file_repo.file_exists(welcome_path):
                from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.factory.mobile_flutter_factory import (
                    MobileFlutterFactory,
                )

                fact = MobileFlutterFactory()
                for sub in [
                    "lib/level_01_atoms",
                    "lib/level_02_molecules/ui_inspector",
                    "lib/level_03_organisms",
                    "lib/level_04_templates",
                    "lib/level_05_pages",
                    "lib/hooks",
                    "lib/services",
                ]:
                    os.makedirs(os.path.join(fl_dir, sub), exist_ok=True)

                # Write basic files
                self._write(
                    os.path.join(fl_dir, "pubspec.yaml"),
                    "name: mobile_flutter\ndependencies:\n  flutter:\n    sdk: flutter",
                )
                self._write(
                    os.path.join(fl_dir, "lib", "main.dart"),
                    fact.create_main_window(project_name),
                )
                self._write(
                    os.path.join(fl_dir, "lib", "level_01_atoms", "buttons.dart"),
                    fact.create_buttons(),
                )
                self._write(
                    os.path.join(fl_dir, "lib", "level_01_atoms", "inputs.dart"),
                    fact.create_inputs(),
                )
                self._write(
                    os.path.join(fl_dir, "lib", "level_01_atoms", "labels.dart"),
                    fact.create_labels(),
                )
                self._write(
                    os.path.join(fl_dir, "lib", "hooks", "use_async.dart"),
                    fact.create_async_hook(),
                )
                self._write(
                    os.path.join(
                        fl_dir,
                        "lib",
                        "level_02_molecules",
                        "ui_inspector",
                        "ui_inspector.dart",
                    ),
                    fact.create_ui_inspector(),
                )
                self._write(welcome_path, fact.create_page("Welcome", "welcome"))

            if snake:
                from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.factory.mobile_flutter_factory import (
                    MobileFlutterFactory,
                )

                fact = MobileFlutterFactory()
                self._write(
                    os.path.join(fl_dir, "lib", "level_05_pages", f"{snake}_page.dart"),
                    fact.create_page(pascal, snake),
                )
                self._write(
                    os.path.join(fl_dir, "lib", "hooks", f"use_{snake}.dart"),
                    fact.create_feature_hook(pascal, snake),
                )

        if any("mobile_react_native" in p for p in platforms):
            rn_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "mobile_react_native"
            )
            welcome_path = os.path.join(
                rn_dir, "src", "level_05_pages", "WelcomeScreen.tsx"
            )
            if not self._file_repo.file_exists(welcome_path):
                from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.factory.mobile_react_native_factory import (
                    MobileReactNativeFactory,
                )

                fact = MobileReactNativeFactory()
                for sub in [
                    "src/level_01_atoms",
                    "src/level_02_molecules/ui_inspector",
                    "src/level_03_organisms",
                    "src/level_04_templates",
                    "src/level_05_pages",
                    "src/hooks",
                    "src/services",
                ]:
                    os.makedirs(os.path.join(rn_dir, sub), exist_ok=True)

                # Write basic files
                self._write(
                    os.path.join(rn_dir, "package.json"),
                    '{"name": "mobile_react_native", "version": "1.0.0"}',
                )
                self._write(
                    os.path.join(rn_dir, "tsconfig.json"), '{"compilerOptions": {}}'
                )
                self._write(
                    os.path.join(rn_dir, "App.tsx"),
                    fact.create_main_window(project_name),
                )
                self._write(
                    os.path.join(rn_dir, "src", "level_01_atoms", "buttons.tsx"),
                    fact.create_buttons(),
                )
                self._write(
                    os.path.join(rn_dir, "src", "level_01_atoms", "inputs.tsx"),
                    fact.create_inputs(),
                )
                self._write(
                    os.path.join(rn_dir, "src", "level_01_atoms", "labels.tsx"),
                    fact.create_labels(),
                )
                self._write(
                    os.path.join(rn_dir, "src", "hooks", "use_async.ts"),
                    fact.create_async_hook(),
                )
                self._write(
                    os.path.join(
                        rn_dir,
                        "src",
                        "level_02_molecules",
                        "ui_inspector",
                        "ui_inspector.tsx",
                    ),
                    fact.create_ui_inspector(),
                )
                self._write(welcome_path, fact.create_page("Welcome", "welcome"))

            if snake:
                from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.factory.mobile_react_native_factory import (
                    MobileReactNativeFactory,
                )

                fact = MobileReactNativeFactory()
                self._write(
                    os.path.join(
                        rn_dir, "src", "level_05_pages", f"{pascal}Screen.tsx"
                    ),
                    fact.create_page(pascal, snake),
                )
                self._write(
                    os.path.join(rn_dir, "src", "hooks", f"use_{snake}.ts"),
                    fact.create_feature_hook(pascal, snake),
                )

        if any("mobile_jetpack_compose" in p for p in platforms):
            jc_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "mobile_jetpack_compose"
            )
            welcome_path = os.path.join(
                jc_dir,
                "src",
                "main",
                "java",
                "com",
                "cleanarch",
                "app",
                "level_05_pages",
                "WelcomeScreen.kt",
            )
            if not self._file_repo.file_exists(welcome_path):
                from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.factory.mobile_jetpack_compose_factory import (
                    MobileJetpackComposeFactory,
                )

                fact = MobileJetpackComposeFactory()
                for sub in [
                    "src/main/java/com/cleanarch/app/level_01_atoms",
                    "src/main/java/com/cleanarch/app/level_02_molecules/ui_inspector",
                    "src/main/java/com/cleanarch/app/level_03_organisms",
                    "src/main/java/com/cleanarch/app/level_04_templates",
                    "src/main/java/com/cleanarch/app/level_05_pages",
                    "src/main/java/com/cleanarch/app/hooks",
                    "src/main/java/com/cleanarch/app/services",
                ]:
                    os.makedirs(os.path.join(jc_dir, sub), exist_ok=True)

                # Write basic files
                self._write(
                    os.path.join(jc_dir, "build.gradle.kts"), "// build.gradle.kts"
                )
                self._write(
                    os.path.join(jc_dir, "src", "main", "AndroidManifest.xml"),
                    "<manifest></manifest>",
                )
                self._write(
                    os.path.join(
                        jc_dir,
                        "src",
                        "main",
                        "java",
                        "com",
                        "cleanarch",
                        "app",
                        "MainActivity.kt",
                    ),
                    fact.create_main_window(project_name),
                )
                self._write(
                    os.path.join(
                        jc_dir,
                        "src",
                        "main",
                        "java",
                        "com",
                        "cleanarch",
                        "app",
                        "level_01_atoms",
                        "Buttons.kt",
                    ),
                    fact.create_buttons(),
                )
                self._write(
                    os.path.join(
                        jc_dir,
                        "src",
                        "main",
                        "java",
                        "com",
                        "cleanarch",
                        "app",
                        "level_01_atoms",
                        "Inputs.kt",
                    ),
                    fact.create_inputs(),
                )
                self._write(
                    os.path.join(
                        jc_dir,
                        "src",
                        "main",
                        "java",
                        "com",
                        "cleanarch",
                        "app",
                        "level_01_atoms",
                        "Labels.kt",
                    ),
                    fact.create_labels(),
                )
                self._write(
                    os.path.join(
                        jc_dir,
                        "src",
                        "main",
                        "java",
                        "com",
                        "cleanarch",
                        "app",
                        "hooks",
                        "UseAsync.kt",
                    ),
                    fact.create_async_hook(),
                )
                self._write(
                    os.path.join(
                        jc_dir,
                        "src",
                        "main",
                        "java",
                        "com",
                        "cleanarch",
                        "app",
                        "level_02_molecules",
                        "ui_inspector",
                        "UIInspector.kt",
                    ),
                    fact.create_ui_inspector(),
                )
                self._write(welcome_path, fact.create_page("Welcome", "welcome"))

            if snake:
                from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.factory.mobile_jetpack_compose_factory import (
                    MobileJetpackComposeFactory,
                )

                fact = MobileJetpackComposeFactory()
                self._write(
                    os.path.join(
                        jc_dir,
                        "src",
                        "main",
                        "java",
                        "com",
                        "cleanarch",
                        "app",
                        "level_05_pages",
                        f"{pascal}Screen.kt",
                    ),
                    fact.create_page(pascal, snake),
                )
                self._write(
                    os.path.join(
                        jc_dir,
                        "src",
                        "main",
                        "java",
                        "com",
                        "cleanarch",
                        "app",
                        "hooks",
                        f"Use{pascal}.kt",
                    ),
                    fact.create_feature_hook(pascal, snake),
                )

        if any("cli" in p for p in platforms):
            cli_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "cli", "commands"
            )
            welcome_path = os.path.join(cli_dir, "welcome_cli.py")
            if not self._file_repo.file_exists(welcome_path):
                os.makedirs(cli_dir, exist_ok=True)
                self._write(os.path.join(cli_dir, "__init__.py"), "")
                self._write(welcome_path, tp.get_ui_cli_template("Welcome", "welcome"))

        if any("web" in p for p in platforms) or not platforms:
            web_dir = os.path.join(
                root, paths.SRC, paths.LAYER_04, paths.UI, "web_fastapi", "frontend"
            )
            welcome_path = os.path.join(web_dir, "level_05_pages", "welcome.html")
            if not self._file_repo.file_exists(welcome_path):
                # Sinh bộ dịch vụ theme/i18n cục bộ cho Web Frontend
                self._ensure_presentation_services(
                    root, web_dir, color_palette=color_palette
                )

                for sub in [
                    "level_01_atoms",
                    "level_02_molecules",
                    "level_03_organisms",
                    "level_04_templates",
                    "level_05_pages",
                    "hooks",
                ]:
                    d = os.path.join(web_dir, sub)
                    os.makedirs(d, exist_ok=True)
                    self._write(os.path.join(d, "__init__.py"), "")

                # Create Assets subdirectories
                for asset_sub in ["images", "fonts", "icons"]:
                    os.makedirs(
                        os.path.join(web_dir, "assets", asset_sub), exist_ok=True
                    )

                self._write(os.path.join(web_dir, "__init__.py"), "")

                # Write base Web Component HTML/JS atoms
                self._write(
                    os.path.join(web_dir, "level_01_atoms", "buttons.js"),
                    tp.get_ui_web_atom_buttons_template(),
                )
                self._write(
                    os.path.join(web_dir, "level_01_atoms", "inputs.js"),
                    tp.get_ui_web_atom_inputs_template(),
                )
                self._write(
                    os.path.join(web_dir, "level_01_atoms", "labels.js"),
                    tp.get_ui_web_atom_labels_template(),
                )

                # Write base hooks
                self._write(
                    os.path.join(web_dir, "hooks", "use_async.js"),
                    tp.get_ui_web_use_async_template(),
                )

                # Write page under level_05_pages/
                self._write(
                    welcome_path, tp.get_ui_web_html_template("Welcome", "welcome")
                )

                # Write JS UI Inspector
                inspector_dir = os.path.join(
                    web_dir, "level_02_molecules", "ui_inspector"
                )
                os.makedirs(inspector_dir, exist_ok=True)
                self._write(
                    os.path.join(inspector_dir, "ui_inspector.js"),
                    tp.get_ui_web_ui_inspector_template(),
                )
                self._write(
                    os.path.join(web_dir, "level_02_molecules", "__init__.py"), ""
                )

                # Write FastAPI main and debug router
                fastapi_dir = os.path.join(
                    root, paths.SRC, paths.LAYER_04, paths.UI, "web_fastapi", "fastapi"
                )
                os.makedirs(fastapi_dir, exist_ok=True)
                self._write(
                    os.path.join(fastapi_dir, "main.py"),
                    tp.get_fastapi_main_template(project_name),
                )

                routers_dir = os.path.join(fastapi_dir, "routers")
                os.makedirs(routers_dir, exist_ok=True)
                self._write(os.path.join(routers_dir, "__init__.py"), "")
                self._write(
                    os.path.join(routers_dir, "debug.py"),
                    tp.get_fastapi_debug_router_template(),
                )

            # Sinh trang con & Hook cụ thể cho từng feature (nếu có snake name)
            if snake:
                self._write(
                    os.path.join(web_dir, "level_05_pages", f"{snake}.html"),
                    tp.get_ui_web_html_template(pascal, snake),
                )
                self._write(
                    os.path.join(web_dir, "hooks", f"use_{snake}.js"),
                    tp.get_ui_web_feature_hook_template(pascal, snake),
                )

        # Generate project-level runner scripts (one per platform, named after project not feature)
        # Runner chỉ được tạo một lần khi chưa tồn tại - không ghi đè nếu đã có
        project_snake = (
            re.sub(r"[^a-z0-9_]", "_", project_name.lower()).strip("_")
            if project_name
            else "project"
        )
        for plat in platforms:
            runner_dir = os.path.join(root, "scripts", "run", plat)
            os.makedirs(runner_dir, exist_ok=True)
            if "cli" in plat:
                file_path = os.path.join(runner_dir, f"run_{project_snake}.py")
                if not self._file_repo.file_exists(file_path):
                    self._write(
                        file_path, tp.get_run_cli_project_template(project_snake)
                    )
            elif "desktop_tauri" in plat:
                file_path = os.path.join(runner_dir, f"run_{project_snake}.py")
                if not self._file_repo.file_exists(file_path):
                    self._write(
                        file_path, tp.get_run_tauri_project_template(project_snake)
                    )
            elif "desktop" in plat:
                file_path = os.path.join(runner_dir, f"run_{project_snake}.py")
                if not self._file_repo.file_exists(file_path):
                    self._write(
                        file_path, tp.get_run_desktop_project_template(project_snake)
                    )
            elif "mobile" in plat:
                file_path = os.path.join(runner_dir, f"run_{project_snake}.py")
                if not self._file_repo.file_exists(file_path):
                    self._write(
                        file_path, tp.get_run_mobile_project_template(project_snake)
                    )
            elif "web" in plat:
                file_path = os.path.join(runner_dir, f"run_{project_snake}.py")
                if not self._file_repo.file_exists(file_path):
                    self._write(
                        file_path, tp.get_run_web_project_template(project_snake)
                    )

    def _update_desktop_main_window(self, main_win_path, pascal, snake):
        if not self._file_repo.file_exists(main_win_path):
            return
        content = self._file_repo.read_file(main_win_path)

        # Insert import
        import_stmt = f"from .level_05_pages.{snake}_page import {pascal}Page"
        if import_stmt not in content:
            # Put import statement at the top (after import sys/PyQt)
            lines = content.splitlines()
            insert_idx = 0
            for idx, line in enumerate(lines):
                if line.startswith("class MainWindow"):
                    insert_idx = idx
                    break
            lines.insert(insert_idx, import_stmt)
            content = "\n".join(lines)

        # Insert registration statement
        reg_stmt = f'self.add_page("{snake}", {pascal}Page(self.context), "{pascal}")'
        if reg_stmt not in content:
            if "# <-- REGISTER_PAGES_HERE -->" in content:
                content = content.replace(
                    "# <-- REGISTER_PAGES_HERE -->",
                    f"{reg_stmt}\n        # <-- REGISTER_PAGES_HERE -->",
                )
            else:
                if "self.pages_map = {}" in content:
                    content = content.replace(
                        "self.pages_map = {}",
                        f"self.pages_map = {{}}\n        {reg_stmt}",
                    )

        self._file_repo.write_file(main_win_path, content)

    def _generate_fastapi_router(self, root, pascal, snake, group=""):
        r_dir = os.path.join(
            root,
            paths.SRC,
            paths.LAYER_04,
            paths.UI,
            "web_fastapi",
            "fastapi",
            "routers",
        )
        self._write(os.path.join(r_dir, "__init__.py"), "")
        self._write(
            os.path.join(r_dir, f"{snake}.py"),
            tp.get_fastapi_router_template(pascal, snake, group),
        )

        main_file = os.path.join(
            root,
            paths.SRC,
            paths.LAYER_04,
            paths.UI,
            "web_fastapi",
            "fastapi",
            "main.py",
        )
        if self._file_repo.file_exists(main_file):
            content = self._file_repo.read_file(main_file)
            import_statement = f"from .routers import {snake}"
            if import_statement not in content:
                import_match = re.search(r"(from \.routers import [^\n]+)", content)
                if import_match:
                    content = content.replace(
                        import_match.group(1), f"{import_match.group(1)}, {snake}"
                    )
                else:
                    content = content.replace(
                        "def create_app()", f"{import_statement}\n\ndef create_app()"
                    )

            include_statement = f"app.include_router({snake}.router)"
            if include_statement not in content:
                if "app.include_router(" in content:
                    last_idx = content.rfind("app.include_router(")
                    end_line = content.find("\n", last_idx)
                    content = (
                        content[:end_line]
                        + f"\n    {include_statement}"
                        + content[end_line:]
                    )
                else:
                    content = content.replace(
                        "    return app", f"    {include_statement}\n\n    return app"
                    )
            self._file_repo.write_file(main_file, content)

    def _generate_tests(self, root, pascal, snake, group=""):
        if group:
            unit_test_dir = os.path.join(
                root, paths.TESTS, "unit", paths.LAYER_02, paths.USECASES, group
            )
            os.makedirs(unit_test_dir, exist_ok=True)
            group_init = os.path.join(
                root,
                paths.TESTS,
                "unit",
                paths.LAYER_02,
                paths.USECASES,
                group,
                "__init__.py",
            )
            if not self._file_repo.file_exists(group_init):
                self._write(group_init, "")
        else:
            unit_test_dir = os.path.join(
                root, paths.TESTS, "unit", paths.LAYER_02, paths.USECASES
            )
        self._write(os.path.join(unit_test_dir, "__init__.py"), "")
        self._write(
            os.path.join(unit_test_dir, f"test_{snake}.py"),
            tp.get_test_template(pascal, snake, group),
        )

        integration_test_dir = os.path.join(root, paths.TESTS, "integration")
        self._write(os.path.join(integration_test_dir, "__init__.py"), "")
        self._write(
            os.path.join(integration_test_dir, f"test_{snake}_flow.py"),
            tp.get_integration_test_template(pascal, snake, group),
        )

    def _update_app_contexts(self, root, pascal, snake, platforms, db_techs, group=""):
        bootstrap_dir = os.path.join(root, paths.SRC, paths.LAYER_05)
        if not self._file_repo.file_exists(bootstrap_dir):
            os.makedirs(bootstrap_dir, exist_ok=True)

        di_file = os.path.join(bootstrap_dir, "di_container.py")
        self._write(di_file, tp.get_di_container_template())

        base_ctx = os.path.join(bootstrap_dir, "app_context_base.py")
        self._write(base_ctx, tp.get_app_context_base_template())

        base_plats = set()
        for plat in platforms:
            if "desktop" in plat:
                base_plats.add("desktop")
            elif "mobile" in plat:
                base_plats.add("mobile")
            elif "web" in plat:
                base_plats.add("web")
            else:
                base_plats.add(plat)

        for plat in base_plats:
            ctx_file = os.path.join(bootstrap_dir, f"app_context_{plat}.py")
            if not self._file_repo.file_exists(ctx_file):
                if plat == "web":
                    self._write(ctx_file, tp.get_app_context_web_template())
                elif plat == "desktop":
                    self._write(ctx_file, tp.get_app_context_desktop_template())
                elif plat == "mobile":
                    self._write(ctx_file, tp.get_app_context_mobile_template())
                elif plat == "cli":
                    self._write(ctx_file, tp.get_app_context_cli_template())

        if not pascal:
            return

        for plat in base_plats:
            ctx_file = os.path.join(bootstrap_dir, f"app_context_{plat}.py")
            if not self._file_repo.file_exists(ctx_file):
                continue

            content = self._file_repo.read_file(ctx_file)
            if f"{pascal}Interactor" in content:
                continue

            # Map back to specific platform for imports
            orig_plats = [p for p in platforms if p == plat or (plat in p)]
            # We just use the first matching one for the controller import, or fallback to the generic
            best_plat = orig_plats[0] if orig_plats else plat

            usecase_subpath = f"{group}.{snake}" if group else snake
            imports = [
                f"from src.{paths.LAYER_02}.{paths.USECASES}.{usecase_subpath}.{snake}_interactor import {pascal}Interactor",
                f"from src.{paths.LAYER_02}.{paths.GATEWAYS_INTERFACE}.i_{snake}_repository import I{pascal}Repository",
                f"from src.{paths.LAYER_03}.{paths.GATEWAYS}.{paths.GATEWAYS_OUTBOUND}.i_{snake}_data_source import I{pascal}DataSource",
                f"from src.{paths.LAYER_03}.{paths.GATEWAYS}.{paths.GATEWAYS_INBOUND}.{snake}_repository import {pascal}Repository",
                f"from src.{paths.LAYER_03}.{paths.CONTROLLERS}.{best_plat}.{snake} import {pascal}Controller",
            ]

            for db in db_techs:
                db_pascal = db.capitalize()
                imports.append(
                    f"from src.{paths.LAYER_04}.{paths.DATABASES}.{db}.{snake}_data_source import {db_pascal}{pascal}DataSource"
                )

            # Chèn import thông minh sau dòng import cuối cùng
            lines = content.split("\n")
            insert_idx = 0
            for i, line in enumerate(lines):
                if (
                    line.startswith("from src.")
                    or line.startswith("from .")
                    or line.startswith("import ")
                ):
                    insert_idx = i + 1
            for imp in reversed(imports):
                if imp not in content:
                    lines.insert(insert_idx, imp)
            content = "\n".join(lines)

            marker = "# <-- BIND_REPOSITORY_HERE -->"
            if marker not in content:
                content = content.rstrip() + "\n\n    " + marker + "\n"

            multi_db_note = ""
            if len(db_techs) > 1:
                others = ", ".join(db_techs[1:])
                multi_db_note = (
                    f"\n        # NOTE: Bạn cũng đã sinh DataSource cho: {others}.\n"
                    f"        # Đổi {db_techs[0].capitalize()}{pascal}DataSource bên dưới nếu muốn dùng DB khác.\n"
                )

            camel = pascal[0].lower() + pascal[1:] if pascal else "feature"
            bindings = f"\n        # {pascal} Bindings (DB: {db_techs[0] if db_techs else 'none'}){multi_db_note}\n"
            if db_techs:
                db = db_techs[0]
                db_pascal = db.capitalize()
                bindings += f"        ds_{camel} = {db_pascal}{pascal}DataSource()\n"
                bindings += f"        self.container.register(I{pascal}DataSource, ds_{camel})\n"
                bindings += f"        repo_{camel} = {pascal}Repository(ds_{camel})\n"
            else:
                bindings += f"        repo_{camel} = {pascal}Repository()\n"
            bindings += (
                f"        self.container.register(I{pascal}Repository, repo_{camel})\n"
            )
            bindings += (
                f"        interactor_{camel} = {pascal}Interactor(repo_{camel})\n"
            )
            bindings += f"        self.container.register({pascal}Interactor, interactor_{camel})\n"
            bindings += (
                f"        controller_{camel} = {pascal}Controller(interactor_{camel})\n"
            )
            bindings += f"        self.container.register({pascal}Controller, controller_{camel})\n        {marker}"

            content = content.replace(marker, bindings)
            self._file_repo.write_file(ctx_file, content)

    def _ensure_presentation_services(
        self, root, dest_dir, color_palette="Catppuccin_Mocha"
    ):
        os.makedirs(dest_dir, exist_ok=True)
        self._write(os.path.join(dest_dir, "__init__.py"), "")

        # Chỉ sinh dịch vụ Python cho Desktop PyQt6
        if "desktop_qt6" not in dest_dir:
            return

        services_dir = os.path.join(dest_dir, "services")
        os.makedirs(services_dir, exist_ok=True)
        self._write(os.path.join(services_dir, "__init__.py"), "")

        # Settings Store
        store_path = os.path.join(services_dir, "settings_store.py")
        if not self._file_repo.file_exists(store_path):
            self._write(store_path, tp.get_ui_pyqt6_settings_store_template())

        # Assets Loader
        assets_loader_path = os.path.join(services_dir, "assets_loader.py")
        if not self._file_repo.file_exists(assets_loader_path):
            self._write(assets_loader_path, tp.get_ui_pyqt6_assets_loader_template())

        # Managers
        mode_path = os.path.join(services_dir, "light_dark_mode_manager.py")
        if not self._file_repo.file_exists(mode_path):
            self._write(mode_path, tp.get_ui_pyqt6_light_dark_mode_manager_template())

        # locales under services/i18n/
        i18n_dir = os.path.join(services_dir, "i18n")
        os.makedirs(i18n_dir, exist_ok=True)
        self._write(os.path.join(i18n_dir, "__init__.py"), "")

        i18n_path = os.path.join(i18n_dir, "i18n_manager.py")
        if not self._file_repo.file_exists(i18n_path):
            self._write(i18n_path, tp.get_ui_pyqt6_i18n_manager_template())

        locales_dir = os.path.join(i18n_dir, "locales")
        os.makedirs(locales_dir, exist_ok=True)
        for lang in ["en", "vi", "zh"]:
            lang_path = os.path.join(locales_dir, f"{lang}.json")
            if not self._file_repo.file_exists(lang_path):
                self._write(lang_path, tp.get_ui_pyqt6_locale_json_template(lang))

        # themes under services/theme/
        theme_dir = os.path.join(services_dir, "theme")
        os.makedirs(theme_dir, exist_ok=True)
        self._write(os.path.join(theme_dir, "__init__.py"), "")

        t_name = color_palette.lower()

        theme_path = os.path.join(theme_dir, "theme_manager.py")
        if not self._file_repo.file_exists(theme_path):
            theme_content = tp.get_ui_pyqt6_theme_manager_template()
            theme_content = theme_content.replace(
                'default_theme: str = "classic"', f'default_theme: str = "{t_name}"'
            )
            self._write(theme_path, theme_content)

        base_qss_path = os.path.join(theme_dir, "base.qss")
        if not self._file_repo.file_exists(base_qss_path):
            self._write(base_qss_path, tp.get_ui_pyqt6_base_qss_template())

        themes_dir = os.path.join(theme_dir, "themes")
        os.makedirs(themes_dir, exist_ok=True)

        # Ghi README.md hướng dẫn AI/Developer cách thêm theme động
        readme_path = os.path.join(themes_dir, "README.md")
        if not self._file_repo.file_exists(readme_path):
            self._write(readme_path, tp.get_ui_pyqt6_themes_readme_template())

        # Đọc cấu hình branding từ project_config.json
        from scripts.util_dev.project_manager_app.config.project_config import (
            read_project_branding,
        )

        branding = read_project_branding(root)

        # Động hóa việc sinh theme - Chỉ sinh duy nhất theme đã chọn
        t_dir = os.path.join(themes_dir, t_name)
        os.makedirs(t_dir, exist_ok=True)

        t_json = os.path.join(t_dir, "theme.json")
        if not self._file_repo.file_exists(t_json):
            import json

            # Thư mục chứa các tệp json hệ màu
            presets_dir = os.path.abspath(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "..",
                    "..",
                    "..",
                    "appdata",
                    "theme_presets",
                    "07_color_palettes",
                )
            )
            preset_name = color_palette.lower().replace("_", "")
            preset_file = None

            if os.path.exists(presets_dir):
                for file_name in os.listdir(presets_dir):
                    name_without_ext, _ = os.path.splitext(file_name)
                    if name_without_ext.lower().replace("_", "") == preset_name:
                        preset_file = os.path.join(presets_dir, file_name)
                        break

            # Fallback nếu không tìm thấy tệp preset phù hợp
            if not preset_file or not os.path.exists(preset_file):
                preset_file = os.path.join(presets_dir, "Catppuccin_Mocha.json")

            try:
                with open(preset_file, "r", encoding="utf-8") as f:
                    theme_data = json.load(f)
            except Exception:
                # Fallback cứng nếu không đọc được file
                theme_data = {
                    "dark": {
                        "DARK_BG": "#1e1e2e",
                        "SIDEBAR_BG": "#11111b",
                        "CARD_BG": "#181825",
                        "TEXT_COLOR": "#cdd6f4",
                        "SUBTEXT_COLOR": "#a6adc8",
                        "ACCENT_COLOR": "#89b4fa",
                        "ACCENT_HOVER": "#b4befe",
                        "SUCCESS_COLOR": "#a6e3a1",
                        "ERROR_COLOR": "#f38ba8",
                        "BORDER_COLOR": "#313244",
                        "RADIUS": "8px",
                        "BORDER_WIDTH": "1px",
                        "FONT_FAMILY": "Inter, Roboto, sans-serif",
                    },
                    "light": {
                        "DARK_BG": "#f8f9fa",
                        "SIDEBAR_BG": "#e9ecef",
                        "CARD_BG": "#ffffff",
                        "TEXT_COLOR": "#212529",
                        "SUBTEXT_COLOR": "#6c757d",
                        "ACCENT_COLOR": "#4f46e5",
                        "ACCENT_HOVER": "#4338ca",
                        "SUCCESS_COLOR": "#10b981",
                        "ERROR_COLOR": "#ef4444",
                        "BORDER_COLOR": "#dee2e6",
                        "RADIUS": "8px",
                        "BORDER_WIDTH": "1px",
                        "FONT_FAMILY": "Inter, Roboto, sans-serif",
                    },
                }

            # Áp dụng cấu hình branding thủ công từ project_config.json (nếu có)
            for mode in ["dark", "light"]:
                if mode in theme_data:
                    # Accent colors
                    if f"accent_color_{mode}" in branding:
                        theme_data[mode]["ACCENT_COLOR"] = branding[
                            f"accent_color_{mode}"
                        ]
                    if f"accent_hover_{mode}" in branding:
                        theme_data[mode]["ACCENT_HOVER"] = branding[
                            f"accent_hover_{mode}"
                        ]
                    # Font family
                    if "font_family" in branding:
                        theme_data[mode]["FONT_FAMILY"] = branding["font_family"]

            # Phân tách cấu trúc 7 Trụ cột
            # 1. 07_color_palettes
            pal_dir = os.path.join(t_dir, "07_color_palettes")
            os.makedirs(pal_dir, exist_ok=True)
            color_keys = [
                "DARK_BG",
                "SIDEBAR_BG",
                "CARD_BG",
                "TEXT_COLOR",
                "SUBTEXT_COLOR",
                "ACCENT_COLOR",
                "ACCENT_HOVER",
                "SUCCESS_COLOR",
                "ERROR_COLOR",
                "BORDER_COLOR",
            ]
            pal_data = {}
            for mode in ["dark", "light"]:
                if mode in theme_data:
                    pal_data[mode] = {
                        k: v for k, v in theme_data[mode].items() if k in color_keys
                    }
            self._write(
                os.path.join(pal_dir, "theme.json"),
                json.dumps(pal_data, indent=4, ensure_ascii=False),
            )

            # Lấy mẫu cấu hình hình học/chữ từ mode dark làm đại diện (do dùng chung)
            ref_mode = "dark" if "dark" in theme_data else list(theme_data.keys())[0]
            ref_data = theme_data[ref_mode]

            # 2. 01_geometry_borders
            geom_dir = os.path.join(t_dir, "01_geometry_borders")
            os.makedirs(geom_dir, exist_ok=True)
            geom_data = {
                "RADIUS": ref_data.get("RADIUS", "8px"),
                "RADIUS_NUM": ref_data.get(
                    "RADIUS_NUM", ref_data.get("RADIUS", "8px").replace("px", "")
                ),
                "BORDER_WIDTH": ref_data.get("BORDER_WIDTH", "1px"),
            }
            self._write(
                os.path.join(geom_dir, "theme.json"),
                json.dumps(geom_data, indent=4, ensure_ascii=False),
            )

            # 3. 02_typography
            type_dir = os.path.join(t_dir, "02_typography")
            os.makedirs(type_dir, exist_ok=True)
            type_data = {
                "FONT_FAMILY": ref_data.get("FONT_FAMILY", "Inter, Roboto, sans-serif"),
                "BUTTON_FONT_SIZE": ref_data.get("BUTTON_FONT_SIZE", "13px"),
                "INPUT_FONT_SIZE": ref_data.get("INPUT_FONT_SIZE", "13px"),
            }
            self._write(
                os.path.join(type_dir, "theme.json"),
                json.dumps(type_data, indent=4, ensure_ascii=False),
            )

            # 4. 03_spacing
            space_dir = os.path.join(t_dir, "03_spacing")
            os.makedirs(space_dir, exist_ok=True)
            space_data = {
                "SPACING_BASE": ref_data.get("SPACING_BASE", "8px"),
                "BUTTON_PADDING": ref_data.get("BUTTON_PADDING", "10px 20px"),
                "INPUT_PADDING": ref_data.get("INPUT_PADDING", "8px 12px"),
            }
            self._write(
                os.path.join(space_dir, "theme.json"),
                json.dumps(space_data, indent=4, ensure_ascii=False),
            )

            # 5. 04_shadows_elevation
            shadow_dir = os.path.join(t_dir, "04_shadows_elevation")
            os.makedirs(shadow_dir, exist_ok=True)
            shadow_data = {
                "SHADOW": ref_data.get("SHADOW", "0 4px 6px rgba(0, 0, 0, 0.1)")
            }
            self._write(
                os.path.join(shadow_dir, "theme.json"),
                json.dumps(shadow_data, indent=4, ensure_ascii=False),
            )

            # 6. 05_motion_animations
            motion_dir = os.path.join(t_dir, "05_motion_animations")
            os.makedirs(motion_dir, exist_ok=True)
            motion_data = {
                "TRANSITION_DURATION": ref_data.get("TRANSITION_DURATION", "200ms")
            }
            self._write(
                os.path.join(motion_dir, "theme.json"),
                json.dumps(motion_data, indent=4, ensure_ascii=False),
            )

        t_qss = os.path.join(t_dir, "theme.qss")
        if not self._file_repo.file_exists(t_qss):
            self._write(t_qss, tp.get_ui_pyqt6_classic_theme_qss_template())

        # 7. 06_visual_assets
        assets_dir = os.path.join(t_dir, "06_visual_assets")
        os.makedirs(assets_dir, exist_ok=True)
        for asset_sub in ["images", "fonts", "icons"]:
            d_sub = os.path.join(assets_dir, asset_sub)
            os.makedirs(d_sub, exist_ok=True)
            self._write(os.path.join(d_sub, ".gitkeep"), "")
