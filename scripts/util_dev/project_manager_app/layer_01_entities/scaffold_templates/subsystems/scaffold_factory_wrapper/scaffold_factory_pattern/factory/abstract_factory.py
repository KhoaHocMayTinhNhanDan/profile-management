from abc import ABC, abstractmethod


class ITemplateFactory(ABC):
    """
    Abstract Factory Interface.
    Mỗi Concrete Factory sinh ra các sản phẩm hoặc templates tương ứng.

    GoF Role: AbstractFactory
    """

    @abstractmethod
    def create_page(self, pascal_name: str, snake_name: str) -> str:
        pass

    @abstractmethod
    def create_buttons(self) -> str:
        pass

    @abstractmethod
    def create_inputs(self) -> str:
        pass

    @abstractmethod
    def create_labels(self) -> str:
        pass

    @abstractmethod
    def create_async_hook(self) -> str:
        pass

    @abstractmethod
    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        pass
