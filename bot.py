import discord
import bottoken
import typing
import time
from discord.ext import commands

client = commands.Bot(command_prefix='.')

# Is the bot working?
@client.event
async def on_ready():
    print("bot is ready")

# Ping
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! ({round(client.latency * 1000)}ms)")

# Spam cannons

# Stores author of last message sent at all times
lastmessageauthor = ""
@client.event
async def on_message(message):
    global lastmessageauthor
    lastmessageauthor = message.author
    await client.process_commands(message)

@client.command()
async def cannon(message, user, frequency: typing.Optional[int] = 100):
    # embeds
    embed = discord.Embed(
        color=discord.Color.red()
    )
    embed.add_field(name="SPAM CANNONS", value=("You have chosen to fire upon " + user + " " + str(frequency) + " times or until they respond"))
    embed.add_field(name="Firing in", value="10 seconds", inline=False)
    cancelembed = discord.Embed(
        color=discord.Color.green()
    )
    cancelembed.add_field(name="SPAM CANNONS", value="Spamming cancelled")

    # print initial embed
    await message.channel.send(embed=embed)

    # wait alotted time
    time.sleep(10)

    # unleashes the cannons
    for x in range(0, frequency):
        if lastmessageauthor == user:
            await message.channel.send(user)
        else:
            await message.channel.send(embed=cancelembed)
            break

# handles cannon command syntax error
@cannon.error
async def cannon_error(ctx):
    embed = discord.Embed(
        color=discord.Color.red()
    )
    embed.add_field(name="SPAM CANNONS: PROPER SYNTAX", value=".cannon [USER] [# OF MESSAGES] [WAIT TIME]")
    await ctx.send(embed=embed)


client.run(bottoken.get_token())
