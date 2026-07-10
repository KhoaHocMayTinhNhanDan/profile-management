# =========================================================
# File: factory_method/modular_mode/client/client.py
# =========================================================

from ..factory_method_pattern.creator.concrete_creator_a import (
    ConcreteCreatorA,
)

from ..factory_method_pattern.creator.concrete_creator_b import (
    ConcreteCreatorB,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """

    # =====================================================
    # ConcreteCreatorA quyết định:
    # tạo ConcreteProductA
    # =====================================================

    creator_a = ConcreteCreatorA()

    print(creator_a.some_operation())

    print()

    # =====================================================
    # ConcreteCreatorB quyết định:
    # tạo ConcreteProductB
    # =====================================================

    creator_b = ConcreteCreatorB()

    print(creator_b.some_operation())