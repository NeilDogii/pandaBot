from typing import Final
import os
import os.path
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
import requests
from customcommands import setCommands
import json


# Retrieving the resource located at the URL 
# and storing it in the file name a.png 


    
def getEmoji(name):
    if os.path.isfile("db/"+str(name)+".png"):
        return 1
    else:
        return 0
    

#url ta url varable e defined ache below token (saved in env file)
#username, avatarurl, ta msg theke copy paste, ar content ta hobe emoji, content will be the image link from json file
def sendWebhook(url, username, avatar_url, content):
    myobj = {
     "username": username,
     "avatar_url": avatar_url,
     "content": content
    }
    x = requests.post(url, json = myobj)





#setup
load_dotenv()
url = os.getenv('WEBHOOK_URL')
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
setCommands(bot)




#events
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return

    username: str = message.author.name
    user_message: str = message.content
    channel: str = message.channel.name

    print(f"User: {username} | Message: {user_message} | Channel: {channel}")

    # await message.channel.send("Hi i am bot")
    await bot.process_commands(message)



#main
def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()

