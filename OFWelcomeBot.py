import discord
from discord.ext import commands
from datetime import datetime
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!',intents=intents)

serverID = 0 #Server ID goes here
bot.oldFartServer = ""
bot.twosMakerChannel = ""
bot.threesMakerChannel = ""
bot.twosCategory = ""
bot.threesCategory = ""

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
    #create categories
    if not guild_has_category(oldFartServer, "2v2"):
        print("making 2v2 category...")
        await oldFartServer.create_category("2v2")
        
        bot.twosCategory = get_category(oldFartServer, "2v2")
         #create temp vc makers
        await oldFartServer.create_voice_channel("Create new 2v2",category=bot.twosCategory)

    if not guild_has_category(oldFartServer, "3v3"):
        print("making 3v3 category...")
        await oldFartServer.create_category("3v3")
        
        bot.threesCategory = get_category(oldFartServer, "3v3")
         #create temp vc makers
        await oldFartServer.create_voice_channel("Create new 3v3",category=bot.threesCategory)

    #get categories
    bot.twosCategory = get_category(oldFartServer, "2v2")
    bot.threesCategory = get_category(oldFartServer, "3v3")
    #get creator channels
    for c in oldFartServer.channels:
        if c.name == "Create new 2v2":
            bot.twosMakerChannel = c
        if c.name == "Create new 3v3":
            bot.threesMakerChannel = c


   
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

@bot.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == serverID:
        guild = member.guild
        vcGen2v2 = bot.twosMakerChannel
        threesMakerChan = bot.threesMakerChannel
        
        if after.channel == vcGen2v2:
            #create 2 max VC
            #pull user into new VC
            cnum = 1
            cpos = vcGen2v2.position + 1
            for c in guild.channels:
                if c != None and "2 Max" in c.name:
                    cnum = cnum+1
                    cpos = cpos +1
            await guild.create_voice_channel("2 Max #" + str(cnum), position=cpos, category=bot.twosCategory, user_limit=2)
            for c in guild.channels:
                if c != None and c.name == "2 Max #" + str(cnum):
                    await member.move_to(c)
        if before.channel != None and "2 Max #" in before.channel.name:
            if len(before.channel.members) == 0:
                await before.channel.delete()

        if after.channel == threesMakerChan:
            #create 3 max VC
            #pull user into new VC
            cnum = 1
            cpos = threesMakerChan.position + 1
            for c in guild.channels:
                if c != None and "3 Max" in c.name:
                    cnum = cnum+1
                    cpos = cpos +1
            await guild.create_voice_channel("3 Max #" + str(cnum), position=cpos, category=bot.threesCategory, user_limit=3)
            for c in guild.channels:
                if c != None and c.name == "3 Max #" + str(cnum):
                    await member.move_to(c)
        if before.channel != None and "3 Max #" in before.channel.name:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                
@bot.event
async def on_guild_channel_create(channel):
    print(channel.name + " was created!")
    if channel.name == "2v2":
        bot.twosMakerChannel = channel
    if channel.name == "Create new 3v3":
        bot.threesMakerChannel = channel

    
#@bot.event
#async def on_member_join(member):
#    # channel to print to
#    printChan = bot.get_channel(12345679)
#    await printChan.send( "Welcome " + member.mention + " Please head over to " + printChan.mention + " to set up your profile")

######## END OF COMMANDS ##########################################################

def get_guild():
    return bot.oldFartServer

with open('token.txt') as f:
    TOKEN = f.readline()

bot.run(TOKEN)



# user does some command like "!LFG Diamond2 2v2 VC" (need to think of a way to make this more user friendly)
#bot creates voice channel max 2/3 based on mode selected.
#bot pulls user into VC
#bot posts link to channel in LFG chat + info about the LFG

