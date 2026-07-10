from .strategy_interface import (
    StrategyInterface,
)


class ConcreteStrategyB(
    StrategyInterface
):
    """
    Role: ConcreteStrategyB
    Description: Core participant in the Concrete Strategy B.Py structure.
    """

    def execute(self):

        print(
            "ConcreteStrategyB executing algorithm..."
        )

        return "Algorithm B Result"