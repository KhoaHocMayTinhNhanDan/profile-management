# =========================================================
# File:
# flyweight/modular_mode/flyweight_pattern/context/context.py
# =========================================================


class Context:
    """
    Role: Context
    Description: Core participant in the Flyweight Pattern structure.
    """

    def __init__(
        self,
        flyweight,
        unique_state,
    ):

        self._flyweight = (
            flyweight
        )

        self._unique_state = (
            unique_state
        )

    def operation(self):

        return self._flyweight.operation(
            self._unique_state
        )