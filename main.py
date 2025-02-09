import json
import os
import os.path
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands

#db setup
temp_folder = 'temp'
json_file = 'db.json'
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)
if not os.path.exists(json_file):
    with open(json_file, 'w') as file:
        json.dump({},file)

from customcommands import setCommands




#setup
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
setCommands(bot)




#events
@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return

    # username: str = message.author.name
    # user_message: str = message.content
    # channel: str = message.channel.name

    # print(f"User: {username} | Message: {user_message} | Channel: {channel}")

    await bot.process_commands(message)



#main
def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()

