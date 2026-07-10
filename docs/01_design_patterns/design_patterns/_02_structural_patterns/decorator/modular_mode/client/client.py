# =========================================================
# File:
# decorator/modular_mode/client/client.py
# =========================================================

from ..decorator_pattern.concrete_component.concrete_component import (
    ConcreteComponent,
)

from ..decorator_pattern.concrete_decorator.concrete_decorator_a import (
    ConcreteDecoratorA,
)

from ..decorator_pattern.concrete_decorator.concrete_decorator_b import (
    ConcreteDecoratorB,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CONCRETE COMPONENT")
    print("=" * 50)

    component = ConcreteComponent()

    print(component.operation())

    print()

    print("=" * 50)
    print("DECORATOR A")
    print("=" * 50)

    decorator_a = ConcreteDecoratorA(
        component
    )

    print(decorator_a.operation())

    print()

    print("=" * 50)
    print("DECORATOR A + DECORATOR B")
    print("=" * 50)

    decorator_b = ConcreteDecoratorB(
        decorator_a
    )

    print(decorator_b.operation())