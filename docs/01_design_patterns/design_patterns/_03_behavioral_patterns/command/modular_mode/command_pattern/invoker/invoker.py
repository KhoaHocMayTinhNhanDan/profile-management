class Invoker:
    """
    Role: Invoker
    Description: Core participant in the Command Pattern structure.
    """

    def __init__(self):

        self._commands = []

    def add_command(self, command):

        self._commands.append(command)

    def run(self):

        for command in self._commands:

            print(command.execute())