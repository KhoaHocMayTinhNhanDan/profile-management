from ..memento.memento import (
    Memento,
)


class Originator:
    """
    Role: Originator
    Description: Core participant in the Memento Pattern structure.
    """

    def __init__(
        self,
        state: str,
    ):

        self._state = state

    def do_something(
        self,
        new_state: str,
    ):

        print(
            f"[Originator]"
            f" Change state to: "
            f"{new_state}"
        )

        self._state = new_state

    def save(self):

        print(
            "[Originator]"
            " Save snapshot."
        )

        return Memento(
            self._state
        )

    def restore(
        self,
        memento: Memento,
    ):

        self._state = (
            memento.get_state()
        )

        print(
            "[Originator]"
            f" Restored state: "
            f"{self._state}"
        )

    def show_state(self):

        return (
            f"Current State: "
            f"{self._state}"
        )