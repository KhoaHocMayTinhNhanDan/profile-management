from .command_interface import (
    CommandInterface,
)


class ConcreteCommandA(
    CommandInterface
):
    """
    Role: ConcreteCommandA
    Description: Core participant in the Concrete Command A.Py structure.
    """

    def __init__(self, receiver):

        self._receiver = receiver

    def execute(self):

        return (
            "[CommandA] -> "
            f"{self._receiver.action_a()}"
        )