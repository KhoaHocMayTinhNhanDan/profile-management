from abc import ABC, abstractmethod


class AbstractMainWindow(ABC):
    """
    GoF Role: AbstractProduct
    """

    @abstractmethod
    def get_template(self) -> str:
        pass
