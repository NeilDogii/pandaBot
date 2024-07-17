from discord import File
from discord.ext import commands
import json
from imageresize import resize_image
from requests import get
import os

filepath: str = "db.json"
db = json.load(open(filepath))



def setCommands(bot):
    @bot.command(name="emoji")
    async def emoji(ctx):
        try:
            name = ctx.message.content[len("/emoji"):].strip().lower()
            await ctx.message.delete()
            if ctx.message.reference:
                replyEmoji(ctx,name)
            else:
                await ctx.send(db[name])
        except:
            await ctx.send("Invalid emoji name")
    
    @bot.command(name="addEmoji")
    async def addEmoji(ctx):
        name = ctx.message.content[len("/addEmoji"):].strip().lower()
        print(name)
        
        if not name:
            await ctx.reply("No emoji name provided")
            return
        if name in db:
            await ctx.reply("Emoji name already exists")
            return
        if len(ctx.message.attachments) <= 0:
            await ctx.reply("No attachment provided")
            return 
        
        emoji=downloadEmoji(ctx.message.attachments[0].url,name)
        print(emoji)
        if emoji:
            await ctx.send(file=File(emoji))
            
        # emoji = ctx.message.attachments[0].url
        # db[name] = emoji
        # json.dump(db, open(filepath,"w"),indent=4)
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
        
