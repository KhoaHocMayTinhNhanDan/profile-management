from ..memento_pattern.originator.originator import (
    Originator,
)

from ..memento_pattern.caretaker.caretaker import (
    Caretaker,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CREATE ORIGINATOR")
    print("=" * 50)

    originator = Originator(
        "STATE_1"
    )

    caretaker = Caretaker(
        originator
    )

    print()

    print(originator.show_state())

    print()

    # =====================================================
    # SAVE SNAPSHOT
    # =====================================================

    caretaker.backup()

    originator.do_something(
        "STATE_2"
    )

    caretaker.backup()

    originator.do_something(
        "STATE_3"
    )

    caretaker.backup()

    originator.do_something(
        "STATE_4"
    )

    print()

    print("=" * 50)
    print("CURRENT STATE")
    print("=" * 50)

    print(originator.show_state())

    print()

    print("=" * 50)
    print("SHOW HISTORY")
    print("=" * 50)

    caretaker.show_history()

    print()

    print("=" * 50)
    print("UNDO")
    print("=" * 50)

    caretaker.undo()

    print(
        originator.show_state()
    )

    print()

    caretaker.undo()

    print(
        originator.show_state()
    )