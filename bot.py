import asyncio
import bottoken
import discord
from discord.ext import commands

import utils.embeds as embeds

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
            embed = await embeds.member_join(client, member)
            await channel.send(embed=embed)
            print("[MEMBER JOIN] " + str(member) + " has joined: " + member.guild.name + " (" + str(member.guild.id) + ")")


# Log user leaving
@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == log_channel:
            embed = await embeds.member_remove(client, member)
            await channel.send(embed=embed)
            print("[MEMBER LEAVE] " + str(member) + " has left: " + member.guild.name + " (" + str(member.guild.id) + ")")


# Log user bans
@client.event
async def on_member_ban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            banreason = await guild.fetch_ban(user)
            embed = await embeds.member_banned(client, user, banreason)
            await channel.send(embed=embed)
            print("[MEMBER BAN] " + str(user) + " has been banned from: " + guild.name + " (" + str(guild.id) + ")" + " for reason: " + str(banreason.reason))


# Log user unbans
@client.event
async def on_member_unban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            embed = await embeds.member_unbanned(client, user)
            await channel.send(embed=embed)
            print("[MEMBER UNBAN] " + str(user) + " has been unbanned from: " + guild.name + " (" + str(guild.id) + ")")


# Log when user changes nickname
@client.event
async def on_member_update(before, after):
    for channel in after.guild.channels:
        if str(channel) == log_channel:
            if before.nick != after.nick:
                embed = await embeds.member_alias_change(client, before, after)
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
                        embed = await embeds.member_username_change(client, before, after)
                        await channel.send(embed=embed)
                        print("[MEMBER UPDATE] " + str(before) + " has changed their username to: " + str(after))

# Log message deletions
@client.event
async def on_message_delete(message):
    for channel in message.guild.channels:
        if str(channel) == log_channel:
            embed = await embeds.message_deleted(client, message)
            await channel.send(embed=embed)
            print("[MESSAGE DELETED] in: " + str(message.guild) + " Author: " + str(message.author) + " | Message: " + str(message.content))


# Log message edits
@client.event
async def on_message_edit(before, after):
    if str(before.content) != str(after.content):
        for channel in after.guild.channels:
            if str(channel) == log_channel:
                embed = await embeds.message_edited(client, before, after)
                await channel.send(embed=embed)
                print("[MESSAGE EDITED] in: " + str(after.guild) + " by: " + str(after.author) + " | Before: " + str(before.content) + " After: " + str(after.content))

########################################################################################################################
# Moderation
########################################################################################################################
# Role needed to use moderation commands
mod_role = "HackingApChem"

# Ban users
@client.command()
async def ban(ctx, member: discord.User = None, *, reason=None):
    nopermissions = True
    for role in ctx.message.author.roles:
        if str(role) == mod_role:
            nopermissions = False
            if ctx.message.author == member:
                embed = await embeds.error_target_self(client, member, "ban")
                await ctx.send(embed=embed)
                break
            if member is None:
                embed = await embeds.error_target_none(client, ctx, "ban", ".ban @USER REASON")
                await ctx.send(embed=embed)
                break
            try:
                await ctx.guild.ban(member, reason=reason)
                embed = await embeds.member_banned_command(client, ctx, member, reason)
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[BANNED MEMBER] " + str(ctx.message.author) + " has banned: " + str(member) + " in: " + str(ctx.guild) + " using CheeseBot for reason: " + str(reason))
            except discord.errors.Forbidden:
                embed = await embeds.error_insufficient_permissions(client, member, "ban")
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[INSUFFICENT PERMISSIONS] CheeseBot does not have sufficient permissions to ban: " + str(member) + " in: " + str(ctx.guild))
    if nopermissions:
        embed = await embeds.error_unauthorized_use(client, ctx)
        await ctx.send(embed=embed)
        for channel in ctx.guild.channels:
            if str(channel) == log_channel:
                await channel.send(embed=embed)
                print("[UNAUTHROIZED USE] " + str(ctx.message.author) + " tried to use CheeseBot moderation commands in: " + str(ctx.guild) + " without proper permissions")

# Kick users
@client.command()
async def kick(ctx, member: discord.User = None, *, reason=None):
    nopermissions = True
    for role in ctx.author.roles:
        if str(role) == mod_role:
            nopermissions = False
            if ctx.message.author == member:
                embed = await embeds.error_target_self(client, member, "kick")
                await ctx.send(embed=embed)
                break
            if member is None:
                embed = await embeds.error_target_none(client, ctx, "kick", ".kick @USER REASON")
                await ctx.send(embed=embed)
                break
            try:
                await ctx.guild.kick(member, reason=reason)
                embed = await embeds.member_kicked_command(client, ctx, member, reason)
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[KICKED MEMBER] " + str(ctx.message.author) + " has kicked: " + str(member) + " in: " + str(ctx.guild) + " using CheeseBot for reason: " + str(reason))
            except discord.errors.Forbidden:
                embed = await embeds.error_insufficient_permissions(client, member, "kick")
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[INSUFFICENT PERMISSIONS] CheeseBot does not have sufficient permissions to kick: " + str(member) + " in: " + str(ctx.guild))
    if nopermissions:
        embed = await embeds.error_unauthorized_use(client, ctx)
        await ctx.send(embed=embed)
        for channel in ctx.guild.channels:
            if str(channel) == log_channel:
                await channel.send(embed=embed)
        print("[UNAUTHROIZED USE] " + str(ctx.message.author) + " tried to use CheeseBot moderation commands in: " + str(ctx.guild) + " without proper permissions")

# Vote Kick Users
@client.command()
async def votekick(ctx, member: discord.User = None, *, reason=None):
    if ctx.message.author == member:
        embed = await embeds.error_target_self(client, member, "vote kick")
        await ctx.send(embed=embed)
        return
    if member is None:
        embed = await embeds.error_target_none(client, ctx, "vote kick", ".votekick @USER REASON")
        await ctx.send(embed=embed)
        return
    try:
        embed = await embeds.vote_kick(client, ctx, member, reason)
        options = ['❌', '✅']
        votemessage = await ctx.send(embed=embed)
        for option in options:
            await votemessage.add_reaction(emoji=option)
        await asyncio.sleep(60)
        votemessage = await ctx.fetch_message(votemessage.id)
        counts = {react.emoji: react.count for react in votemessage.reactions}
        winner = max(options, key=counts.get)
        if winner == '✅':
            embed = await embeds.vote_kick_win(client, member, reason)
            await ctx.send(embed=embed)
            for channel in ctx.guild.channels:
                if str(channel) == log_channel:
                    await channel.send(embed=embed)
            await ctx.guild.kick(member, reason=reason)
            print("[VOTE KICKED MEMBER] " + str(ctx.message.author) + " has vote kicked: " + str(member) + " in: " + str(ctx.guild) + " using CheeseBot for reason: " + str(reason))
        else:
            embed = await embeds.vote_kick_lose(client, member)
            await ctx.send(embed=embed)
    except discord.errors.Forbidden:
        embed = await embeds.error_insufficient_permissions(client, member, "votekick")
        await ctx.send(embed=embed)
        for channel in ctx.guild.channels:
            if str(channel) == log_channel:
                await channel.send(embed=embed)
        print("[INSUFFICENT PERMISSIONS] CheeseBot does not have sufficient permissions to votekick: " + str(member) + " in: " + str(ctx.guild))

########################################################################################################################
# Fun Stuff
########################################################################################################################

client.run(bottoken.get_token())
