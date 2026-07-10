from abc import abstractmethod


class ElementInterface:
    """
    Role: ElementInterface
    Description: Core participant in the Element Interface.Py structure.
    """

    @abstractmethod
    def accept(self, visitor):
        pass