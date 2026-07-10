from ..strategy.strategy_interface import (
    StrategyInterface,
)


class Context:
    """
    Role: Context
    Description: Core participant in the Strategy Pattern structure.
    """

    def __init__(
        self,
        strategy: StrategyInterface,
    ):

        self._strategy = strategy

    @property
    def strategy(self):

        return self._strategy

    @strategy.setter
    def strategy(
        self,
        strategy: StrategyInterface,
    ):

        print(
            f"Context switched to: "
            f"{strategy.__class__.__name__}"
        )

        self._strategy = strategy

    def execute_strategy(self):

        print(
            "Context delegating work to strategy..."
        )

        return self._strategy.execute()