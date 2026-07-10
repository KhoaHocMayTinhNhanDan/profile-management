from abc import ABC, abstractmethod


class ProductInterface(ABC):

    @abstractmethod
    def operation(self) -> str:
        pass