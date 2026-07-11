from abc import ABC, abstractmethod


class AbstractHook(ABC):
    @abstractmethod
    def get_async_template(self) -> str:
        pass

    @abstractmethod
    def get_feature_template(self, pascal_name: str, snake_name: str) -> str:
        pass
