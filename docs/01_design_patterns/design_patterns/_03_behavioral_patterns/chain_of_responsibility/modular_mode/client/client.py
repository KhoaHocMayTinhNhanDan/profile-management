# =========================================================
# File:
# chain_of_responsibility/modular_mode/client/client.py
# =========================================================

from ..chain_of_responsibility_pattern.concrete_handler.monkey_handler import (
    MonkeyHandler,
)

from ..chain_of_responsibility_pattern.concrete_handler.squirrel_handler import (
    SquirrelHandler,
)

from ..chain_of_responsibility_pattern.concrete_handler.dog_handler import (
    DogHandler,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("BUILD CHAIN")
    print("=" * 50)

    # =====================================================
    # CREATE HANDLERS
    # =====================================================

    monkey = MonkeyHandler()

    squirrel = SquirrelHandler()

    dog = DogHandler()

    # =====================================================
    # BUILD CHAIN
    # =====================================================

    monkey.set_next(
        squirrel
    ).set_next(
        dog
    )

    print(
        "Monkey -> Squirrel -> Dog"
    )

    print()

    # =====================================================
    # SEND REQUESTS
    # =====================================================

    requests = [
        "Nut",
        "Banana",
        "MeatBall",
        "Coffee",
    ]

    for request in requests:

        print("=" * 50)

        print(
            f"Request: {request}"
        )

        result = monkey.handle(request)

        if result:

            print(result)

        else:

            print(
                f"No handler for {request}."
            )

        print()