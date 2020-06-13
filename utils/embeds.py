import discord

async def user_join_embed(client, member):
    embed = discord.Embed(
        color=discord.Color.green(),
        title="Member Join",
        description=f"{member.mention} **has joined the server**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_leave_embed(client, member):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Member Leave",
        description=f"{member.mention} **has left the server**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_banned_embed(client, user, banreason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Member Banned",
        description=f"{user.mention} **has been banned from the server for reason:** {banreason.reason}"
    )
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_unbanned_embed(client, user):
    embed = discord.Embed(
        color=discord.Color.green(),
        title="Member Unbanned",
        description=f"{user.mention} **has been unbanned from the server**"
    )
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_aliaschange_embed(client, before, after):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title="Member Update",
        description=f"{after.mention} **has changed their alias from** {before.nick} **to** {after.nick}"
    )
    embed.set_author(name=str(before), icon_url=before.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def user_userupdate_embed(client, before, after):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title="Member Update",
        description=f"{after.mention} **has changed their username from** {str(before)} **to** {str(after)}"
    )
    embed.set_author(name=str(before), icon_url=before.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def ban_user_embed(client, ctx, member, reason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Banned Member",
        description=f"{ctx.message.author.mention} **has banned** {member.mention} **for reason** {reason}"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def kick_user_embed(client, ctx, member, reason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Kicked Member",
        description=f"{ctx.message.author.mention} **has kicked** {member.mention} **for reason** {reason}"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_target_self_embed(client, member, action):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**You can't {action} yourself**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_target_none_embed(client, ctx, action, usage):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**You must choose someone to {action}**\n\nUsage: `{usage}`"
    )
    embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_insufficient_permissions_embed(client, member, action):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**CheeseBot does not have sufficient permissions to {action}** {member.mention}"
    )
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_unauthorized_use_embed(client, ctx):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Unauthroized Use",
        description=f"{ctx.message.author.mention} **does not have sufficient permissions to use CheeseBot moderation commands**"
    )
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
    embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar_url)

    return embed
