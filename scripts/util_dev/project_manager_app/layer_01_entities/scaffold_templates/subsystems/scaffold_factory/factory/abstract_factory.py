from typing import Protocol, runtime_checkable


@runtime_checkable
class ITemplateFactory(Protocol):
    """
    Abstract Factory Interface.
    Mỗi Concrete Factory sinh ra các sản phẩm hoặc templates tương ứng.
    """

    def create_page(self, pascal_name: str, snake_name: str) -> str: ...

    def create_buttons(self) -> str: ...

    def create_inputs(self) -> str: ...

    def create_labels(self) -> str: ...

    def create_async_hook(self) -> str: ...

    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str: ...
