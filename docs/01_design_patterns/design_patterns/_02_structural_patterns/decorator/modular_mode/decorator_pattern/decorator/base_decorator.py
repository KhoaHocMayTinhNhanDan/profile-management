# =========================================================
# File:
# decorator/modular_mode/decorator_pattern/decorator/base_decorator.py
# =========================================================

from ..component.component import Component


class BaseDecorator(Component):
    """
    Role: BaseDecorator
    Description: Core participant in the Base Decorator.Py structure.
    """

    def __init__(self, component: Component):

        self.component = component

    def operation(self):

        return self.component.operation()