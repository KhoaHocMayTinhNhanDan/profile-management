# =========================================================
# File:
# decorator/modular_mode/decorator_pattern/concrete_component/concrete_component.py
# =========================================================

from ..component.component import Component


class ConcreteComponent(Component):
    """
    Role: ConcreteComponent
    Description: Core participant in the Concrete Component.Py structure.
    """

    def operation(self):

        return "ConcreteComponent"