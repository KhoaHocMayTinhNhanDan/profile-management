from ..originator.originator import (
    Originator,
)


class Caretaker:
    """
    Role: Caretaker
    Description: Core participant in the Memento Pattern structure.
    """

    def __init__(
        self,
        originator: Originator,
    ):

        self._originator = originator

        self._history = []

    def backup(self):

        self._history.append(
            self._originator.save()
        )

    def undo(self):

        if not self._history:

            print(
                "[Caretaker]"
                " No history."
            )

            return

        memento = (
            self._history.pop()
        )

        print(
            "[Caretaker]"
            f" Restore: "
            f"{memento.get_name()}"
        )

        self._originator.restore(
            memento
        )

    def show_history(self):

        print(
            "[Caretaker]"
            " Snapshot History:"
        )

        for memento in self._history:

            print(
                memento.get_name()
            )