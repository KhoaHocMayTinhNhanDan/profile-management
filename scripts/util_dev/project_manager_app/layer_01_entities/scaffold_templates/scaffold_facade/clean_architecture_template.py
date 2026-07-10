"""
CleanArchitectureTemplate — Facade Pattern

Lớp này là Facade, giữ nguyên toàn bộ API công khai để tương thích ngược.
Nó đóng vai trò là Client hoặc wrapper gọi xuống bộ Abstract Factory được thiết kế chuẩn GoF:
    templates/
    ├── client/                          ← TemplateClient (sử dụng Concrete Factory)
    ├── factory/                         ← Interface & Concrete Factories
    └── products/                        ← Phân cấp sản phẩm template chuỗi UI
"""

from ..subsystems import (
    CommonFactory,
    DesktopQt6Factory,
    DesktopQt5Factory,
    DesktopTkinterFactory,
    MobileKivyFactory,
    WebFastApiFactory,
    WebFrontendFactory,
    CliFactory,
    RunnerFactory,
    TemplateClient,
)


class CleanArchitectureTemplate:
    """
    Facade — Thực thể cốt lõi chứa quy tắc về hình dáng của mã nguồn Clean Architecture.
    Delegate toàn bộ logic xuống bộ các concrete factory & products học thuật.
    """

    # =========================================================================
    # Common — UseCase, Gateway, Repository, DataSource, Bootstrap
    # =========================================================================

    @staticmethod
    def get_usecase_interactor_template(pascal_name: str, snake_name: str) -> str:
        return CommonFactory.get_usecase_interactor_template(pascal_name, snake_name)

    @staticmethod
    def get_usecase_dto_template(pascal_name: str) -> str:
        return CommonFactory.get_usecase_dto_template(pascal_name)

    @staticmethod
    def get_usecase_repository_interface_template(pascal_name: str) -> str:
        return CommonFactory.get_usecase_repository_interface_template(pascal_name)

    @staticmethod
    def get_controller_template(pascal_name: str, snake_name: str, platform: str) -> str:
        return CommonFactory.get_controller_template(pascal_name, snake_name, platform)

    @staticmethod
    def get_presenter_template(pascal_name: str, snake_name: str) -> str:
        return CommonFactory.get_presenter_template(pascal_name, snake_name)

    @staticmethod
    def get_outbound_data_source_interface_template(pascal_name: str) -> str:
        return CommonFactory.get_outbound_data_source_interface_template(pascal_name)

    @staticmethod
    def get_repository_template(pascal_name: str, snake_name: str) -> str:
        return CommonFactory.get_repository_template(pascal_name, snake_name)

    @staticmethod
    def get_data_source_impl_template(pascal_name: str, snake_name: str, tech: str) -> str:
        return CommonFactory.get_data_source_impl_template(pascal_name, snake_name, tech)

    @staticmethod
    def get_test_template(pascal_name: str, snake_name: str) -> str:
        return CommonFactory.get_test_template(pascal_name, snake_name)

    @staticmethod
    def get_integration_test_template(pascal_name: str, snake_name: str) -> str:
        return CommonFactory.get_integration_test_template(pascal_name, snake_name)

    @staticmethod
    def get_di_container_template() -> str:
        return CommonFactory.get_di_container_template()

    @staticmethod
    def get_app_context_base_template() -> str:
        return CommonFactory.get_app_context_base_template()

    @staticmethod
    def get_app_context_desktop_template() -> str:
        return CommonFactory.get_app_context_desktop_template()

    @staticmethod
    def get_app_context_web_template() -> str:
        return CommonFactory.get_app_context_web_template()

    @staticmethod
    def get_app_context_mobile_template() -> str:
        return CommonFactory.get_app_context_mobile_template()

    @staticmethod
    def get_app_context_cli_template() -> str:
        return CommonFactory.get_app_context_cli_template()

    @staticmethod
    def get_app_logger_template() -> str:
        return CommonFactory.get_app_logger_template()

    @staticmethod
    def get_config_template() -> str:
        return CommonFactory.get_config_template()

    # =========================================================================
    # Desktop — PyQt6 (Sử dụng qua Client của Abstract Factory)
    # =========================================================================

    @staticmethod
    def get_ui_pyqt6_atom_buttons_template() -> str:
        client = TemplateClient(DesktopQt6Factory())
        return client.get_buttons()

    @staticmethod
    def get_ui_pyqt6_atom_inputs_template() -> str:
        client = TemplateClient(DesktopQt6Factory())
        return client.get_inputs()

    @staticmethod
    def get_ui_pyqt6_atom_labels_template() -> str:
        client = TemplateClient(DesktopQt6Factory())
        return client.get_labels()

    @staticmethod
    def get_ui_pyqt6_page_template(pascal_name: str, snake_name: str) -> str:
        client = TemplateClient(DesktopQt6Factory())
        return client.get_page(pascal_name, snake_name)

    @staticmethod
    def get_ui_pyqt6_main_window_template() -> str:
        return DesktopQt6Factory().create_main_window()

    @staticmethod
    def get_ui_pyqt6_ui_inspector_template() -> str:
        return DesktopQt6Factory().create_ui_inspector()

    # =========================================================================
    # Desktop — PyQt5
    # =========================================================================

    @staticmethod
    def get_ui_pyqt5_template(pascal_name: str, snake_name: str) -> str:
        return DesktopQt5Factory.get_ui_pyqt5_template(pascal_name, snake_name)

    # =========================================================================
    # Desktop — Tkinter
    # =========================================================================

    @staticmethod
    def get_ui_tkinter_template(pascal_name: str, snake_name: str) -> str:
        return DesktopTkinterFactory.get_ui_tkinter_template(pascal_name, snake_name)

    # =========================================================================
    # Mobile — Kivy (Sử dụng qua Client của Abstract Factory)
    # =========================================================================

    @staticmethod
    def get_ui_kivy_atom_buttons_template() -> str:
        client = TemplateClient(MobileKivyFactory())
        return client.get_buttons()

    @staticmethod
    def get_ui_kivy_atom_inputs_template() -> str:
        client = TemplateClient(MobileKivyFactory())
        return client.get_inputs()

    @staticmethod
    def get_ui_kivy_atom_labels_template() -> str:
        client = TemplateClient(MobileKivyFactory())
        return client.get_labels()

    @staticmethod
    def get_ui_kivy_template(pascal_name: str, snake_name: str) -> str:
        client = TemplateClient(MobileKivyFactory())
        return client.get_page(pascal_name, snake_name)

    # =========================================================================
    # Web — FastAPI Backend
    # =========================================================================

    @staticmethod
    def get_fastapi_router_template(pascal_name: str, snake_name: str) -> str:
        return WebFastApiFactory.get_fastapi_router_template(pascal_name, snake_name)

    # =========================================================================
    # Web — Frontend (Sử dụng qua Client của Abstract Factory)
    # =========================================================================

    @staticmethod
    def get_ui_web_atom_buttons_template() -> str:
        client = TemplateClient(WebFrontendFactory())
        return client.get_buttons()

    @staticmethod
    def get_ui_web_atom_inputs_template() -> str:
        client = TemplateClient(WebFrontendFactory())
        return client.get_inputs()

    @staticmethod
    def get_ui_web_atom_labels_template() -> str:
        client = TemplateClient(WebFrontendFactory())
        return client.get_labels()

    @staticmethod
    def get_ui_web_html_template(pascal_name: str, snake_name: str) -> str:
        client = TemplateClient(WebFrontendFactory())
        return client.get_page(pascal_name, snake_name)

    # =========================================================================
    # CLI
    # =========================================================================

    @staticmethod
    def get_ui_cli_template(pascal_name: str, snake_name: str) -> str:
        return CliFactory.get_ui_cli_template(pascal_name, snake_name)

    # =========================================================================
    # Runner scripts
    # =========================================================================

    @staticmethod
    def get_run_cli_template(pascal_name: str, snake_name: str) -> str:
        return RunnerFactory.get_run_cli_template(pascal_name, snake_name)

    @staticmethod
    def get_run_desktop_template(pascal_name: str, snake_name: str) -> str:
        return RunnerFactory.get_run_desktop_template(pascal_name, snake_name)

    @staticmethod
    def get_run_cli_project_template(project_snake: str) -> str:
        return RunnerFactory.get_run_cli_project_template(project_snake)

    @staticmethod
    def get_run_desktop_project_template(project_snake: str) -> str:
        return RunnerFactory.get_run_desktop_project_template(project_snake)

    # =========================================================================
    # PyQt6 Presentation Services & Templates
    # =========================================================================

    @staticmethod
    def get_ui_pyqt6_i18n_manager_template() -> str:
        from .presentation_templates import I18N_MANAGER_TEMPLATE
        return I18N_MANAGER_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_light_dark_mode_manager_template() -> str:
        from .presentation_templates import LIGHT_DARK_MODE_MANAGER_TEMPLATE
        return LIGHT_DARK_MODE_MANAGER_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_theme_manager_template() -> str:
        from .presentation_templates import THEME_MANAGER_TEMPLATE
        return THEME_MANAGER_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_base_qss_template() -> str:
        from .presentation_templates import BASE_QSS_TEMPLATE
        return BASE_QSS_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_classic_theme_json_template() -> str:
        from .presentation_templates import CLASSIC_THEME_JSON_TEMPLATE
        return CLASSIC_THEME_JSON_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_classic_theme_qss_template() -> str:
        from .presentation_templates import CLASSIC_THEME_QSS_TEMPLATE
        return CLASSIC_THEME_QSS_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_base_page_template() -> str:
        from .presentation_templates import BASE_PAGE_TEMPLATE
        return BASE_PAGE_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_locale_json_template(lang: str) -> str:
        from .presentation_templates import EN_JSON_TEMPLATE, VI_JSON_TEMPLATE, ZH_JSON_TEMPLATE
        if lang == "vi":
            return VI_JSON_TEMPLATE
        elif lang == "zh":
            return ZH_JSON_TEMPLATE
        return EN_JSON_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_use_async_template() -> str:
        client = TemplateClient(DesktopQt6Factory())
        return client.get_async_hook()

    @staticmethod
    def get_ui_kivy_use_async_template() -> str:
        client = TemplateClient(MobileKivyFactory())
        return client.get_async_hook()

    @staticmethod
    def get_ui_web_use_async_template() -> str:
        client = TemplateClient(WebFrontendFactory())
        return client.get_async_hook()

    @staticmethod
    def get_ui_pyqt6_feature_hook_template(pascal: str, snake: str) -> str:
        client = TemplateClient(DesktopQt6Factory())
        return client.get_feature_hook(pascal, snake)

    @staticmethod
    def get_ui_kivy_feature_hook_template(pascal: str, snake: str) -> str:
        client = TemplateClient(MobileKivyFactory())
        return client.get_feature_hook(pascal, snake)

    @staticmethod
    def get_ui_web_feature_hook_template(pascal: str, snake: str) -> str:
        client = TemplateClient(WebFrontendFactory())
        return client.get_feature_hook(pascal, snake)




