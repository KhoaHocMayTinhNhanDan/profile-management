from ..mediator.mediator_interface import (
    MediatorInterface,
)


class BaseComponent:
    """
    Role: BaseComponent
    Description: Core participant in the Base Component.Py structure.
    """

    def __init__(
        self,
        mediator: MediatorInterface,
    ):

        self._mediator = mediator