from discord import File,Embed
from discord.ext import commands
import json
from imageresize import resize_image,resize_gif
from requests import get
import os
import aiohttp
from dotenv import load_dotenv




filepath: str = "db.json"
db = json.load(open(filepath))
prefix = "/"

load_dotenv()
admin = os.getenv('ADMIN_ID')

def setCommands(bot):
    @bot.command(name="e")
    async def emoji(ctx):
        name = emojiName(ctx.message.content,str(ctx.command))
        if name not in db:
            await ctx.reply("Emoji not found")
            return
        
        if ctx.message.reference:
            await replyEmoji(ctx,name)
            await ctx.message.delete()
        else:
            avatar = await fetch_avatar(ctx.message.author.avatar)
            await webhookSend(ctx.channel,ctx.author.nick or ctx.author.name,avatar,db[name])
            await ctx.message.delete()

    
    @bot.command(name="ae")
    async def addEmoji(ctx):
        name = emojiName(ctx.message.content,str(ctx.command))
        
        if not name or invalid(name):
            await ctx.reply("Invalid name")
            return
        if name in db:
            await ctx.reply("Emoji name already exists")
            return
        if len(ctx.message.attachments) <= 0:
            await ctx.reply("No attachment provided")
            return 
        
        
        if ctx.message.attachments[0].filename.endswith('.png'):
            emoji_path=downloadImage(ctx.message.attachments[0].url,name)
        elif ctx.message.attachments[0].filename.endswith('.gif'):
            emoji_path=downloadGif(ctx.message.attachments[0].url,name)
        else:
            await ctx.send("Invalid format (try using .png or .gif)")
            return
        
        if emoji_path:
            emoji = await ctx.send(file=File(emoji_path))
            emoji = emoji.attachments[0].url
            db[name] = emoji
            json.dump(db, open(filepath,"w"),indent=4)
            os.remove(emoji_path)
        else:
            await ctx.send("Invalid attachment")
            return
        
        await ctx.send(f"Emoji added {name}, please don't delete the bot message with image/gif!!")
    
    @bot.command(name="de")
    async def deleteEmoji(ctx):
        if str(ctx.message.author.id) == str(admin):
            name = emojiName(ctx.message.content,str(ctx.command))
            if name in db:
                del db[name]
                json.dump(db, open(filepath,"w"),indent=4)
                await ctx.send(f"Emoji {name} deleted")
            else:
                await ctx.send("Emoji not found")
        else:
            await ctx.send("You are not admin")
        
    @bot.command(name="le")
    async def listEmoji(ctx):
        emojis = ""
        for n,emoji in enumerate(db):
            emojis += f"{n}. {emoji}\n"
        if not emojis:
            await ctx.send("No emojis found")
            return
        await ctx.send(emojis)
        
    @bot.command(name="helpnub")
    async def helpNub(ctx):
        embed = Embed(title="Help",description="Commands for the bot",color=0x00ff00)
        embed.add_field(name="/e <name>",value="Send emoji",inline=False)
        embed.add_field(name="/ae <name> <attachment>",value="Add emoji (.png and .gif only)",inline=False)
        embed.add_field(name="/de <name>",value="Delete emoji (Admin only)",inline=False)
        embed.add_field(name="/le",value="List all emojis",inline=False)
        await ctx.send(embed=embed)    
    
        
async def replyEmoji(ctx,name):
    message = await ctx.fetch_message(ctx.message.reference.message_id)
    await message.reply(db[name])
    await ctx.send(f"-# sent by {ctx.message.author.nick or ctx.message.author.name}")
    
async def webhookSend(channel,username,avatar,emoji):
    webhook = await channel.create_webhook(name=username,avatar=avatar)
    await webhook.send(emoji)
    await webhook.delete()


async def fetch_avatar(avatar_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(str(avatar_url)) as response:
            return await response.read()
    
def downloadImage(url,name):
    temp_filepath = f"temp/{name}.png"
    response = get(url)
    if response.status_code == 200:
        with open(temp_filepath, 'wb') as f:
            f.write(response.content)
        resize_image(temp_filepath,temp_filepath)
        return temp_filepath
    else:
        return None

def downloadGif(url,name):
    temp_filepath = f"temp/{name}.gif"
    response = get(url)
    if response.status_code == 200:
        with open(temp_filepath, 'wb') as f:
            f.write(response.content)
        resize_gif(temp_filepath,temp_filepath)
        return temp_filepath
    else:
        return None
        
def invalid(name):
    if " " in name or "/" in name or "\\" in name or "." in name:
        return True
    return False

def emojiName(name,command):
    res = name[len(prefix)+len(command):].strip()
    res= "".join([char.lower() if char.isalpha() else char for char in res])
    return res
