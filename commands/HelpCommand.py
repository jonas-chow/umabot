from commands.command import Command

# to be replaced with a link to github page
class HelpCommand(Command):
    COMMAND_WORD = "help"
    FORMAT = "help `command`"

    def copy(self):
        return HelpCommand()

    def set_arguments(self, arguments: str, _: int):
        self.arguments = arguments.strip()

    def set_commands(self, commands):
        self.commands = commands


    def execute(self, _):
        cmd = self.commands.get(self.arguments)

        if cmd is None:
            return 'Possible commands: ' + ', '.join(self.commands.keys()) + '\n' + \
                '`!help command` for more info on each command, or try them out yourself!'
        else:
            return cmd.FORMAT