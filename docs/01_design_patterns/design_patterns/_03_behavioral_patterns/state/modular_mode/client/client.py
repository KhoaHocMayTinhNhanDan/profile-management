# =========================================================
# File:
# state/modular_mode/client/client.py
# =========================================================



from ..state_pattern.context.context import (
    Context,
)

from ..state_pattern.state.concrete_state_a import (
    ConcreteStateA,
)


def run_client():

    print("=" * 50)
    print("CREATE CONTEXT")
    print("=" * 50)

    context = Context(
        ConcreteStateA()
    )

    print()

    print("=" * 50)
    print("REQUEST 1")
    print("=" * 50)

    context.request()

    print()

    print("=" * 50)
    print("REQUEST 2")
    print("=" * 50)

    context.request()