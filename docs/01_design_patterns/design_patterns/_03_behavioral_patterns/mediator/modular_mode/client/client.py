from ..mediator_pattern.mediator.concrete_mediator import (
    ConcreteMediator,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CREATE MEDIATOR")
    print("=" * 50)

    mediator = ConcreteMediator()

    print()

    print("=" * 50)
    print("CHECKBOX EVENT")
    print("=" * 50)

    mediator.checkbox.check()

    print()

    print("=" * 50)
    print("TEXTBOX EVENT")
    print("=" * 50)

    mediator.textbox.input_text(
        "hello mediator"
    )

    print()

    print("=" * 50)
    print("BUTTON EVENT")
    print("=" * 50)

    mediator.button.click()