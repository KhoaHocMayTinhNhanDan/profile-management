from .command_interface import (
    CommandInterface,
)


class ConcreteCommandB(
    CommandInterface
):
    """
    Role: ConcreteCommandB
    Description: Core participant in the Concrete Command B.Py structure.
    """

    def __init__(self, receiver):

        self._receiver = receiver

    def execute(self):

        return (
            "[CommandB] -> "
            f"{self._receiver.action_b()}"
        )