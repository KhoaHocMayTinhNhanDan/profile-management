from abc import ABC, abstractmethod


class AbstractLabels(ABC):
    """
    GoF Role: AbstractProduct
    """

    @abstractmethod
    def get_template(self) -> str:
        pass
