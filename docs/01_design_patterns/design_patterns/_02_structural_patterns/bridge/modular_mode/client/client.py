# =========================================================
# File:
# bridge/modular_mode/client/client.py
# =========================================================

from ..bridge_pattern.abstraction.abstraction import (
    Abstraction,
)

from ..bridge_pattern.abstraction.refined_abstraction import (
    RefinedAbstraction,
)

from ..bridge_pattern.implementation.concrete_implementation_a import (
    ConcreteImplementationA,
)

from ..bridge_pattern.implementation.concrete_implementation_b import (
    ConcreteImplementationB,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("ABSTRACTION + IMPLEMENTATION A")
    print("=" * 50)

    implementation_a = (
        ConcreteImplementationA()
    )

    abstraction = Abstraction(
        implementation_a
    )

    print(abstraction.operation())

    print()

    print("=" * 50)
    print("REFINED ABSTRACTION + IMPLEMENTATION B")
    print("=" * 50)

    implementation_b = (
        ConcreteImplementationB()
    )

    refined_abstraction = (
        RefinedAbstraction(
            implementation_b
        )
    )

    print(refined_abstraction.operation())