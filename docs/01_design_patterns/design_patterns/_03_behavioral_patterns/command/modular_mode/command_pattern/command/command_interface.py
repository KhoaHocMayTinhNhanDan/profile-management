from abc import ABC, abstractmethod


class CommandInterface(ABC):
    """
    Role: CommandInterface
    Description: Core participant in the Command Interface.Py structure.
    """

    @abstractmethod
    def execute(self):
        pass