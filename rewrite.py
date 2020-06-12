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
            embed = user_join_embed(member)
            await channel.send(embed=embed)
            print("[MEMBER JOIN] " + str(member) + " has joined: " + member.guild.name + " (" + str(member.guild.id) + ")")


# Log user leaving
@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == log_channel:
            embed = user_leave_embed(member)
            await channel.send(embed=embed)
            print("[MEMBER LEAVE] " + str(member) + " has left: " + member.guild.name + " (" + str(member.guild.id) + ")")


# Log user bans
@client.event
async def on_member_ban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            banreason = await guild.fetch_ban(user)
            embed = user_banned_embed(user, banreason)
            await channel.send(embed=embed)
            print("[MEMBER BAN] " + str(user) + " has been banned from: " + guild.name + " (" + str(guild.id) + ")" + " for reason: " + str(banreason.reason))


# Log user unbans
@client.event
async def on_member_unban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            embed = user_unbanned_embed()
            await channel.send(embed=embed)
            print("[MEMBER UNBAN] " + str(user) + " has been unbanned from: " + guild.name + " (" + str(guild.id) + ")")


# Log when user changes nickname
@client.event
async def on_member_update(before, after):
    for channel in after.guild.channels:
        if str(channel) == log_channel:
            if before.nick != after.nick:
                embed = user_aliaschange_embed(before, after)
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
                        embed = user_userupdate_embed(before, after)
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
                embed = error_target_self_embed(member, "ban")
                await ctx.send(embed=embed)
                break
            if member is None:
                embed = error_target_none_embed(ctx, "ban", ".ban @USER REASON")
                await ctx.send(embed=embed)
                break
            try:
                await ctx.guild.ban(member, reason=reason)
                embed = ban_user_embed(ctx, member, reason)
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[BANNED MEMBER] " + str(ctx.message.author) + " has banned: " + str(member) + " in: " + str(ctx.guild) + " using CheeseBot for reason: " + str(reason))
            except discord.errors.Forbidden:
                embed = error_insufficient_permissions_embed(member, "ban")
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[INSUFFICENT PERMISSIONS] CheeseBot does not have sufficient permissions to ban: " + str(member) + " in: " + str(ctx.guild))
    if nopermissions:
        embed = error_unauthorized_use_embed(ctx)
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
                embed = error_target_self_embed(member, "kick")
                await ctx.send(embed=embed)
                break
            if member is None:
                embed = error_target_none_embed(ctx, "kick", ".kick @USER REASON")
                await ctx.send(embed=embed)
                break
            try:
                await ctx.guild.kick(member, reason=reason)
                embed = kick_user_embed(ctx, member, reason)
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[KICKED MEMBER] " + str(ctx.message.author) + " has kicked: " + str(member) + " in: " + str(ctx.guild) + " using CheeseBot for reason: " + str(reason))
            except discord.errors.Forbidden:
                embed = error_insufficient_permissions_embed(member, "kick")
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:
                    if str(channel) == log_channel:
                        await channel.send(embed=embed)
                print("[INSUFFICENT PERMISSIONS] CheeseBot does not have sufficient permissions to kick: " + str(member) + " in: " + str(ctx.guild))
    if nopermissions:
        embed = error_unauthorized_use_embed(ctx)
        await ctx.send(embed=embed)
        for channel in ctx.guild.channels:
            if str(channel) == log_channel:
                await channel.send(embed=embed)
        print("[UNAUTHROIZED USE] " + str(ctx.message.author) + " tried to use CheeseBot moderation commands in: " + str(ctx.guild) + " without proper permissions")


########################################################################################################################
# Embeds
########################################################################################################################

async def user_join_embed(member):
    embed = discord.Embed(
        color=discord.Color.green(),
        title="Member Join",
        description=f"{member.mention} **has joined the server**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_leave_embed(member):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Member Leave",
        description=f"{member.mention} **has left the server**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_banned_embed(user, banreason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Member Banned",
        description=f"{user.mention} **has been banned from the server for reason:** {banreason.reason}"
    )
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_unbanned_embed(user):
    embed = discord.Embed(
        color=discord.Color.green(),
        title="Member Unbanned",
        description=f"{user.mention} **has been unbanned from the server**"
    )
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_aliaschange_embed(before, after):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title="Member Update",
        description=f"{after.mention} **has changed their alias from** {before.nick} **to** {after.nick}"
    )
    embed.set_author(name=str(before), icon_url=before.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_userupdate_embed(before, after):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title="Member Update",
        description=f"{after.mention} **has changed their username from** {str(before)} **to** {str(after)}"
    )
    embed.set_author(name=str(before), icon_url=before.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def ban_user_embed(ctx, member, reason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Banned Member",
        description=f"{ctx.message.author.mention} **has banned** {member.mention} **for reason** {reason}"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def kick_user_embed(ctx, member, reason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Kicked Member",
        description=f"{ctx.message.author.mention} **has kicked** {member.mention} **for reason** {reason}"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_target_self_embed(member, action):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**You can't {action} yourself**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_target_none_embed(ctx, action, usage):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**You must choose someone to {action}**\n\nUsage: `{usage}`"
    )
    embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_insufficient_permissions_embed(member, action):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**CheeseBot does not have sufficient permissions to {action}** {member.mention}"
    )
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_unauthorized_use_embed(ctx):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Unauthroized Use",
        description=f"{ctx.message.author.mention} **does not have sufficient permissions to use CheeseBot moderation commands**"
    )
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
    embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar_url)

    return embed


client.run(bottoken.get_token())
