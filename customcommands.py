import discord
from discord.ext import commands
import json

filepath: str = "db.json"
db = json.load(open(filepath))



def setCommands(bot):
    @bot.command(name="emoji")
    async def emoji(ctx):
        try:
            name = ctx.message.content.split(" ")[1]
            await ctx.message.delete()
            if ctx.message.reference:
                message = await ctx.fetch_message(ctx.message.reference.message_id)
                await message.reply(db[name])
            else:
                await ctx.send(db[name])
        except:
            await ctx.send("Invalid emoji name")
    