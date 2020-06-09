import discord, bottoken

client = discord.Client()

########################################################################################################################
# Log Channel
########################################################################################################################
# Set channel name to be used here
log_channel = "log"
log_guild = "Test Server"

# Log user joins
@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == log_channel:
            await channel.send(f"{member.mention} has joined the server")
            print("[MEMBER JOIN] " + str(member) + " has joined: " + member.guild.name + " (" + str(member.guild.id) + ")")

# Log user leaving
@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == log_channel:
            await channel.send(f"{member.mention} has left the server")
            print("[MEMBER LEAVE] " + str(member) + " has left: " + member.guild.name + " (" + str(member.guild.id) + ")")

# Log user bans
@client.event
async def on_member_ban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            banreason = await guild.fetch_ban(user)
            await channel.send(f"{user.mention} has been banned from the server for reason: " + str(banreason.reason))
            print("[MEMBER BAN] " + str(user) + " has been banned from: " + guild.name + " (" + str(guild.id) + ")" + " for reason: " + str(banreason.reason))

# Log user unbans
@client.event
async def on_member_unban(guild, user):
    for channel in guild.channels:
        if str(channel) == log_channel:
            await channel.send(f"{user.mention} has been unbanned from the server")
            print("[MEMBER UNBAN] " + str(user) + " has been unbanned from: " + guild.name + " (" + str(guild.id) + ")")

# Log when user changes nickname
@client.event
async def on_member_update(before, after):
    for channel in after.guild.channels:
        if str(channel) == log_channel:
            if before.nick != after.nick:
                await channel.send(f"{after.mention} has changed their alias from {before.nick} to {after.nick}")
                print("[MEMBER UPDATE] " + str(after) + " has changed their alias in " + str(after.guild.name) + ": " + str(before.nick) + " -> " + str(after.nick))

# Log when user updates username
@client.event
async def on_user_update(before, after):
    for guild in client.guilds:
        if str(guild) == log_guild:
            for channel in guild.channels:
                if str(channel) == log_channel:
                    if str(before) != str(after):
                        await channel.send(f"{after.mention} has changed their username from {str(before)} to {str(after)}")
                        print("[MEMBER UPDATE] " + str(before) + " has changed their username to: " + str(after))


########################################################################################################################
# Stats
########################################################################################################################

@client.event
async def on_message(message):
    if message.author != client.user:
        print("[MESSAGE RECIEVED] " + str(message.author) + ": " + message.content)

client.run(bottoken.get_token())
