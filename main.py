from typing import Final
import os
import os.path
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
import urllib.request
from PIL import Image 

# Retrieving the resource located at the URL 
# and storing it in the file name a.png 

def addEmoji(name, url):
    if os.path.isfile("db/"+str(name)+".png"):
        return 0
    else:
        urllib.request.urlretrieve(url, "db/"+str(name)+".png")
        return 1
    
def getEmoji(name):
    if os.path.isfile("db/"+str(name)+".png"):
        return 1
    else:
        return 0
    
def resize_image(imagePath,savePath):
    img = Image.open(imagePath)
    img = img.resize((32,32))
    img.save(savePath)



#setup
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


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

    await message.channel.send("Hi i am bot")
    # await bot.process_commands(message)



#main
def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()

