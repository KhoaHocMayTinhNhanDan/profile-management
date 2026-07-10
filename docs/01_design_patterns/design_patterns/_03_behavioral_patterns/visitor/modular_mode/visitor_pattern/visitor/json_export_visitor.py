from .visitor_interface import VisitorInterface


class JSONExportVisitor(VisitorInterface):
    """
    Role: JSONExportVisitor
    Description: Core participant in the Json Export Visitor.Py structure.
    """

    def visit_city(self, city):
        print({"city": city.name})

    def visit_industry(self, industry):
        print({"industry": industry.name})

    def visit_sightseeing(self, sightseeing):
        print({"sightseeing": sightseeing.name})