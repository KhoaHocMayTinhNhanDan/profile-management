from ..command_pattern.receiver.receiver import (
    Receiver,
)

from ..command_pattern.command.concrete_command_a import (
    ConcreteCommandA,
)

from ..command_pattern.command.concrete_command_b import (
    ConcreteCommandB,
)

from ..command_pattern.invoker.invoker import (
    Invoker,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CREATE RECEIVER")
    print("=" * 50)

    receiver = Receiver()

    print()

    print("=" * 50)
    print("CREATE COMMANDS")
    print("=" * 50)

    command_a = ConcreteCommandA(
        receiver
    )

    command_b = ConcreteCommandB(
        receiver
    )

    print("Commands created")

    print()

    print("=" * 50)
    print("INVOKER")
    print("=" * 50)

    invoker = Invoker()

    invoker.add_command(command_a)

    invoker.add_command(command_b)

    invoker.run()