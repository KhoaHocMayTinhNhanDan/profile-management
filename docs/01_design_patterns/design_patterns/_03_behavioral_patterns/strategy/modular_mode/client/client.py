from ..strategy_pattern.context.context import (
    Context,
)

from ..strategy_pattern.strategy.concrete_strategy_a import (
    ConcreteStrategyA,
)

from ..strategy_pattern.strategy.concrete_strategy_b import (
    ConcreteStrategyB,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CREATE CONTEXT")
    print("=" * 50)

    context = Context(
        ConcreteStrategyA()
    )

    print()

    print("=" * 50)
    print("EXECUTE STRATEGY A")
    print("=" * 50)

    result = context.execute_strategy()

    print(
        f"Result: {result}"
    )

    print()

    print("=" * 50)
    print("SWITCH TO STRATEGY B")
    print("=" * 50)

    context.strategy = (
        ConcreteStrategyB()
    )

    print()

    print("=" * 50)
    print("EXECUTE STRATEGY B")
    print("=" * 50)

    result = context.execute_strategy()

    print(
        f"Result: {result}"
    )