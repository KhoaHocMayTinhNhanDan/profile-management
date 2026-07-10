# =========================================================
# File:
# flyweight/modular_mode/flyweight_pattern/factory/flyweight_factory.py
# =========================================================

from ..flyweight.concrete_flyweight import (
    ConcreteFlyweight,
)


class FlyweightFactory:
    """
    Role: FlyweightFactory
    Description: Core participant in the Flyweight Factory.Py structure.
    """

    def __init__(self):

        self._flyweights = {}

    def get_flyweight(
        self,
        shared_state,
    ):

        key = str(shared_state)

        # ==================================================
        # Reuse existing flyweight
        # ==================================================

        if key not in self._flyweights:

            print(
                f"[Factory] Creating flyweight: {key}"
            )

            self._flyweights[key] = (
                ConcreteFlyweight(
                    shared_state
                )
            )

        else:

            print(
                f"[Factory] Reusing flyweight: {key}"
            )

        return self._flyweights[key]

    def list_flyweights(self):

        print("\nCached Flyweights:")

        for key in self._flyweights:
            print(key)