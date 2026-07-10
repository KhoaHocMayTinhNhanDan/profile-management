# =========================================================
# File:
# composite/modular_mode/composite_pattern/leaf/leaf.py
# =========================================================

from ..component.component import Component


class Leaf(Component):
    """
    Role: Leaf
    Description: Core participant in the Composite Pattern structure.
    """

    def operation(self):

        return "Leaf"