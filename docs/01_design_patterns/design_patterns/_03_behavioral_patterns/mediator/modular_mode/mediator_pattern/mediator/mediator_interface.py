from abc import (
    ABC,
    abstractmethod,
)


class MediatorInterface(ABC):
    """
    Role: MediatorInterface
    Description: Core participant in the Mediator Interface.Py structure.
    """

    @abstractmethod
    def notify(
        self,
        sender,
        event: str,
    ):
        pass