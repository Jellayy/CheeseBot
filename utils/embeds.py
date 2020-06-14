import discord

async def member_join(client, member):
    embed = discord.Embed(
        color=discord.Color.green(),
        title="Member Join",
        description=f"{member.mention} **has joined the server**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def member_remove(client, member):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Member Leave",
        description=f"{member.mention} **has left the server**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def member_banned(client, user, banreason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Member Banned",
        description=f"{user.mention} **has been banned from the server for reason:** {banreason.reason}"
    )
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def member_unbanned(client, user):
    embed = discord.Embed(
        color=discord.Color.green(),
        title="Member Unbanned",
        description=f"{user.mention} **has been unbanned from the server**"
    )
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def member_alias_change(client, before, after):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title="Member Update",
        description=f"{after.mention} **has changed their alias from** {before.nick} **to** {after.nick}"
    )
    embed.set_author(name=str(before), icon_url=before.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def member_username_change(client, before, after):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title="Member Update",
        description=f"{after.mention} **has changed their username from** {str(before)} **to** {str(after)}"
    )
    embed.set_author(name=str(before), icon_url=before.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def member_banned_command(client, ctx, member, reason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Banned Member",
        description=f"{ctx.message.author.mention} **has banned** {member.mention} **for reason** {reason}"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def member_kicked_command(client, ctx, member, reason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Kicked Member",
        description=f"{ctx.message.author.mention} **has kicked** {member.mention} **for reason** {reason}"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def message_deleted(client, message):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Message Deleted",
        description=f"**Author: **{message.author.mention}\n**Message: **{message.content}"
    )
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def message_edited(client, before, after):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Message Edited",
        description=f"**Before: **{before.content}\n**After: **{after.content}"
    )
    embed.set_author(name=str(after.author), icon_url=after.author.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def vote_kick(client, ctx, member, reason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Vote Kick",
        description=f"{ctx.message.author.mention} **has started a vote to kick** {member.mention} **for reason** {reason}**. React below to vote! Polling will end in one minute!**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def vote_kick_win(client, member, reason):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Vote Decision: **KICK**",
        description=f"**The people have spoken!** {member.mention} **shall be kicked for** {reason}!"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def vote_kick_lose(client, member):
    embed = discord.Embed(
        color=discord.Color.green(),
        title="Vote Decision: **STAY**",
        description=f"**The people have spoken!** {member.mention} **is not guilty!**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_target_self(client, member, action):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**You can't {action} yourself**"
    )
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_target_none(client, ctx, action, usage):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**You must choose someone to {action}**\n\nUsage: `{usage}`"
    )
    embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_insufficient_permissions(client, member, action):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Error",
        description=f"**CheeseBot does not have sufficient permissions to {action}** {member.mention}"
    )
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)

    return embed

async def error_unauthorized_use(client, ctx):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Unauthroized Use",
        description=f"{ctx.message.author.mention} **does not have sufficient permissions to use CheeseBot moderation commands**"
    )
    embed.set_footer(text="CheeseBot", icon_url=client.user.avatar_url)
    embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar_url)

    return embed
