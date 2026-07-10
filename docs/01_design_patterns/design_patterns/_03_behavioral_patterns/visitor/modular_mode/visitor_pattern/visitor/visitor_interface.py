from abc import abstractmethod


class VisitorInterface:
    """
    Role: VisitorInterface
    Description: Core participant in the Visitor Interface.Py structure.
    """

    @abstractmethod
    def visit_city(self, city):
        pass

    @abstractmethod
    def visit_industry(self, industry):
        pass

    @abstractmethod
    def visit_sightseeing(self, sightseeing):
        pass