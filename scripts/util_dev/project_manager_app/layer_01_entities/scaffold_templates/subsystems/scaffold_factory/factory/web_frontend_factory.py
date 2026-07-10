from .abstract_factory import ITemplateFactory
from ..products.web_frontend.web_page_product import WebPage
from ..products.web_frontend.web_buttons_product import WebButtons
from ..products.web_frontend.web_inputs_product import WebInputs
from ..products.web_frontend.web_labels_product import WebLabels
from ..products.web_frontend.web_hook_product import WebHook

class WebFrontendFactory:
    """
    Concrete Factory tạo các UI templates cho Web Frontend Components.
    """
    def create_page(self, pascal_name: str, snake_name: str) -> str:
        return WebPage().get_template(pascal_name, snake_name)

    def create_buttons(self) -> str:
        return WebButtons().get_template()

    def create_inputs(self) -> str:
        return WebInputs().get_template()

    def create_labels(self) -> str:
        return WebLabels().get_template()

    def create_async_hook(self) -> str:
        return WebHook().get_async_template()

    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        return WebHook().get_feature_template(pascal_name, snake_name)
