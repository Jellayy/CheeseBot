import discord, bottoken
from discord.ext import commands

client = commands.Bot(command_prefix=".")

########################################################################################################################
# Log Channel
########################################################################################################################
# Configuration
log_channel = "log"
log_guild = "Test Server"

# Log user joins
@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == log_channel:
            embed = discord.Embed(
                color=discord.Color.green(),
                title="Member Join",
                description=f"{member.mention} **has joined the server**"
            )
            embed.set_author(name=str(member), icon_url=member.avatar_url)
            embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
            await channel.send(embed=embed)
            print("[MEMBER JOIN] " + str(member) + " has joined: " + member.guild.name + " (" + str(member.guild.id) + ")")

# Log user leaving
@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == log_channel:
            embed = discord.Embed(
                color=discord.Color.red(),
                title="Member Leave",
                description=f"{member.mention} **has left the server**"
            )
            embed.set_author(name=str(member), icon_url=member.avatar_url)
            embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
            await channel.send(embed=embed)
            print("[MEMBER LEAVE] " + str(member) + " has left: " + member.guild.name + " (" + str(member.guild.id) + ")")

# Log user bans
@client.event
async def on_member_ban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            banreason = await guild.fetch_ban(user)
            embed = discord.Embed(
                color=discord.Color.red(),
                title="Member Banned",
                description=f"{user.mention} **has been banned from the server for reason:** {banreason.reason}"
            )
            embed.set_author(name=str(user), icon_url=user.avatar_url)
            embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
            await channel.send(embed=embed)
            print("[MEMBER BAN] " + str(user) + " has been banned from: " + guild.name + " (" + str(guild.id) + ")" + " for reason: " + str(banreason.reason))

# Log user unbans
@client.event
async def on_member_unban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            embed = discord.Embed(
                color=discord.Color.green(),
                title="Member Unbanned",
                description=f"{user.mention} **has been unbanned from the server**"
            )
            embed.set_author(name=str(user), icon_url=user.avatar_url)
            embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
            await channel.send(embed=embed)
            print("[MEMBER UNBAN] " + str(user) + " has been unbanned from: " + guild.name + " (" + str(guild.id) + ")")

# Log when user changes nickname
@client.event
async def on_member_update(before, after):
    for channel in after.guild.channels:
        if str(channel) == log_channel:
            if before.nick != after.nick:
                embed = discord.Embed(
                    color=discord.Color.blue(),
                    title="Member Update",
                    description=f"{after.mention} **has changed their alias from** {before.nick} **to** {after.nick}"
                )
                embed.set_author(name=str(before), icon_url=before.avatar_url)
                embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
                await channel.send(embed=embed)
                print("[MEMBER UPDATE] " + str(after) + " has changed their alias in " + str(after.guild.name) + ": " + str(before.nick) + " -> " + str(after.nick))

# Log when user updates username
@client.event
async def on_user_update(before, after):
    for guild in client.guilds:
        if str(guild) == log_guild:
            for channel in guild.channels:
                if str(channel) == log_channel:
                    if str(before) != str(after):
                        embed = discord.Embed(
                            color=discord.Color.blue(),
                            title="Member Update",
                            description=f"{after.mention} **has changed their username from** {str(before)} **to** {str(after)}"
                        )
                        embed.set_author(name=str(before), icon_url=before.avatar_url)
                        embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
                        await channel.send(embed=embed)
                        print("[MEMBER UPDATE] " + str(before) + " has changed their username to: " + str(after))

########################################################################################################################
# Moderation
########################################################################################################################
# Role needed to use moderation commands
mod_role = "FUCCN OG"

# Ban users
@client.command()
async def ban(ctx, member: discord.User = None, *, reason=None):
    nopermissions = True
    for role in ctx.message.author.roles:
        if str(role) == mod_role:
            nopermissions = False
            try:
                await ctx.guild.ban(member, reason=reason)
                print("[BANNED MEMBER] " + str(ctx.message.author) + " has banned: " + str(member) + " in: " + str(ctx.guild) + " using CheeseBot for reason: " + str(reason))
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title="Banned Member",
                    description=f"{ctx.message.author.mention} **has banned** {member.mention} **for reason** {reason}"
                )
                embed.set_author(name=str(member), icon_url=member.avatar_url)
                embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
            except discord.errors.Forbidden:
                print("[INSUFFICENT PERMISSIONS] CheeseBot does not have sufficient permissions to ban: " + str(member) + " in: " + str(ctx.guild))
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title="Error",
                    description=f"**CheeseBot does not have sufficient permissions to ban** {member.mention}"
                )
                embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
    if nopermissions:
        print("[UNAUTHROIZED USE] " + str(ctx.message.author) + " tried to use CheeseBot moderation commands in: " + str(ctx.guild) + " without proper permissions")
        embed = discord.Embed(
            color=discord.Color.red(),
            title="Unauthroized Use",
            description=f"{ctx.message.author.mention} **does not have sufficient permissions to use CheeseBot moderation commands**"
        )
        embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
        embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        for channel in ctx.guild.channels:
            if str(channel) == log_channel:
                await channel.send(embed=embed)

########################################################################################################################
# Fun Stuff
########################################################################################################################
# Configurations
# approved_vim_channel = "vim_is_love_vim_is_life"
#
# # Ban people for mentioning VIM outside of the VIM channel
# # VIM channel con be configured under approved_vim_channel
# @client.event
# async def on_message(message):
#     if message.author != client.user:
#         message.content = message.content.lower()
#         if message.content.find("vim") != -1:
#             if str(message.channel) != approved_vim_channel:
#                 print("[HERECY DETECTED] " + str(message.author) + " has been detected mentioning VIM outside of approved channels in: " + str(message.guild))
#                 await message.channel.send("MENTION OF VIM OUTSIDE OF THE VIM CHANNEL IS HERECY AND PUNISHABLE BY DEATH")
#                 try:
#                     await message.guild.ban(message.author, reason="HERECY OF VIM ORIGIN", delete_message_days=0)
#                 except discord.errors.Forbidden:
#                     print("[INSUFFICIENT PERMISSIONS] CheeseBot does not have sufficient permissions to ban: " + str(message.author) + " in: " + str(message.guild))
#                     for channel in message.guild.channels:
#                         if str(channel) == log_channel:
#                             await channel.send(f"CheeseBot does not have sufficient permissions to ban {message.author}")
#
# # Literally just bans Ben's VIM bot
# @client.event
# async def on_message(message):
#     for member in message.guild.members:
#         if str(member).find("VIM") != -1:
#             print(member)
#             await message.guild.ban(member, reason="BOT DEDICATED TO HERECY", delete_message_days=0)

client.run(bottoken.get_token())
