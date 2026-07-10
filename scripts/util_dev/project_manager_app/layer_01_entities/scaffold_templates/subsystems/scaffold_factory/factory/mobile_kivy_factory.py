from .abstract_factory import ITemplateFactory
from ..products.mobile_kivy.kivy_page_product import KivyPage
from ..products.mobile_kivy.kivy_buttons_product import KivyButtons
from ..products.mobile_kivy.kivy_inputs_product import KivyInputs
from ..products.mobile_kivy.kivy_labels_product import KivyLabels
from ..products.mobile_kivy.kivy_hook_product import KivyHook

class MobileKivyFactory:
    """
    Concrete Factory tạo các UI templates cho Mobile Kivy.
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
