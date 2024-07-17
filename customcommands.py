from discord import File
from discord.ext import commands
import json
from imageresize import resize_image
from requests import get
import os

filepath: str = "db.json"
db = json.load(open(filepath))
prefix = "/"


def setCommands(bot):
    @bot.command(name="emoji")
    async def emoji(ctx):
        try:
            print(ctx.command)
            name = emojiName(ctx.message.content,str(ctx.command))
            print(name)
            await ctx.message.delete()
            if ctx.message.reference:
                replyEmoji(ctx,name)
            else:
                await ctx.send(db[name])
        except:
            await ctx.send("Invalid emoji name")
    
    @bot.command(name="addEmoji")
    async def addEmoji(ctx):
        name = emojiName(ctx.message.content,str(ctx.command))
        if not name or valid(name):
            await ctx.reply("Invalid name")
            return
        if name in db:
            await ctx.reply("Emoji name already exists")
            return
        if len(ctx.message.attachments) <= 0:
            await ctx.reply("No attachment provided")
            return 
        
        emoji_path=downloadEmoji(ctx.message.attachments[0].url,name)
        if emoji_path:
            emoji = await ctx.send(file=File(emoji_path))
            emoji = emoji.attachments[0].url
            db[name] = emoji
            json.dump(db, open(filepath,"w"),indent=4)
            os.remove(emoji_path)
        else:
            await ctx.send("Invalid attachment")
            return
        
        await ctx.reply("Emoji added!")
        
async def replyEmoji(ctx,name):
    message = await ctx.fetch_message(ctx.message.reference.message_id)
    await message.reply(db[name])
    
def downloadEmoji(url,name):
    temp_filepath = f"temp/{name}.png"
    response = get(url)
    if response.status_code == 200:
        with open(temp_filepath, 'wb') as f:
            f.write(response.content)
        resize_image(temp_filepath,temp_filepath)
        return temp_filepath
    else:
        return None
        
def valid(name):
    if " " in name or "/" in name or "\\" in name:
        return False

def emojiName(name,command):
    res = name[len(prefix)+len(command):].strip()
    res= "".join([char.lower() if char.isalpha() else char for char in res])
    return res