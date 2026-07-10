# =========================================================
# File:
# composite/modular_mode/client/client.py
# =========================================================

from ..composite_pattern.leaf.leaf import (
    Leaf,
)

from ..composite_pattern.composite.composite import (
    Composite,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("LEAF")
    print("=" * 50)

    leaf = Leaf()

    print(leaf.operation())

    print()

    print("=" * 50)
    print("COMPOSITE TREE")
    print("=" * 50)

    tree = Composite()

    branch_1 = Composite()
    branch_1.add(Leaf())
    branch_1.add(Leaf())

    branch_2 = Composite()
    branch_2.add(Leaf())

    tree.add(branch_1)
    tree.add(branch_2)

    print(tree.operation())