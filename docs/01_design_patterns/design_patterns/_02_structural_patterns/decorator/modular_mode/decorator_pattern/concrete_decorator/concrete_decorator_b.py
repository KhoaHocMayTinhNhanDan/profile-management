# =========================================================
# File:
# decorator/modular_mode/decorator_pattern/concrete_decorator/concrete_decorator_b.py
# =========================================================

from ..decorator.base_decorator import (
    BaseDecorator,
)


class ConcreteDecoratorB(BaseDecorator):
    """
    Role: ConcreteDecoratorB
    Description: Core participant in the Concrete Decorator B.Py structure.
    """

    def operation(self):

        return (
            "DecoratorB("
            f"{super().operation()}"
            ")"
        )