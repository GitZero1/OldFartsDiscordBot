import discord
from discord.ext import commands
from datetime import datetime
#import QeueSystem

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
bot.customCreators = []

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
            #set the new channel bitrate to whatever the max rate is for the server
            bot.newChanBitrate = int(oldFartServer.bitrate_limit)
         
    
    #create categories
    if not guild_has_category(oldFartServer, "2-MAX VOICE CHANNELS"):
        print("making 2v2 category...")
        await oldFartServer.create_category("2-MAX VOICE CHANNELS")
        
        bot.twosCategory = get_category(oldFartServer, "2-MAX VOICE CHANNELS")
         #create temp vc makers
        await oldFartServer.create_voice_channel("➕ Create 2's VC",category=bot.twosCategory)

    #create 3v3 category
    if not guild_has_category(oldFartServer, "3-MAX VOICE CHANNELS"):
        print("making 3v3 category...")
        await oldFartServer.create_category("3-MAX VOICE CHANNELS")
        
        bot.threesCategory = get_category(oldFartServer, "3-MAX VOICE CHANNELS")
         #create temp vc makers
        await oldFartServer.create_voice_channel("➕ Create 3's VC",category=bot.threesCategory)

    #create 4v4 category
    if not guild_has_category(oldFartServer, "4-MAX VOICE CHANNELS"):
        print("making 4v4 category...")
        await oldFartServer.create_category("4-MAX VOICE CHANNELS")
        
        bot.foursCategory = get_category(oldFartServer, "4-MAX VOICE CHANNELS")
         #create temp vc makers
        await oldFartServer.create_voice_channel("➕ Create 4's VC",category=bot.foursCategory)

    #create 6mans category
    if not guild_has_category(oldFartServer, "6-MAX VOICE CHANNELS"):
        print("making 6mans category...")
        await oldFartServer.create_category("6-MAX VOICE CHANNELS")
        
        bot.sixesCategory = get_category(oldFartServer, "6-MAX VOICE CHANNELS")
         #create temp vc makers
        await oldFartServer.create_voice_channel("➕ Create 6's VC",category=bot.sixesCategory)

    #get categories
    bot.twosCategory = get_category(oldFartServer, "2-MAX VOICE CHANNELS")
    bot.threesCategory = get_category(oldFartServer, "3-MAX VOICE CHANNELS")
    bot.foursCategory = get_category(oldFartServer, "4-MAX VOICE CHANNELS")
    bot.sixesCategory = get_category(oldFartServer, "6-MAX VOICE CHANNELS")
    #get creator channels
    for c in oldFartServer.channels:
        if c.name == "➕ Create 2's VC":
            bot.twosMakerChannel = c
        if c.name == "➕ Create 3's VC":
            bot.threesMakerChannel = c
        if c.name == "➕ Create 4's VC":
            bot.foursMakerChannel = c
        if c.name == "➕ Create 6's VC":
            bot.sixesMakerChannel = c
    

async def update_channels():
    try:
        await rename_and_reorder("2 Max", bot.twosMakerChannel.position +1)
    except:
        print("failed to reorder 2s")
    try:
        await rename_and_reorder("3 Max", bot.threesMakerChannel.position +1)
    except:
        print("failed to reorder 3s")
    try:
        await rename_and_reorder("4 Max", bot.foursMakerChannel.position +1)
    except:
        print("failed to reorder 4s")
    try:
        await rename_and_reorder("6 Max", bot.sixesMakerChannel.position +1)
    except:
        print("failed to reorder 6s")
 
@bot.event
async def on_message(msg):
    await update_channels()
    await bot.process_commands(msg)
    

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


async def rename_and_reorder(cName, cPos):
    cnum = 1
    #for channel in server
    for c in bot.oldFartServer.channels:
        if c != None and cName in c.name:
            await c.edit(name = cName +" #" + str(cnum), position = cPos)
            cnum = cnum +1
            cPos = cPos +1


with open('token.txt') as f:
    TOKEN = f.readline()

bot.run(TOKEN)