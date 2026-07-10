# =========================================================
# File:
# state/modular_mode/state_pattern/state/
# concrete_state_b.py
# =========================================================

"""
Concrete State B
--------------------------------------------------------

State khác với behavior khác.
"""

from .state_interface import (
    StateInterface,
)


class ConcreteStateB(
    StateInterface
):

    def handle(self):

        print(
            "ConcreteStateB handling request."
        )

        print(
            "ConcreteStateB transitions "
            "to ConcreteStateA."
        )

        # ==========================================
        # Import tại runtime
        # để tránh circular import
        # ==========================================

        from .concrete_state_a import (
            ConcreteStateA,
        )

        self.context.set_state(
            ConcreteStateA()
        )