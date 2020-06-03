import discord
import bottoken
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("bot is ready")

client.run(bottoken.get_token())
