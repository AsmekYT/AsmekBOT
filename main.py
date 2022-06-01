import discord
from discord.ext import commands

client = commands.Bot(command_prefix= "a!")
client.remove_command("help")


@client.command()
async def help(ctx):
    await ctx.send("Prace nad botem trwają")



client.run("OTUzMzkwMTAxODkzODkwMTc5.GnwHzI.9AoFbin4furyoj6NjiH6ok1Rhk_ghwEC5xjknI")