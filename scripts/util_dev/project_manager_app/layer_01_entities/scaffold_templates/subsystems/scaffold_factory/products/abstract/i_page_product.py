from abc import ABC, abstractmethod


class AbstractPage(ABC):
    @abstractmethod
    def get_template(self, pascal_name: str, snake_name: str) -> str:
        pass
