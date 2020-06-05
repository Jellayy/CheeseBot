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

# Handles stopping of the spam cannons
beingspammed = ""
keepspamming = True
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
        return
    lastmessageauthor = message.author.mention
    lastmessageauthor = lastmessageauthor.replace('!', '')

    if lastmessageauthor == beingspammed:
        global keepspamming
        keepspamming = False

    await client.process_commands(message)

@client.command()
async def cannon(message, user, frequency: typing.Optional[int] = 100):
    # I have to do this because discord api sux
    user = user.replace('!', '')
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
    print(user)

    # give user being spammed to stop spamming function
    global keepspamming, beingspammed
    keepspamming = True
    beingspammed = user

    # print initial embed
    await message.channel.send(embed=embed)

    # wait alotted time
    time.sleep(10)

    # unleashes the cannons
    for x in range(0, frequency):
        if keepspamming:
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
