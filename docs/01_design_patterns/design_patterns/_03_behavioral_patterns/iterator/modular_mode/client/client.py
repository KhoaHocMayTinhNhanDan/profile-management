# =========================================================
# File:
# iterator/modular_mode/client/client.py
# =========================================================

from ..iterator_pattern.collection.concrete_collection import (
    ConcreteCollection,
)

from ..iterator_pattern.iterator.reverse_iterator import (
    ReverseIterator,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CREATE COLLECTION")
    print("=" * 50)

    collection = ConcreteCollection()

    collection.add_item("BTCUSDT")

    collection.add_item("ETHUSDT")

    collection.add_item("SOLUSDT")

    collection.add_item("BNBUSDT")

    print()

    print("=" * 50)
    print("FORWARD ITERATOR")
    print("=" * 50)

    iterator = (
        collection.create_iterator()
    )

    while iterator.has_next():

        print(iterator.next())

    print()

    print("=" * 50)
    print("RESET ITERATOR")
    print("=" * 50)

    iterator.reset()

    while iterator.has_next():

        print(iterator.next())

    print()

    print("=" * 50)
    print("REVERSE ITERATOR")
    print("=" * 50)

    reverse_iterator = ReverseIterator(
        collection
    )

    while reverse_iterator.has_next():

        print(reverse_iterator.next())