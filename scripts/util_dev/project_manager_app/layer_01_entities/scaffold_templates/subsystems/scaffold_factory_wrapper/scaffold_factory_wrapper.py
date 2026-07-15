from typing import Any


class ScaffoldFactoryWrapper:
    """
    ScaffoldFactoryWrapper (Public Entry Point of scaffold_factory package).
    Resolves the concrete factory based on the platform string and delegates calls to it.
    Can also accept a direct factory instance for unit testing.
    """

    def __init__(self, platform_or_factory):
        self._factory: Any
        if isinstance(platform_or_factory, str):
            self._factory = self._resolve_factory(platform_or_factory)
        else:
            self._factory = platform_or_factory

    def _resolve_factory(self, platform: str):
        # Local lazy imports to prevent circular imports during packaging initialization
        if platform == "web_fastapi":
            from .scaffold_factory_pattern.factory.web_fastapi_factory import (
                WebFastApiFactory,
            )

            return WebFastApiFactory()
        elif platform == "web" or platform == "web_frontend":
            from .scaffold_factory_pattern.factory.web_frontend_factory import (
                WebFrontendFactory,
            )

            return WebFrontendFactory()
        elif platform == "desktop_qt6":
            from .scaffold_factory_pattern.factory.desktop_qt6_factory import (
                DesktopQt6Factory,
            )

            return DesktopQt6Factory()
        elif platform == "desktop_qt5":
            from .scaffold_factory_pattern.factory.desktop_qt5_factory import (
                DesktopQt5Factory,
            )

            return DesktopQt5Factory()
        elif platform == "desktop_tkinter":
            from .scaffold_factory_pattern.factory.desktop_tkinter_factory import (
                DesktopTkinterFactory,
            )

            return DesktopTkinterFactory()
        elif platform == "mobile_kivy":
            from .scaffold_factory_pattern.factory.mobile_kivy_factory import (
                MobileKivyFactory,
            )

            return MobileKivyFactory()
        elif platform == "mobile_flutter":
            from .scaffold_factory_pattern.factory.mobile_flutter_factory import (
                MobileFlutterFactory,
            )

            return MobileFlutterFactory()
        elif platform == "mobile_jetpack_compose":
            from .scaffold_factory_pattern.factory.mobile_jetpack_compose_factory import (
                MobileJetpackComposeFactory,
            )

            return MobileJetpackComposeFactory()
        elif platform == "mobile_react_native":
            from .scaffold_factory_pattern.factory.mobile_react_native_factory import (
                MobileReactNativeFactory,
            )

            return MobileReactNativeFactory()
        elif platform == "cli":
            from .scaffold_factory_pattern.factory.cli_factory import CliFactory

            return CliFactory()
        elif platform == "runner":
            from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

            return RunnerFactory()
        elif platform == "common":
            from .scaffold_factory_pattern.factory.common_factory import CommonFactory

            return CommonFactory()
        else:
            raise ValueError(f"Unsupported platform key: {platform}")

    # =========================================================================
    # Instance Delegations (Abstract Factory UI products)
    # =========================================================================

    def get_page(self, pascal_name: str, snake_name: str) -> str:
        return self._factory.create_page(pascal_name, snake_name)

    def get_buttons(self) -> str:
        return self._factory.create_buttons()

    def get_inputs(self) -> str:
        return self._factory.create_inputs()

    def get_labels(self) -> str:
        return self._factory.create_labels()

    def get_async_hook(self) -> str:
        return self._factory.create_async_hook()

    def get_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        return self._factory.create_feature_hook(pascal_name, snake_name)

    def get_ui_inspector(self) -> str:
        func = getattr(self._factory, "create_ui_inspector", None)
        if func and callable(func):
            res = func()
            if isinstance(res, str):
                return res
        return ""

    def get_main_window(self, project_name: str) -> str:
        func = getattr(self._factory, "create_main_window", None)
        if func and callable(func):
            res = func(project_name)
            if isinstance(res, str):
                return res
        return ""

    def get_buttons_qss(self) -> str:
        func = getattr(self._factory, "create_buttons_qss", None)
        if func and callable(func):
            res = func()
            if isinstance(res, str):
                return res
        return ""

    def get_inputs_qss(self) -> str:
        func = getattr(self._factory, "create_inputs_qss", None)
        if func and callable(func):
            res = func()
            if isinstance(res, str):
                return res
        return ""

    def get_labels_qss(self) -> str:
        func = getattr(self._factory, "create_labels_qss", None)
        if func and callable(func):
            res = func()
            if isinstance(res, str):
                return res
        return ""

    # =========================================================================
    # Static Delegations (Common Architecture & Script Templates)
    # =========================================================================

    @staticmethod
    def get_usecase_interactor_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_usecase_interactor_template(pascal_name, snake_name)

    @staticmethod
    def get_usecase_dto_template(pascal_name: str) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_usecase_dto_template(pascal_name)

    @staticmethod
    def get_usecase_repository_interface_template(pascal_name: str) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_usecase_repository_interface_template(pascal_name)

    @staticmethod
    def get_controller_template(
        pascal_name: str, snake_name: str, platform: str, group: str = ""
    ) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_controller_template(
            pascal_name, snake_name, platform, group
        )

    @staticmethod
    def get_presenter_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_presenter_template(pascal_name, snake_name, group)

    @staticmethod
    def get_outbound_data_source_interface_template(pascal_name: str) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_outbound_data_source_interface_template(pascal_name)

    @staticmethod
    def get_repository_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_repository_template(pascal_name, snake_name)

    @staticmethod
    def get_data_source_impl_template(
        pascal_name: str, snake_name: str, tech: str
    ) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_data_source_impl_template(
            pascal_name, snake_name, tech
        )

    @staticmethod
    def get_test_template(pascal_name: str, snake_name: str, group: str = "") -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_test_template(pascal_name, snake_name, group)

    @staticmethod
    def get_integration_test_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_integration_test_template(
            pascal_name, snake_name, group
        )

    @staticmethod
    def get_di_container_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_di_container_template()

    @staticmethod
    def get_app_context_base_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_app_context_base_template()

    @staticmethod
    def get_app_context_desktop_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_app_context_desktop_template()

    @staticmethod
    def get_app_context_web_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_app_context_web_template()

    @staticmethod
    def get_app_context_mobile_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_app_context_mobile_template()

    @staticmethod
    def get_app_context_cli_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_app_context_cli_template()

    @staticmethod
    def get_app_logger_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_app_logger_template()

    @staticmethod
    def get_config_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_config_template()

    @staticmethod
    def get_fastapi_router_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        from .scaffold_factory_pattern.factory.web_fastapi_factory import (
            WebFastApiFactory,
        )

        return WebFastApiFactory.get_fastapi_router_template(
            pascal_name, snake_name, group
        )

    @staticmethod
    def get_fastapi_main_template(project_name: str) -> str:
        from .scaffold_factory_pattern.factory.web_fastapi_factory import (
            WebFastApiFactory,
        )

        return WebFastApiFactory.get_fastapi_main_template(project_name)

    @staticmethod
    def get_fastapi_debug_router_template() -> str:
        from .scaffold_factory_pattern.factory.web_fastapi_factory import (
            WebFastApiFactory,
        )

        return WebFastApiFactory.get_fastapi_debug_router_template()

    @staticmethod
    def get_ui_cli_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.cli_factory import CliFactory

        return CliFactory.get_ui_cli_template(pascal_name, snake_name)

    @staticmethod
    def get_run_cli_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_cli_template(pascal_name, snake_name)

    @staticmethod
    def get_run_desktop_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_desktop_template(pascal_name, snake_name)

    @staticmethod
    def get_run_cli_project_template(project_snake: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_cli_project_template(project_snake)

    @staticmethod
    def get_run_desktop_project_template(project_snake: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_desktop_project_template(project_snake)

    @staticmethod
    def get_run_mobile_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_mobile_template(pascal_name, snake_name)

    @staticmethod
    def get_run_web_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_web_template(pascal_name, snake_name)

    @staticmethod
    def get_run_mobile_project_template(project_snake: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_mobile_project_template(project_snake)

    @staticmethod
    def get_run_web_project_template(project_snake: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_web_project_template(project_snake)

    @staticmethod
    def get_run_tauri_project_template(project_snake: str) -> str:
        from .scaffold_factory_pattern.factory.runner_factory import RunnerFactory

        return RunnerFactory.get_run_tauri_project_template(project_snake)

    @staticmethod
    def get_ui_pyqt5_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.desktop_qt5_factory import (
            DesktopQt5Factory,
        )

        return DesktopQt5Factory.get_ui_pyqt5_template(pascal_name, snake_name)

    @staticmethod
    def get_ui_tkinter_template(pascal_name: str, snake_name: str) -> str:
        from .scaffold_factory_pattern.factory.desktop_tkinter_factory import (
            DesktopTkinterFactory,
        )

        return DesktopTkinterFactory.get_ui_tkinter_template(pascal_name, snake_name)

    @staticmethod
    def get_design_token_linter_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_design_token_linter_template()

    @staticmethod
    def get_test_theme_tokens_linter_template() -> str:
        from .scaffold_factory_pattern.factory.common_factory import CommonFactory

        return CommonFactory.get_test_theme_tokens_linter_template()
