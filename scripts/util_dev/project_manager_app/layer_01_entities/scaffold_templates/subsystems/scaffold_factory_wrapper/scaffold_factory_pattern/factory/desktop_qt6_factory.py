from .abstract_factory import ITemplateFactory
from ..products.desktop_qt6.qt6_page_product import Qt6Page
from ..products.desktop_qt6.qt6_buttons_product import Qt6Buttons
from ..products.desktop_qt6.qt6_inputs_product import Qt6Inputs
from ..products.desktop_qt6.qt6_labels_product import Qt6Labels
from ..products.desktop_qt6.qt6_main_window_product import Qt6MainWindow
from ..products.desktop_qt6.qt6_ui_inspector_product import Qt6UiInspector
from ..products.desktop_qt6.qt6_hook_product import Qt6Hook


class DesktopQt6Factory(ITemplateFactory):
    """
    Concrete Factory tạo các UI templates cho Desktop PyQt6.

    GoF Role: ConcreteFactory
    """

    def create_page(self, pascal_name: str, snake_name: str) -> str:
        return Qt6Page().get_template(pascal_name, snake_name)

    def create_buttons(self) -> str:
        return Qt6Buttons().get_template()

    def create_buttons_qss(self) -> str:
        return Qt6Buttons().get_qss_template()

    def create_inputs(self) -> str:
        return Qt6Inputs().get_template()

    def create_inputs_qss(self) -> str:
        return Qt6Inputs().get_qss_template()

    def create_labels(self) -> str:
        return Qt6Labels().get_template()

    def create_labels_qss(self) -> str:
        return Qt6Labels().get_qss_template()

    def create_main_window(self, project_name: str = "Application") -> str:
        return Qt6MainWindow().get_template(project_name)

    def create_ui_inspector(self) -> str:
        return Qt6UiInspector().get_template()

    def create_ui_inspector_qss(self) -> str:
        return Qt6UiInspector().get_qss_template()

    def create_assets_loader(self) -> str:
        from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.scaffold_facade_pattern.presentation_templates import (
            ASSETS_LOADER_TEMPLATE,
        )

        return ASSETS_LOADER_TEMPLATE

    def create_async_hook(self) -> str:
        return Qt6Hook().get_async_template()

    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        return Qt6Hook().get_feature_template(pascal_name, snake_name)
