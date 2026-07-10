from .element_interface import ElementInterface


class SightSeeing(ElementInterface):
    """
    Role: SightSeeing
    Description: Core participant in the Visitor Pattern structure.
    """

    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        visitor.visit_sightseeing(self)