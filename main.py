from commands.CommandException import CommandException
from discord import Client, Game
from commands.parser import Parser
from os import getenv
from logging import INFO, getLogger, log

class UmaBot(Client):
    def __init__(self, dbUrl):
        super().__init__()
        self.parser = Parser("!")
        self.dbUrl = dbUrl

    async def on_ready(self):
        await self.change_presence(activity=Game(name="!help"))

    async def on_message(self,message):
        if self.is_ws_ratelimited():
            log(INFO, "rate limited!")
            return

        command = self.parser.parse(message)

        if command is None:
            return

        await message.add_reaction('✅')
        
        try:
            response = command.execute(self.dbUrl)
        except CommandException as e:
            response = str(e)
        except Exception as e:
            log(INFO, message.content + "raised: " + str(e))
            response = 'Something went wrong >//<'

        await message.channel.send(response)

def main():
    logger = getLogger()
    logger.setLevel(INFO)

    discordKey = getenv('DISCORD_KEY')
    dbUrl = getenv('DATABASE_URL')

    bot = UmaBot(dbUrl)
    bot.run(discordKey)

if __name__ == "__main__":
    main()