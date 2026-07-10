# =========================================================
# File:
# builder/modular_mode/client/client.py
# =========================================================

from ..builder_pattern.builder.concrete_builder_a import (
    ConcreteBuilderA,
)

from ..builder_pattern.builder.concrete_builder_b import (
    ConcreteBuilderB,
)

from ..builder_pattern.director.director import (
    Director,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """

    # =====================================================
    # Builder A
    # =====================================================

    builder_a = ConcreteBuilderA()

    director = Director(builder_a)

    print("=" * 50)
    print("BUILDER A - MINIMAL PRODUCT")
    print("=" * 50)

    director.build_minimal_product()

    product = builder_a.get_product()

    print(product.show_product())

    print()

    print("=" * 50)
    print("BUILDER A - FULL PRODUCT")
    print("=" * 50)

    director.build_full_feature_product()

    product = builder_a.get_product()

    print(product.show_product())

    print()

    # =====================================================
    # Builder B
    # =====================================================

    builder_b = ConcreteBuilderB()

    director.change_builder(builder_b)

    print("=" * 50)
    print("BUILDER B - FULL PRODUCT")
    print("=" * 50)

    director.build_full_feature_product()

    product = builder_b.get_product()

    print(product.show_product())