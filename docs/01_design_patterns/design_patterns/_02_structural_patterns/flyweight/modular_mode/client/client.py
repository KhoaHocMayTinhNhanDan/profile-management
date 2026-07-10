# =========================================================
# File:
# flyweight/modular_mode/client/client.py
# =========================================================

from ..flyweight_pattern.factory.flyweight_factory import (
    FlyweightFactory,
)

from ..flyweight_pattern.context.context import (
    Context,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CREATE FACTORY")
    print("=" * 50)

    factory = FlyweightFactory()

    print()

    print("=" * 50)
    print("REQUEST FLYWEIGHTS")
    print("=" * 50)

    flyweight_a = (
        factory.get_flyweight(
            "TREE_TEXTURE"
        )
    )

    flyweight_b = (
        factory.get_flyweight(
            "TREE_TEXTURE"
        )
    )

    flyweight_c = (
        factory.get_flyweight(
            "ROCK_TEXTURE"
        )
    )

    print()

    print("=" * 50)
    print("CREATE CONTEXT OBJECTS")
    print("=" * 50)

    tree_1 = Context(
        flyweight_a,
        {
            "x": 10,
            "y": 20,
        },
    )

    tree_2 = Context(
        flyweight_b,
        {
            "x": 50,
            "y": 80,
        },
    )

    rock_1 = Context(
        flyweight_c,
        {
            "x": 100,
            "y": 200,
        },
    )

    print(tree_1.operation())

    print(tree_2.operation())

    print(rock_1.operation())

    print()

    print("=" * 50)
    print("CHECK SHARED OBJECT")
    print("=" * 50)

    print(
        flyweight_a is flyweight_b
    )

    print()

    factory.list_flyweights()