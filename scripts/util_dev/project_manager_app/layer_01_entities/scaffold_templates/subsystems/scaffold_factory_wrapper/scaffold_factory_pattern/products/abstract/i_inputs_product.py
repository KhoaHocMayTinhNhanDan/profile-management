from abc import ABC, abstractmethod


class AbstractInputs(ABC):
    """
    GoF Role: AbstractProduct
    """

    @abstractmethod
    def get_template(self) -> str:
        pass
