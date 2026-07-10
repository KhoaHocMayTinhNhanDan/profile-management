# =========================================================
# File:
# state/modular_mode/state_pattern/context/context.py
# =========================================================

"""
Context
--------------------------------------------------------

Giữ current state
và delegate behavior cho state object.
"""


class Context:

    def __init__(self, state):

        self._state = None

        self.set_state(state)

    def set_state(self, state):

        print(
            f"Context transitions to: "
            f"{state.__class__.__name__}"
        )

        self._state = state

        self._state.context = self

    def request(self):

        self._state.handle()