import os
import re
from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_file_repository import IFileRepository
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_dto import GenerateFeatureInput, GenerateFeatureOutput
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates import CleanArchitectureTemplate as tp
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates import CleanArchitecturePaths as paths

def to_snake_case(name: str) -> str:
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def to_pascal_case(name: str) -> str:
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return ''.join(word.title() for word in name.split('_') if word)

class GenerateFeatureInteractor:
    def __init__(self, file_repo: IFileRepository):
        self._file_repo = file_repo

    def execute(self, input_data: GenerateFeatureInput) -> GenerateFeatureOutput:
        snake = to_snake_case(input_data.feature_name)
        pascal = to_pascal_case(snake)
        root = input_data.project_root_dir
        
        try:
            self._ensure_common_infra(root)
            
            # Nếu chỉ là khởi tạo dự án rỗng
            if not input_data.feature_name.strip():
                self._generate_ui_pages(root, "", "", input_data.platforms, input_data.project_name)
                self._update_app_contexts(root, "", "", input_data.platforms, input_data.db_techs)
                return GenerateFeatureOutput("ok", "Project structured scaffolded successfully.")
                
            self._generate_layer_02(root, pascal, snake)
            self._generate_layer_03(root, pascal, snake, input_data.platforms)
            self._generate_layer_04_repositories(root, pascal, snake, input_data.db_techs)
            self._generate_ui_pages(root, pascal, snake, input_data.platforms, input_data.project_name)
            if "web" in input_data.platforms or not input_data.platforms:
                self._generate_fastapi_router(root, pascal, snake)
            self._generate_tests(root, pascal, snake)
            self._update_app_contexts(root, pascal, snake, input_data.platforms, input_data.db_techs)
            return GenerateFeatureOutput("ok", f"Feature '{pascal}' generated successfully.")
        except Exception as e:
            return GenerateFeatureOutput("error", str(e))

    def _ensure_common_infra(self, root):
        # Automate layer_01_entities scaffolding
        entities_dir = os.path.join(root, paths.SRC, paths.LAYER_01)
        os.makedirs(entities_dir, exist_ok=True)
        init_file = os.path.join(entities_dir, "__init__.py")
        if not self._file_repo.file_exists(init_file):
            self._write(init_file, "# Clean Architecture Layer 1: Entities\n")

        # Automate layer_04_infrastructure standard directories scaffolding (Self-Documenting Structure)
        infra_subdirs = {
            paths.DATABASES: "# Clean Architecture Layer 4: Databases (SQLite, Postgres, MongoDB, etc.)\n",
            paths.DEVICES: "# Clean Architecture Layer 4: Devices & Hardware Drivers\n",
            paths.EXTERNAL_SERVICES: "# Clean Architecture Layer 4: External Services (Email, SMS, Payment Gateways etc.)\n",
            paths.UI: "# Clean Architecture Layer 4: User Interfaces (Desktop, CLI, Web, etc.)\n",
            paths.WEB_DRIVERS: "# Clean Architecture Layer 4: Web Servers & API Client Drivers\n"
        }
        for subdir, desc in infra_subdirs.items():
            dir_path = os.path.join(root, paths.SRC, paths.LAYER_04, subdir)
            os.makedirs(dir_path, exist_ok=True)
            init_file_path = os.path.join(dir_path, "__init__.py")
            if not self._file_repo.file_exists(init_file_path):
                self._write(init_file_path, desc)
            gitkeep_path = os.path.join(dir_path, ".gitkeep")
            if not self._file_repo.file_exists(gitkeep_path):
                self._write(gitkeep_path, "# Gitkeep to preserve self-documenting directory structure\n")

        logger_path = os.path.join(root, paths.SRC, "shared", "logger", "app_logger.py")
        if not self._file_repo.file_exists(logger_path):
            os.makedirs(os.path.dirname(logger_path), exist_ok=True)
            self._write(os.path.join(root, paths.SRC, "shared", "__init__.py"), "")
            self._write(os.path.join(root, paths.SRC, "shared", "logger", "__init__.py"), "")
            self._write(logger_path, tp.get_app_logger_template())
            
        config_path = os.path.join(root, paths.SRC, "config.py")
        if not self._file_repo.file_exists(config_path):
            self._write(config_path, tp.get_config_template())

    def _write(self, path: str, content: str):
        if not self._file_repo.file_exists(path):
            self._file_repo.write_file(path, content.strip() + "\n")
            print(f"Created: {path}")

    def _generate_layer_02(self, root, pascal, snake):
        usecase_dir = os.path.join(root, paths.SRC, paths.LAYER_02, paths.USECASES, snake)
        self._write(os.path.join(usecase_dir, f"{snake}_interactor.py"), tp.get_usecase_interactor_template(pascal, snake))
        self._write(os.path.join(usecase_dir, f"{snake}_dto.py"), tp.get_usecase_dto_template(pascal))
        self._write(os.path.join(usecase_dir, "__init__.py"), "")
        
        gw_interface_dir = os.path.join(root, paths.SRC, paths.LAYER_02, paths.GATEWAYS_INTERFACE)
        self._write(os.path.join(gw_interface_dir, f"i_{snake}_repository.py"), tp.get_usecase_repository_interface_template(pascal))

    def _generate_layer_03(self, root, pascal, snake, platforms):
        for plat in platforms:
            c_dir = os.path.join(root, paths.SRC, paths.LAYER_03, paths.CONTROLLERS, plat)
            self._write(os.path.join(c_dir, f"{snake}.py"), tp.get_controller_template(pascal, snake, plat))
            
            p_dir = os.path.join(root, paths.SRC, paths.LAYER_03, paths.PRESENTERS, plat)
            self._write(os.path.join(p_dir, f"{snake}.py"), tp.get_presenter_template(pascal, snake))
            
        gw_dir = os.path.join(root, paths.SRC, paths.LAYER_03, paths.GATEWAYS)
        self._write(os.path.join(gw_dir, paths.GATEWAYS_OUTBOUND, f"i_{snake}_data_source.py"), tp.get_outbound_data_source_interface_template(pascal))
        self._write(os.path.join(gw_dir, paths.GATEWAYS_INBOUND, f"{snake}_repository.py"), tp.get_repository_template(pascal, snake))

    def _generate_layer_04_repositories(self, root, pascal, snake, db_techs):
        for db in db_techs:
            db_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.DATABASES, db)
            self._write(os.path.join(db_dir, f"{snake}_data_source.py"), tp.get_data_source_impl_template(pascal, snake, db))

    def _generate_ui_pages(self, root, pascal, snake, platforms, project_name: str = ""):
        if "desktop" in platforms:
            qt6_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.UI, "desktop_qt6")
            main_win_path = os.path.join(qt6_dir, "main_window.py")
            
            # Chỉ sinh bộ khung UI lần đầu tiên (nếu main_window.py chưa tồn tại)
            if not self._file_repo.file_exists(main_win_path):
                # Sinh bộ dịch vụ theme/i18n cục bộ cho Desktop PyQt6
                self._ensure_presentation_services(root, qt6_dir)
                
                # Create Atomic Design directories & Hooks directory
                for sub in ["level_01_atoms", "level_02_molecules", "level_03_organisms", "level_04_templates", "level_05_pages", "hooks"]:
                    d = os.path.join(qt6_dir, sub)
                    os.makedirs(d, exist_ok=True)
                    self._write(os.path.join(d, "__init__.py"), "")
                    
                # Create Assets subdirectories
                for asset_sub in ["images", "fonts", "icons"]:
                    os.makedirs(os.path.join(qt6_dir, "assets", asset_sub), exist_ok=True)
                    
                self._write(os.path.join(qt6_dir, "__init__.py"), "")
                
                # Ensure PyQt6 BasePageTemplate exists
                page_tpl_path = os.path.join(qt6_dir, "level_04_templates", "page_template.py")
                if not self._file_repo.file_exists(page_tpl_path):
                    self._write(page_tpl_path, tp.get_ui_pyqt6_base_page_template())
                
                # Write base atomic components
                self._write(os.path.join(qt6_dir, "level_01_atoms", "buttons.py"), tp.get_ui_pyqt6_atom_buttons_template())
                self._write(os.path.join(qt6_dir, "level_01_atoms", "inputs.py"), tp.get_ui_pyqt6_atom_inputs_template())
                self._write(os.path.join(qt6_dir, "level_01_atoms", "labels.py"), tp.get_ui_pyqt6_atom_labels_template())
                self._write(os.path.join(qt6_dir, "level_02_molecules", "ui_inspector.py"), tp.get_ui_pyqt6_ui_inspector_template())
                
                # Write base hooks
                self._write(os.path.join(qt6_dir, "hooks", "use_async.py"), tp.get_ui_pyqt6_use_async_template())
                
                # Write welcome_page.py
                self._write(os.path.join(qt6_dir, "level_05_pages", "welcome_page.py"), tp.get_ui_pyqt6_page_template("Welcome", "welcome"))
                
                # Write main_window.py
                self._write(main_win_path, tp.get_ui_pyqt6_main_window_template())
                
            # Sinh trang con & Hook cụ thể cho từng feature (nếu có snake name)
            if snake:
                self._write(os.path.join(qt6_dir, "level_05_pages", f"{snake}_page.py"), tp.get_ui_pyqt6_page_template(pascal, snake))
                self._write(os.path.join(qt6_dir, "hooks", f"use_{snake}.py"), tp.get_ui_pyqt6_feature_hook_template(pascal, snake))

        if "desktop_qt5" in platforms:
            qt_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.UI, "desktop_qt5", "pages")
            welcome_path = os.path.join(qt_dir, "welcome_page.py")
            if not self._file_repo.file_exists(welcome_path):
                os.makedirs(qt_dir, exist_ok=True)
                self._write(os.path.join(qt_dir, "__init__.py"), "")
                self._write(welcome_path, tp.get_ui_pyqt5_template("Welcome", "welcome"))
            
        if "desktop_tkinter" in platforms:
            tk_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.UI, "desktop_tkinter", "pages")
            welcome_path = os.path.join(tk_dir, "welcome_page.py")
            if not self._file_repo.file_exists(welcome_path):
                os.makedirs(tk_dir, exist_ok=True)
                self._write(os.path.join(tk_dir, "__init__.py"), "")
                self._write(welcome_path, tp.get_ui_tkinter_template("Welcome", "welcome"))
            
        if "mobile" in platforms:
            kv_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.UI, "mobile", "kivy")
            welcome_path = os.path.join(kv_dir, "level_05_pages", "welcome_page.py")
            if not self._file_repo.file_exists(welcome_path):
                # Sinh bộ dịch vụ theme/i18n cục bộ cho Mobile Kivy
                self._ensure_presentation_services(root, kv_dir)
                
                for sub in ["level_01_atoms", "level_02_molecules", "level_03_organisms", "level_04_templates", "level_05_pages", "hooks"]:
                    d = os.path.join(kv_dir, sub)
                    os.makedirs(d, exist_ok=True)
                    self._write(os.path.join(d, "__init__.py"), "")
                    
                # Create Assets subdirectories
                for asset_sub in ["images", "fonts", "icons"]:
                    os.makedirs(os.path.join(kv_dir, "assets", asset_sub), exist_ok=True)
                    
                self._write(os.path.join(kv_dir, "__init__.py"), "")
                
                # Write base Kivy atomic components
                self._write(os.path.join(kv_dir, "level_01_atoms", "buttons.py"), tp.get_ui_kivy_atom_buttons_template())
                self._write(os.path.join(kv_dir, "level_01_atoms", "inputs.py"), tp.get_ui_kivy_atom_inputs_template())
                self._write(os.path.join(kv_dir, "level_01_atoms", "labels.py"), tp.get_ui_kivy_atom_labels_template())
                
                # Write base hooks
                self._write(os.path.join(kv_dir, "hooks", "use_async.py"), tp.get_ui_kivy_use_async_template())
                
                # Write page
                self._write(welcome_path, tp.get_ui_kivy_template("Welcome", "welcome"))
                
            # Sinh trang con & Hook cụ thể cho từng feature (nếu có snake name)
            if snake:
                self._write(os.path.join(kv_dir, "level_05_pages", f"{snake}_page.py"), tp.get_ui_kivy_template(pascal, snake))
                self._write(os.path.join(kv_dir, "hooks", f"use_{snake}.py"), tp.get_ui_kivy_feature_hook_template(pascal, snake))
            
        if "cli" in platforms:
            cli_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.UI, "cli", "commands")
            welcome_path = os.path.join(cli_dir, "welcome_cli.py")
            if not self._file_repo.file_exists(welcome_path):
                os.makedirs(cli_dir, exist_ok=True)
                self._write(os.path.join(cli_dir, "__init__.py"), "")
                self._write(welcome_path, tp.get_ui_cli_template("Welcome", "welcome"))
            
        if "web" in platforms or not platforms:
            web_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.UI, "web", "frontend")
            welcome_path = os.path.join(web_dir, "level_05_pages", "welcome.html")
            if not self._file_repo.file_exists(welcome_path):
                # Sinh bộ dịch vụ theme/i18n cục bộ cho Web Frontend
                self._ensure_presentation_services(root, web_dir)
                
                for sub in ["level_01_atoms", "level_02_molecules", "level_03_organisms", "level_04_templates", "level_05_pages", "hooks"]:
                    d = os.path.join(web_dir, sub)
                    os.makedirs(d, exist_ok=True)
                    self._write(os.path.join(d, "__init__.py"), "")
                    
                # Create Assets subdirectories
                for asset_sub in ["images", "fonts", "icons"]:
                    os.makedirs(os.path.join(web_dir, "assets", asset_sub), exist_ok=True)
                    
                self._write(os.path.join(web_dir, "__init__.py"), "")
                    
                # Write base Web Component HTML/JS atoms
                self._write(os.path.join(web_dir, "level_01_atoms", "buttons.js"), tp.get_ui_web_atom_buttons_template())
                self._write(os.path.join(web_dir, "level_01_atoms", "inputs.js"), tp.get_ui_web_atom_inputs_template())
                self._write(os.path.join(web_dir, "level_01_atoms", "labels.js"), tp.get_ui_web_atom_labels_template())
                
                # Write base hooks
                self._write(os.path.join(web_dir, "hooks", "use_async.js"), tp.get_ui_web_use_async_template())
                
                # Write page under level_05_pages/
                self._write(welcome_path, tp.get_ui_web_html_template("Welcome", "welcome"))
                
            # Sinh trang con & Hook cụ thể cho từng feature (nếu có snake name)
            if snake:
                self._write(os.path.join(web_dir, "level_05_pages", f"{snake}.html"), tp.get_ui_web_html_template(pascal, snake))
                self._write(os.path.join(web_dir, "hooks", f"use_{snake}.js"), tp.get_ui_web_feature_hook_template(pascal, snake))





        # Generate project-level runner scripts (one per platform, named after project not feature)
        # Runner chỉ được tạo một lần khi chưa tồn tại - không ghi đè nếu đã có
        project_snake = re.sub(r'[^a-z0-9_]', '_', project_name.lower()).strip('_') if project_name else "project"
        for plat in platforms:
            runner_dir = os.path.join(root, "scripts", "run", plat)
            os.makedirs(runner_dir, exist_ok=True)
            if plat == "cli":
                file_path = os.path.join(runner_dir, f"run_{project_snake}.py")
                if not self._file_repo.file_exists(file_path):
                    self._write(file_path, tp.get_run_cli_project_template(project_snake))
            elif plat == "desktop":
                file_path = os.path.join(runner_dir, f"run_{project_snake}.py")
                if not self._file_repo.file_exists(file_path):
                    self._write(file_path, tp.get_run_desktop_project_template(project_snake))


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
                    f"{reg_stmt}\n        # <-- REGISTER_PAGES_HERE -->"
                )
            else:
                if "self.pages_map = {}" in content:
                    content = content.replace(
                        "self.pages_map = {}",
                        f"self.pages_map = {{}}\n        {reg_stmt}"
                    )
                    
        self._file_repo.write_file(main_win_path, content)

    def _generate_fastapi_router(self, root, pascal, snake):
        r_dir = os.path.join(root, paths.SRC, paths.LAYER_04, paths.UI, "web", "fastapi", "routers")
        self._write(os.path.join(r_dir, "__init__.py"), "")
        self._write(os.path.join(r_dir, f"{snake}.py"), tp.get_fastapi_router_template(pascal, snake))
        
        main_file = os.path.join(root, paths.SRC, paths.LAYER_04, paths.UI, "web", "fastapi", "main.py")
        if self._file_repo.file_exists(main_file):
            content = self._file_repo.read_file(main_file)
            import_statement = f"from .routers import {snake}"
            if import_statement not in content:
                import_match = re.search(r'(from \.routers import [^\n]+)', content)
                if import_match:
                    content = content.replace(import_match.group(1), f"{import_match.group(1)}, {snake}")
                else:
                    content = content.replace("def create_app()", f"{import_statement}\\n\\ndef create_app()")
            
            include_statement = f"app.include_router({snake}.router)"
            if include_statement not in content:
                if "app.include_router(" in content:
                    last_idx = content.rfind("app.include_router(")
                    end_line = content.find("\\n", last_idx)
                    content = content[:end_line] + f"\\n    {include_statement}" + content[end_line:]
                else:
                    content = content.replace("    return app", f"    {include_statement}\\n\\n    return app")
            self._file_repo.write_file(main_file, content)
 
    def _generate_tests(self, root, pascal, snake):
        unit_test_dir = os.path.join(root, paths.TESTS, "unit", paths.LAYER_02, paths.USECASES)
        self._write(os.path.join(unit_test_dir, "__init__.py"), "")
        self._write(os.path.join(unit_test_dir, f"test_{snake}.py"), tp.get_test_template(pascal, snake))
        
        integration_test_dir = os.path.join(root, paths.TESTS, "integration")
        self._write(os.path.join(integration_test_dir, "__init__.py"), "")
        self._write(os.path.join(integration_test_dir, f"test_{snake}_flow.py"), tp.get_integration_test_template(pascal, snake))
 
    def _update_app_contexts(self, root, pascal, snake, platforms, db_techs):
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
            if f"{pascal}Interactor" in content: continue
            
            # Map back to specific platform for imports
            orig_plats = [p for p in platforms if p == plat or (plat == "desktop" and "desktop" in p)]
            # We just use the first matching one for the controller import, or fallback to the generic
            best_plat = orig_plats[0] if orig_plats else plat
            
            imports = [
                f"from src.{paths.LAYER_02}.{paths.USECASES}.{snake}.{snake}_interactor import {pascal}Interactor",
                f"from src.{paths.LAYER_02}.{paths.GATEWAYS_INTERFACE}.i_{snake}_repository import I{pascal}Repository",
                f"from src.{paths.LAYER_03}.{paths.GATEWAYS}.{paths.GATEWAYS_OUTBOUND}.i_{snake}_data_source import I{pascal}DataSource",
                f"from src.{paths.LAYER_03}.{paths.GATEWAYS}.{paths.GATEWAYS_INBOUND}.{snake}_repository import {pascal}Repository",
                f"from src.{paths.LAYER_03}.{paths.CONTROLLERS}.{best_plat}.{snake} import {pascal}Controller"
            ]
            
            for db in db_techs:
                db_pascal = db.capitalize()
                imports.append(f"from src.{paths.LAYER_04}.{paths.DATABASES}.{db}.{snake}_data_source import {db_pascal}{pascal}DataSource")
                
            # Chèn import thông minh sau dòng import cuối cùng
            lines = content.split('\n')
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('from src.') or line.startswith('from .') or line.startswith('import '):
                    insert_idx = i + 1
            for imp in reversed(imports):
                if imp not in content:
                    lines.insert(insert_idx, imp)
            content = '\n'.join(lines)
            
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

            bindings = f"\n        # {pascal} Bindings (DB: {db_techs[0] if db_techs else 'none'}){multi_db_note}\n"
            if db_techs:
                db = db_techs[0]
                db_pascal = db.capitalize()
                bindings += f"        self.container.register(I{pascal}DataSource, {db_pascal}{pascal}DataSource())\n"
            bindings += f"        self.container.register(I{pascal}Repository, {pascal}Repository(self.container.resolve(I{pascal}DataSource)))\n"
            bindings += f"        self.container.register({pascal}Interactor, {pascal}Interactor(self.container.resolve(I{pascal}Repository)))\n"
            bindings += f"        self.container.register({pascal}Controller, {pascal}Controller(self.container.resolve({pascal}Interactor)))\n        {marker}"
            
            content = content.replace(marker, bindings)
            self._file_repo.write_file(ctx_file, content)

    def _ensure_presentation_services(self, root, dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        self._write(os.path.join(dest_dir, "__init__.py"), "")
        
        # Write theme.py entry point
        theme_py_path = os.path.join(dest_dir, "theme.py")
        if not self._file_repo.file_exists(theme_py_path):
            self._write(theme_py_path, "from .services.theme.theme_manager import ThemeManager\n")
            
        services_dir = os.path.join(dest_dir, "services")
        os.makedirs(services_dir, exist_ok=True)
        self._write(os.path.join(services_dir, "__init__.py"), "")
        
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
        
        theme_path = os.path.join(theme_dir, "theme_manager.py")
        if not self._file_repo.file_exists(theme_path):
            self._write(theme_path, tp.get_ui_pyqt6_theme_manager_template())
            
        base_qss_path = os.path.join(theme_dir, "base.qss")
        if not self._file_repo.file_exists(base_qss_path):
            self._write(base_qss_path, tp.get_ui_pyqt6_base_qss_template())

        themes_dir = os.path.join(theme_dir, "themes")
        os.makedirs(themes_dir, exist_ok=True)
        
        for t_name in ["classic", "comic", "galaxy", "ironman"]:
            t_dir = os.path.join(themes_dir, t_name)
            os.makedirs(t_dir, exist_ok=True)
            
            t_json = os.path.join(t_dir, "theme.json")
            if not self._file_repo.file_exists(t_json):
                self._write(t_json, tp.get_ui_pyqt6_classic_theme_json_template())
                
            t_qss = os.path.join(t_dir, "theme.qss")
            if not self._file_repo.file_exists(t_qss):
                self._write(t_qss, tp.get_ui_pyqt6_classic_theme_qss_template())
                
            assets = os.path.join(t_dir, "assets")
            os.makedirs(assets, exist_ok=True)
            self._write(os.path.join(assets, ".gitkeep"), "# Assets placeholder")
