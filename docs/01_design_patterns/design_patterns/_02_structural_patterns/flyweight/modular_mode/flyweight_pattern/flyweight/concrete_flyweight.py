# =========================================================
# File:
# flyweight/modular_mode/flyweight_pattern/flyweight/concrete_flyweight.py
# =========================================================
from .flyweight_interface import (
    FlyweightInterface,
)


class ConcreteFlyweight(
    FlyweightInterface
):
    """
    Role: ConcreteFlyweight
    Description: Core participant in the Concrete Flyweight.Py structure.
    """

    def __init__(
        self,
        shared_state,
    ):

        self._shared_state = (
            shared_state
        )

    def operation(
        self,
        extrinsic_state,
    ):

        return (
            f"Shared: {self._shared_state} | "
            f"Extrinsic: {extrinsic_state}"
        )