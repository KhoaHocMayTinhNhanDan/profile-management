from datetime import (
    datetime,
)


class Memento:
    """
    Role: Memento
    Description: Core participant in the Memento Pattern structure.
    """

    def __init__(
        self,
        state: str,
    ):

        self._state = state

        self._created_at = (
            datetime.now()
        )

    def get_state(self):

        return self._state

    def get_name(self):

        return (
            f"{self._created_at}"
            f" / "
            f"{self._state}"
        )