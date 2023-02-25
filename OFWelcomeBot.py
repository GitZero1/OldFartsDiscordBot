import discord
from discord.ext import commands
from datetime import datetime
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!',intents=intents)

serverID = ""
with open('serverID.txt') as f:
    serverID = f.readline()
serverID = int(serverID)

bot.oldFartServer = ""
bot.twosMakerChannel = ""
bot.threesMakerChannel = ""
bot.fourssMakerChannel = ""
bot.sixesMakerChannel = ""
bot.twosCategory = ""
bot.threesCategory = ""
bot.foursCategory = ""
bot.sixesCategory = ""

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
        else :
            print("server not found")

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


    #get categories
    bot.twosCategory = get_category(oldFartServer, "2v2")
    bot.threesCategory = get_category(oldFartServer, "3v3")
    bot.foursCategory = get_category(oldFartServer, "4v4")
    bot.sixesCategory = get_category(oldFartServer, "6mans")
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
        foursMakerChan = bot.foursMakerChannel
        sixesMakerChan = bot.sixesMakerChannel

        #TODO add 6mans
        if before.channel != None and "Max #" in before.channel.name or before.channel != None and "6mans #" in before.channel.name:
            if len(before.channel.members) == 0:
                await before.channel.delete()

        
        
        if after.channel == vcGen2v2:
            #create 2 max VC
            cnum = 1
            cpos = vcGen2v2.position + 1
            for c in guild.channels:
                if c != None and "2 Max" in c.name:
                    await c.edit(name = "2 Max #" + str(cnum))
                    cnum = cnum+1
                    cpos = cpos +1
            await guild.create_voice_channel("2 Max #" + str(cnum), position=cpos, category=bot.twosCategory, user_limit=2)
            #pull user into new VC
            for c in guild.channels:
                if c != None and c.name == "2 Max #" + str(cnum):
                    await member.move_to(c)

        if after.channel == threesMakerChan:
            #create 3 max VC
            cnum = 1
            cpos = threesMakerChan.position + 1
            for c in guild.channels:
                if c != None and "3 Max" in c.name:
                    await c.edit(name = "3 Max #" + str(cnum))
                    cnum = cnum+1
                    cpos = cpos +1
            await guild.create_voice_channel("3 Max #" + str(cnum), position=cpos, category=bot.threesCategory, user_limit=3)
            #pull user into new VC
            for c in guild.channels:
                if c != None and c.name == "3 Max #" + str(cnum):
                    await member.move_to(c)
        
        if after.channel == foursMakerChan:
            #create 4 max VC
            cnum = 1
            cpos = foursMakerChan.position + 1
            for c in guild.channels:
                if c != None and "4 Max" in c.name:
                    await c.edit(name = "4 Max #" + str(cnum))
                    cnum = cnum+1
                    cpos = cpos +1
            await guild.create_voice_channel("4 Max #" + str(cnum), position=cpos, category=bot.foursCategory, user_limit=4)
            #pull user into new VC
            for c in guild.channels:
                if c != None and c.name == "4 Max #" + str(cnum):
                    await member.move_to(c)

        if after.channel == sixesMakerChan:
            #create 6 max VC
            cnum = 1
            cpos = sixesMakerChan.position + 1
            for c in guild.channels:
                if c != None and "6mans #" in c.name:
                    await c.edit(name = "6mans #" + str(cnum))
                    cnum = cnum+1
                    cpos = cpos +1
            await guild.create_voice_channel("6mans #" + str(cnum), position=cpos, category=bot.sixesCategory, user_limit=6)
            #pull user into new VC
            for c in guild.channels:
                if c != None and c.name == "6mans #" + str(cnum):
                    await member.move_to(c)
                
@bot.event
async def on_guild_channel_create(channel):
    print(channel.name + " was created!")
    
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

