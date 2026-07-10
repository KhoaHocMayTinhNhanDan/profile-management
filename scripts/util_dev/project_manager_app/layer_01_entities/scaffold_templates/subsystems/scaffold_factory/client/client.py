from ..factory.abstract_factory import ITemplateFactory

class TemplateClient:
    """
    TemplateClient (Client của Abstract Factory Pattern).
    Nhận một Concrete Factory cụ thể (implementing ITemplateFactory hoặc Protocol) 
    và dùng nó để lấy ra các UI products.
    """
    def __init__(self, factory: ITemplateFactory):
        self._factory = factory

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
