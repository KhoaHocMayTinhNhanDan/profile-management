from .visitor_interface import VisitorInterface


class XMLExportVisitor(VisitorInterface):
    """
    Role: XMLExportVisitor
    Description: Core participant in the Xml Export Visitor.Py structure.
    """

    def visit_city(self, city):
        print(f"<city>{city.name}</city>")

    def visit_industry(self, industry):
        print(f"<industry>{industry.name}</industry>")

    def visit_sightseeing(self, sightseeing):
        print(f"<sightseeing>{sightseeing.name}</sightseeing>")