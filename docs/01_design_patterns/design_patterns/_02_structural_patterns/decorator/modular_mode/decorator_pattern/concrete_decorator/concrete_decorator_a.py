# =========================================================
# File:
# decorator/modular_mode/decorator_pattern/concrete_decorator/concrete_decorator_a.py
# =========================================================

from ..decorator.base_decorator import (
    BaseDecorator,
)


class ConcreteDecoratorA(BaseDecorator):
    """
    Role: ConcreteDecoratorA
    Description: Core participant in the Concrete Decorator A.Py structure.
    """

    def operation(self):

        return (
            "DecoratorA("
            f"{super().operation()}"
            ")"
        )