# =========================================================
# File:
# flyweight/modular_mode/flyweight_pattern/flyweight/unshared_concrete_flyweight.py
# =========================================================

from .flyweight_interface import (
    FlyweightInterface,
)


class UnsharedConcreteFlyweight(
    FlyweightInterface
):
    """
    Role: UnsharedConcreteFlyweight
    Description: Core participant in the Unshared Concrete Flyweight.Py structure.
    """

    def __init__(
        self,
        state,
    ):

        self._state = state

    def operation(
        self,
        extrinsic_state,
    ):

        return (
            f"Unshared: {self._state} | "
            f"Extrinsic: {extrinsic_state}"
        )