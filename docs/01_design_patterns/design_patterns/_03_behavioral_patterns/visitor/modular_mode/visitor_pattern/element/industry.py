from .element_interface import ElementInterface


class Industry(ElementInterface):
    """
    Role: Industry
    Description: Core participant in the Visitor Pattern structure.
    """

    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        visitor.visit_industry(self)