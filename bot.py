import discord
import bottoken
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("bot is ready")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! ({round(client.latency * 1000)}ms)")


client.run(bottoken.get_token())
