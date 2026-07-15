from abc import ABC, abstractmethod


class AbstractButtons(ABC):
    """
    GoF Role: AbstractProduct
    """

    @abstractmethod
    def get_template(self) -> str:
        pass
