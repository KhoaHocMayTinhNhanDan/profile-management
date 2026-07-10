# =========================================================
# File: simple_factory/modular_mode/client/client.py
# =========================================================

from ..simple_factory_pattern.creator.simple_factory import (
    SimpleFactory,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """

    # =====================================================
    # Factory tạo ProductA
    # =====================================================

    product_a = SimpleFactory.create_product("A")

    print(product_a.operation())

    print()

    # =====================================================
    # Factory tạo ProductB
    # =====================================================

    product_b = SimpleFactory.create_product("B")

    print(product_b.operation())