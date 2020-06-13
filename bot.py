import discord, bottoken
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
            embed = await embeds.user_join_embed(client, member)
            await channel.send(embed=embed)
            print("[MEMBER JOIN] " + str(member) + " has joined: " + member.guild.name + " (" + str(member.guild.id) + ")")


# Log user leaving
@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == log_channel:
            embed = await embeds.user_leave_embed(client, member)
            await channel.send(embed=embed)
            print("[MEMBER LEAVE] " + str(member) + " has left: " + member.guild.name + " (" + str(member.guild.id) + ")")


# Log user bans
@client.event
async def on_member_ban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            banreason = await guild.fetch_ban(user)
            embed = await embeds.user_banned_embed(client, user, banreason)
            await channel.send(embed=embed)
            print("[MEMBER BAN] " + str(user) + " has been banned from: " + guild.name + " (" + str(guild.id) + ")" + " for reason: " + str(banreason.reason))


# Log user unbans
@client.event
async def on_member_unban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            embed = await embeds.user_unbanned_embed(client, user)
            await channel.send(embed=embed)
            print("[MEMBER UNBAN] " + str(user) + " has been unbanned from: " + guild.name + " (" + str(guild.id) + ")")


# Log when user changes nickname
@client.event
async def on_member_update(before, after):
    for channel in after.guild.channels:
        if str(channel) == log_channel:
            if before.nick != after.nick:
                embed = await embeds.user_aliaschange_embed(client, before, after)
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
                        embed = await embeds.user_userupdate_embed(client, before, after)
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
            if ctx.message.author == member:
                embed = await embeds.error_target_self_embed(client, member, "ban")
                await ctx.send(embed=embed)
                break
            if member is None:
                embed = await embeds.error_target_none_embed(client, ctx, "ban", ".ban @USER REASON")
                await ctx.send(embed=embed)
                break
            try:
                await ctx.guild.ban(member, reason=reason)
                embed = await embeds.ban_user_embed(client, ctx, member, reason)
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[BANNED MEMBER] " + str(ctx.message.author) + " has banned: " + str(member) + " in: " + str(ctx.guild) + " using CheeseBot for reason: " + str(reason))
            except discord.errors.Forbidden:
                embed = await embeds.error_insufficient_permissions_embed(client, member, "ban")
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[INSUFFICENT PERMISSIONS] CheeseBot does not have sufficient permissions to ban: " + str(member) + " in: " + str(ctx.guild))
    if nopermissions:
        embed = await embeds.error_unauthorized_use_embed(client, ctx)
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
                embed = await embeds.error_target_self_embed(client, member, "kick")
                await ctx.send(embed=embed)
                break
            if member is None:
                embed = await embeds.error_target_none_embed(client, ctx, "kick", ".kick @USER REASON")
                await ctx.send(embed=embed)
                break
            try:
                await ctx.guild.kick(member, reason=reason)
                embed = await embeds.kick_user_embed(client, ctx, member, reason)
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[KICKED MEMBER] " + str(ctx.message.author) + " has kicked: " + str(member) + " in: " + str(ctx.guild) + " using CheeseBot for reason: " + str(reason))
            except discord.errors.Forbidden:
                embed = await embeds.error_insufficient_permissions_embed(client, member, "kick")
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[INSUFFICENT PERMISSIONS] CheeseBot does not have sufficient permissions to kick: " + str(member) + " in: " + str(ctx.guild))
    if nopermissions:
        embed = await embeds.error_unauthorized_use_embed(client, ctx)
        await ctx.send(embed=embed)
        for channel in ctx.guild.channels:
            if str(channel) == log_channel:
                await channel.send(embed=embed)
        print("[UNAUTHROIZED USE] " + str(ctx.message.author) + " tried to use CheeseBot moderation commands in: " + str(ctx.guild) + " without proper permissions")


client.run(bottoken.get_token())
