from ..visitor_pattern.element.city import City
from ..visitor_pattern.element.industry import Industry
from ..visitor_pattern.element.sightseeing import SightSeeing

from ..visitor_pattern.visitor.xml_export_visitor import XMLExportVisitor
from ..visitor_pattern.visitor.json_export_visitor import JSONExportVisitor


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CREATE OBJECT STRUCTURE (GRAPH)")
    print("=" * 50)

    graph = [
        City("Hanoi"),
        Industry("AI Zone"),
        SightSeeing("Old Quarter"),
    ]

    print()

    print("=" * 50)
    print("CREATE VISITORS")
    print("=" * 50)

    xml_visitor = XMLExportVisitor()
    json_visitor = JSONExportVisitor()

    print()

    print("=" * 50)
    print("RUN VISITOR: XML EXPORT")
    print("=" * 50)

    for node in graph:
        node.accept(xml_visitor)

    print()

    print("=" * 50)
    print("RUN VISITOR: JSON EXPORT")
    print("=" * 50)

    for node in graph:
        node.accept(json_visitor)

    print()

    print("=" * 50)
    print("DONE")
    print("=" * 50)