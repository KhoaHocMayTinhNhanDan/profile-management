# =========================================================
# File:
# state/modular_mode/state_pattern/state/
# concrete_state_a.py
# =========================================================

"""
Concrete State A
--------------------------------------------------------

State xử lý behavior riêng
và có thể transition state.
"""

from .state_interface import (
    StateInterface,
)


class ConcreteStateA(
    StateInterface
):

    def handle(self):

        print(
            "ConcreteStateA handling request."
        )

        print(
            "ConcreteStateA transitions "
            "to ConcreteStateB."
        )

        # ==========================================
        # Import tại runtime
        # để tránh circular import
        # ==========================================

        from .concrete_state_b import (
            ConcreteStateB,
        )

        self.context.set_state(
            ConcreteStateB()
        )