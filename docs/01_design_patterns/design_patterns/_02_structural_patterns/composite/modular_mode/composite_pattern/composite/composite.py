# =========================================================
# File:
# composite/modular_mode/composite_pattern/composite/composite.py
# =========================================================

from ..component.component import Component


class Composite(Component):
    """
    Role: Composite
    Description: Core participant in the Composite Pattern structure.
    """

    def __init__(self):

        self.children = []

    def add(self, component):

        self.children.append(component)

    def remove(self, component):

        self.children.remove(component)

    def is_composite(self):

        return True

    def operation(self):

        results = []

        for child in self.children:

            results.append(
                child.operation()
            )

        return (
            f"Composite({'+'.join(results)})"
        )