from abc import ABC, abstractmethod


class StrategyInterface(ABC):
    """
    Role: StrategyInterface
    Description: Core participant in the Strategy Interface.Py structure.
    """

    @abstractmethod
    def execute(self, data):
        pass