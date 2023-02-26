import discord
from discord.ext import commands
from datetime import datetime
import QeueSystem

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!',intents=intents)

serverID = ""
with open('serverID.txt') as f:
    serverID = f.readline()
serverID = int(serverID)

bot.activeQueues = []
bot.newChanBitrate = 9600
bot.oldFartServer = ""
bot.twosMakerChannel = ""
bot.threesMakerChannel = ""
bot.fourssMakerChannel = ""
bot.sixesMakerChannel = ""
bot.twosCategory = ""
bot.threesCategory = ""
bot.foursCategory = ""
bot.sixesCategory = ""
bot.lfgCategory = ""

@bot.event
async def on_ready():
    print(bot.user.name + " is Online...")
    print(datetime.now().strftime('%H:%M:%S %m-%d-%Y'))
    print('------')

    #get guild
    for g in bot.guilds:
        if g.id == serverID:
            print("Found server")
            bot.oldFartServer = g
            oldFartServer = bot.oldFartServer
            bot.newChanBitrate = int(oldFartServer.bitrate_limit)
    
    #create categories
    if not guild_has_category(oldFartServer, "2v2"):
        print("making 2v2 category...")
        await oldFartServer.create_category("2v2")
        
        bot.twosCategory = get_category(oldFartServer, "2v2")
         #create temp vc makers
        await oldFartServer.create_voice_channel("Create new 2v2",category=bot.twosCategory)

    #create 3v3 category
    if not guild_has_category(oldFartServer, "3v3"):
        print("making 3v3 category...")
        await oldFartServer.create_category("3v3")
        
        bot.threesCategory = get_category(oldFartServer, "3v3")
         #create temp vc makers
        await oldFartServer.create_voice_channel("Create new 3v3",category=bot.threesCategory)

    #create 4v4 category
    if not guild_has_category(oldFartServer, "4v4"):
        print("making 4v4 category...")
        await oldFartServer.create_category("4v4")
        
        bot.foursCategory = get_category(oldFartServer, "4v4")
         #create temp vc makers
        await oldFartServer.create_voice_channel("Create new 4v4",category=bot.foursCategory)

    #create 6mans category
    if not guild_has_category(oldFartServer, "6mans"):
        print("making 6mans category...")
        await oldFartServer.create_category("6mans")
        
        bot.sixesCategory = get_category(oldFartServer, "6mans")
         #create temp vc makers
        await oldFartServer.create_voice_channel("Create new 6mans",category=bot.sixesCategory)

    #create LFG category
    if not guild_has_category(oldFartServer, "LFG"):
        print("making LFG category...")
        await oldFartServer.create_category("LFG")
        bot.lfgCategory = get_category(oldFartServer, "LFG")


    #get categories
    bot.twosCategory = get_category(oldFartServer, "2v2")
    bot.threesCategory = get_category(oldFartServer, "3v3")
    bot.foursCategory = get_category(oldFartServer, "4v4")
    bot.sixesCategory = get_category(oldFartServer, "6mans")
    bot.lfgCategory = get_category(oldFartServer, "LFG")
    #get creator channels
    for c in oldFartServer.channels:
        if c.name == "Create new 2v2":
            bot.twosMakerChannel = c
        if c.name == "Create new 3v3":
            bot.threesMakerChannel = c
        if c.name == "Create new 4v4":
            bot.foursMakerChannel = c
        if c.name == "Create new 6mans":
            bot.sixesMakerChannel = c

@bot.event
async def on_voice_state_update(member, before, after):
    #delete any empty VCs that we are making
    if before.channel != None and "Max #" in before.channel.name:
        if len(before.channel.members) == 0:
            await before.channel.delete()
    
    if after.channel == bot.twosMakerChannel:
        #create 2 max VC
        cpos = bot.twosMakerChannel.position + 1
        await create_custom_channel("2 Max", cpos, bot.twosCategory,2,member)

    if after.channel == bot.threesMakerChannel:
        #create 3 max VC
        cpos = bot.threesMakerChannel.position + 1
        await create_custom_channel("3 Max", cpos, bot.threesCategory,3,member)
        
    if after.channel == bot.foursMakerChannel:
        #create 4 max VC
        cpos = bot.foursMakerChannel.position + 1
        await create_custom_channel("4 Max", cpos, bot.foursCategory,4,member)

    if after.channel == bot.sixesMakerChannel:
        #create 6 max VC
        cpos = bot.sixesMakerChannel.position + 1
        await create_custom_channel("6 Max", cpos, bot.sixesCategory,6,member)

@bot.event
async def on_message(msg):
    await bot.process_commands(msg)
    if msg.author.id == bot.user.id:
        if "LFG" in msg.content:
            qMax_index = msg.content.find("Game Mode: ")
            qMax = msg.content[qMax_index+11:qMax_index+12]
            QeueSystem.create_new_queue(msg.id,qMax,bot.activeQueues)

@bot.event
async def on_raw_reaction_add(payload):
    if QeueSystem.is_queue_message(payload.message_id,bot.activeQueues):
        #TODO handle queue

        #get this message
        mChan = await bot.oldFartServer.fetch_channel(payload.channel_id)
        qMessage = await mChan.fetch_message(payload.message_id)
        
        #get the queue object
        for q in bot.activeQueues:
            if q.id == payload.message_id:
                queueData = q

        #get the reactions to the message
        users = set()
        for reaction in qMessage.reactions:
            async for user in reaction.users():
                users.add(user)
        #print(f"users: {', '.join(user.name for user in users)}")
        #print(users)
         
        #compare the number to the max for this queue
        #if the number of reactors is high enough DM each user
        if len(users) == int(queueData.maxPlayers):
            print("max players achieved!")
            for user in users:
                await user.send("Queue Pop! Head on over to RLOF and join your party in VC if you have not already!")
                #TODO create a reserverd VC that only these players can join and send them a direct invite link to that VC instead of this message

async def create_custom_channel(cName, position, category, userLimit, player):
    cnum = 1
    cpos = position
    guild = bot.oldFartServer
    for c in guild.channels:
        if c != None and cName in c.name:
            await c.edit(name = cName +" #" + str(cnum))
            cnum = cnum+1
            cpos = cpos +1
    await guild.create_voice_channel(cName + " #" + str(cnum), position=cpos, category=category, bitrate = bot.newChanBitrate, user_limit=userLimit)
    #pull user into new VC
    for c in guild.channels:
        if c != None and c.name == cName + " #" + str(cnum):
            await player.move_to(c)


def guild_has_category(guild, cat):
    for c in guild.categories:
        if c.name == cat:
            return True
    print("didnt find it")
    return False

def get_category(guild, cat):
    for c in guild.categories:
        if c.name == cat:
            return c
    return


######## Start of custom commands##################################################

#LFG MAKER PRE ALPHA
@bot.command()
async def LFG(ctx, maxPlayers):
    if not maxPlayers.isdigit():
        await ctx.send("Please enter a valid number between 1 and 6")
        return
    if int(maxPlayers) > 6 or int(maxPlayers) < 1:
        await ctx.send("Please enter a valid number between 1 and 6")
        return
    guild = ctx.guild
    player = ctx.author
    rank = QeueSystem.get_player_rank(player)
    reg = QeueSystem.get_player_region(player)

    await ctx.send("```LFG: \nRank: " + rank + "\nRegion: " + reg + "\nGame Mode: " + maxPlayers + "s\nReact to join Queue...```"  )

######## END OF COMMANDS ##########################################################


with open('token.txt') as f:
    TOKEN = f.readline()

bot.run(TOKEN)




















#@bot.event
#async def on_member_join(member):
#    # channel to print to
#    printChan = bot.get_channel(12345679)
#    await printChan.send( "Welcome " + member.mention + " Please head over to " + printChan.mention + " to set up your profile")



# user does some command like "!LFG Diamond2 2v2 VC" (need to think of a way to make this more user friendly)
#bot creates voice channel max 2/3 based on mode selected.
#bot pulls user into VC
#bot posts link to channel in LFG chat + info about the LFG




#### REMEMBER if you add on message you need to include "await bot.process_commands(message)"
