from .strategy_interface import (
    StrategyInterface,
)


class ConcreteStrategyA(
    StrategyInterface
):
    """
    Role: ConcreteStrategyA
    Description: Core participant in the Concrete Strategy A.Py structure.
    """

    def execute(self):

        print(
            "ConcreteStrategyA executing algorithm..."
        )

        return "Algorithm A Result"