from .abstract_factory import ITemplateFactory
from ..products.mobile_kivy.kivy_page_product import KivyPage
from ..products.mobile_kivy.kivy_buttons_product import KivyButtons
from ..products.mobile_kivy.kivy_inputs_product import KivyInputs
from ..products.mobile_kivy.kivy_labels_product import KivyLabels
from ..products.mobile_kivy.kivy_hook_product import KivyHook
from ..products.mobile_kivy.kivy_ui_inspector_product import KivyUiInspector
from ..products.mobile_kivy.kivy_main_window_product import KivyMainWindow


class MobileKivyFactory(ITemplateFactory):
    """
    Concrete Factory tạo các UI templates cho Mobile Kivy.

    GoF Role: ConcreteFactory
    """

    def create_page(self, pascal_name: str, snake_name: str) -> str:
        return KivyPage().get_template(pascal_name, snake_name)

    def create_buttons(self) -> str:
        return KivyButtons().get_template()

    def create_inputs(self) -> str:
        return KivyInputs().get_template()

    def create_labels(self) -> str:
        return KivyLabels().get_template()

    def create_async_hook(self) -> str:
        return KivyHook().get_async_template()

    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        return KivyHook().get_feature_template(pascal_name, snake_name)

    def create_ui_inspector(self) -> str:
        return KivyUiInspector().get_template()

    def create_main_window(self, project_name: str) -> str:
        return KivyMainWindow().get_template(project_name)
