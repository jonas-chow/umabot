from commands.command import Command
from commands.SetRaceCommand import SetRaceCommand
from commands.StamCalcCommand import StamCalcCommand
from commands.HelpCommand import HelpCommand
from typing import TypedDict

class Parser():
    class Commands(TypedDict):
        name: str
        val: Command

    commands: Commands = {
        SetRaceCommand.COMMAND_WORD : SetRaceCommand(),
        StamCalcCommand.COMMAND_WORD : StamCalcCommand(),
        HelpCommand.COMMAND_WORD : HelpCommand()
    }

    def __init__(self, prefix: str):
        self.prefix = prefix

    def parse(self, message):
        content: str = message.content.strip()

        if not content.startswith(self.prefix):
            return None

        content = content.removeprefix(self.prefix)
        
        words = content.split()

        if len(words) == 0:
            return None

        commandWord = content.split()[0]
        cmd = Parser.commands.get(commandWord)

        if cmd is None:
            return None

        cmd = cmd.copy()
        cmd.set_arguments(content.removeprefix(commandWord), message.author.id)
        if isinstance(cmd, HelpCommand):
            cmd.set_commands(Parser.commands)

        return cmd