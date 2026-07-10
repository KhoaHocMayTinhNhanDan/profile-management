# =========================================================
# File:
# flyweight/modular_mode/flyweight_pattern/flyweight/flyweight_interface.py
# =========================================================

from abc import (
    ABC,
    abstractmethod,
)


class FlyweightInterface(ABC):
    """
    Role: FlyweightInterface
    Description: Core participant in the Flyweight Interface.Py structure.
    """

    @abstractmethod
    def operation(
        self,
        extrinsic_state,
    ):
        pass