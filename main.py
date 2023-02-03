import nest_asyncio
import asyncio
nest_asyncio.apply()
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select,View
import random
import datetime
import time
import os
import json
import random
from PIL import Image, ImageDraw, ImageFont
        
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '/', intents=intents, help_command=None)

# Define image location
global metadatajson
metadatajson = r"C:\Users\USER\Desktop\HolyShxxt Card Fantasy\Metadata.json"
global playeridjson
playeridjson = r"C:\Users\USER\Desktop\HolyShxxt Card Fantasy\Player.json"
global playerimage
playerimage = "C:/Users/USER/Desktop/HolyShxxt Card Fantasy/Card/"
global formationimage
formationimage = r"C:/Users/USER/Desktop/HolyShxxt Card Fantasy/Formation/"
global squadimage
squadimage = r'C:/Users/USER/Desktop/HolyShxxt Card Fantasy/Squad/'
global thumbnailimageloc
thumbnailimageloc = r'C:/Users/USER/Desktop/HolyShxxt Card Fantasy/Thumbnail/'
global listimageloc
listimageloc = r'C:/Users/USER/Desktop/HolyShxxt Card Fantasy/List/'

# Define number of players
global maxplayerlimit
maxplayerlimit = 2426

# Create star player pool
global onestarpool
onestarpool =[]
global twostarpool
twostarpool =[]
global threestarpool
threestarpool =[]
global fourstarpool
fourstarpool = []
global fivestarpool
fivestarpool = []

with open(playeridjson) as f:
    data = json.loads(f.read())
    Playerinfo = data["HolyShxxtPlayers"]
for i in Playerinfo:
    Playerid = i['PlayerID']
    Rating = i["Rating"]
    if Rating == 1:
        onestarpool.append(Playerid)
    elif Rating == 2:
        twostarpool.append(Playerid)
    elif Rating == 3:
        threestarpool.append(Playerid)
    elif Rating == 4:
        fourstarpool.append(Playerid)
    elif Rating == 5:
        fivestarpool.append(Playerid)

@client.event
async def on_ready():
    # Prints a message when the bot is online and functioning
    await client.change_presence(status=discord.Status.online, activity = discord.Game(name=f"Let's join Community-GameFi NFT HolyShxxt! 🥳 🎉 Currently in {len(client.guilds)} servers! 🎉"))
    print('Ready to start the league!')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    

@client.tree.command(name="show", description="Show HolyShxxt Card Fantasy Player Details")
@app_commands.describe(id = "PlayerID of the HolyShxxt Card Fantasy Player")
async def show(interaction:discord.Interaction, id:int):
    # Show player image and ability
    channel = interaction.channel
    userid = interaction.user.id
    playerid = int(id)
    imageid = str(id) + ".png"
    if playerid >= 0 and playerid <= maxplayerlimit:
        with open(playeridjson) as f:
            data = json.loads(f.read())
            Playerinfo = data["HolyShxxtPlayers"]
            Playerinfoid = Playerinfo[int(playerid)]
            Price = Playerinfoid["Price"]
            Position = Playerinfoid["Position"]
            Attacking = Playerinfoid["Attacking"]
            Vision = Playerinfoid["Vision"]
            Defending = Playerinfoid["Defending"]
            Goalkeeping = Playerinfoid["Goalkeeping"]
            Physical = Playerinfoid["Physical"]
        os.chdir(playerimage)
        message = "<@" + str(userid) + "> Player #" + str(playerid)
        message = message + "\n " + "Position: " + str(Position)
        message = message + "\n " + "Attack: " + str(Attacking)
        message = message + "\n " + "Vision: " + str(Vision)
        message = message + "\n " + "Defend: " + str(Defending)
        message = message + "\n " + "Goalkeeping: " + str(Goalkeeping)
        message = message + "\n " + "Physical: " + str(Physical)
        message = message + "\n " + "Mint Price: $" + str("{:,}".format(int(Price)))
        message = message + "\n " + "Burn Price: $" + str("{:,}".format(round(int(Price)/3)))
        f.close()
        await interaction.response.send_message(message, file=discord.File(imageid))
    else:
        message =  "Cannot find the player."
        await interaction.response.send_message(message)


@client.tree.command(name="create", description="Create Gamer Profile for HolyShxxt Card Fantasy")
async def create(interaction:discord.Interaction):
    # Create game profile
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            found = True 
    if found == False:
                gamercount = len(data)
                print(gamercount)
                new_data = {"Profile": str(gamercount),
                 "UserID": str(userid),
                 "Money": 0,
                 "LastClaimTime": str(0),
                 "LastDailyTime": str(0),
                 "LastMatchTime": str(0),
                 "Players":[],
                 "Formation":"",
                 "Squad":["","","","","","","","","","",""]
                 }
                Gamerinfo.append(new_data)
                with open(metadatajson,"w") as f:
                    json.dump(Gamerinfo, f,indent=4, separators=(',',':'))
                message = "Gamer Profile Created. \n Welcome to HolyShxxt Card Fantasy!"
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'Gamer Profile Creation')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
    else:
        message = "You have already created a gamer profile!"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Gamer Profile Creation')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    f.close()


@client.tree.command(name="money", description="Show Current Balance")
async def money(interaction:discord.Interaction):
    # Show current balance
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            found = True
            money = i['Money']
    if found == True:
        message = " You have $ " + str("{:,}".format(int(money)))
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Current Balance')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    else:
        message = "Cannot find your gamer profile.\n Please create a profile using /create"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Current Balance')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    f.close()


@client.tree.command(name="freemint", description="Get a Free Player Each Hour")
async def freemint(interaction:discord.Interaction):
        # Get free player
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            found = True
            lastclaimtime = i['LastClaimTime']
            playerlist = i['Players']
    if found == False:
        message = "Cannot find your gamer profile. \n Please create a profile using /create"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Free Mint')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    elif found == True:
         # Command still in cooldown
        currenttime = time.time()
        timegap = int(currenttime) - int(lastclaimtime)
        if  timegap < 3600:
            message = "Please claim again after " + str(round((int(lastclaimtime) + 3600 - int(currenttime))/60) ) + " minutes."
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Free Mint')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)
        else:
            # Reject if there are 20 players
          if len(playerlist) >= 20:
                message = "You cannot have more than 20 players in your team. \n Please consider burn some players first."
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'Free Mint')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
          else:
            f.close()
            # Randomly select the star pool
            ran = random.randint(1,1000)
            if ran <= 800:
                star = 1
            elif ran <= 944:
                star = 2
            elif ran <= 994:
                star = 3
            elif ran <= 999:
                star = 4
            elif ran <= 1000:
                star = 5
            print(star)
            with open(playeridjson) as f:
                data = json.loads(f.read())
                Playerinfo = data["HolyShxxtPlayers"]
            with open(metadatajson) as g:
                gdata = json.loads(g.read())
                Gamerinfo = gdata
            if star == 1:
                Playerid = random.choice(onestarpool)
            elif star == 2:
                Playerid = random.choice(twostarpool)
            elif star == 3:
                Playerid = random.choice(threestarpool)
            elif star == 4:
                Playerid = random.choice(fourstarpool)
            elif star == 5:
                Playerid = random.choice(fivestarpool)
            Playerinfoid = Playerinfo[Playerid]
            # Check whether user has the player
            while Playerid in playerlist:
                if star == 1:
                    Playerid = random.choice(onestarpool)
                elif star == 2:
                    Playerid = random.choice(twostarpool)
                elif star == 3:
                    Playerid = random.choice(threestarpool)
                elif star == 4:
                    Playerid = random.choice(fourstarpool)
                elif star == 5:
                    Playerid = random.choice(fivestarpool)
                Playerinfoid = Playerinfo[Playerid]
            Price = Playerinfoid["Price"]
            Position = Playerinfoid["Position"]
            Attacking = Playerinfoid["Attacking"]
            Vision = Playerinfoid["Vision"]
            Defending = Playerinfoid["Defending"]
            Goalkeeping = Playerinfoid["Goalkeeping"]
            Physical = Playerinfoid["Physical"]
            f.close()
            g.close()
            # Add player to user
            with open(metadatajson,"r") as f:
                data = json.loads(f.read())
                Gamerinfo = data
            for i in Gamerinfo:
                if i['UserID'] == str(userid):
                    i['Players'].append(Playerid)
            with open(metadatajson,"w") as f:
                json.dump(Gamerinfo, f,indent=4, separators=(',',':'))
                f.close()
            with open(metadatajson,"r") as g:
                gdata = json.loads(g.read())
                Gamerinfo = gdata
                for i in Gamerinfo:
                    if i['UserID'] == str(userid):
                        i['LastClaimTime'] = str(int(currenttime))
                g.close()
            with open(metadatajson,"w") as g:
                json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                g.close()
            message = "Freeminted Player #" + str(Playerid)
            message = message + "\n \n " + "Position: " + str(Position)
            message = message + "\n " + "Attack: " + str(Attacking)
            message = message + "\n " + "Vision: " + str(Vision)
            message = message + "\n " + "Defend: " + str(Defending)
            message = message + "\n " + "Goalkeeping: " + str(Goalkeeping)
            message = message + "\n " + "Physical: " + str(Physical)
            message = message + "\n " + "Mint Price: $" + str("{:,}".format(int(Price)))
            message = message + "\n " + "Burn Price: $" + str("{:,}".format(round(int(Price)/3)))
            os.chdir(playerimage)
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Free Mint')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox, file=discord.File(str(Playerid)+".png"))
            f.close()
            # Ask player whether to burn player
            message = await channel.send("<@"+str(userid)+"> " + "\n Do you want to **burn** freeminted Player# "+ str(Playerid) + " for  $" + str("{:,}".format(round(int(Price)/3))) + "\n \n Click 🔥 in 10s to Burn or Wait to Keep it" )
            await message.add_reaction("🔥")
            def check(reaction, user):
                    return user == interaction.user and str(reaction.emoji) in ["🔥"] and reaction.message == message
            try: # waiting for message
                    confirm = await client.wait_for("reaction_add", check=check,timeout = 10.0)
            except asyncio.TimeoutError: # returning after timeout
                    message = "Freeminted Player#" + str(Playerid) +" has added to your player list"
                    messagebox = discord.Embed(color = 0xff0000)
                    messagebox.set_author(name = f'Free Mint')
                    username = client.get_user(userid)
                    messagebox.add_field(name= username, value = message, inline = False)
                    messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                    await interaction.followup.send(embed = messagebox)
                    return
            if confirm:
                    with open(metadatajson,"r") as f:
                      data = json.loads(f.read())
                      Gamerinfo = data
                    for i in Gamerinfo:
                        if i['UserID'] == str(userid):
                            playerlist = i['Players']
                            squad = i['Squad']
                            money = i['Money']
                    f.close()
                    with open(playeridjson) as f:
                        data = json.loads(f.read())
                        Playerinfo = data["HolyShxxtPlayers"]
                        Playerid = int(Playerid)
                        Playerinfoid = Playerinfo[Playerid]
                        Price = round(int(Playerinfoid['Price'])/3)
                    f.close()
                    pos = playerlist.index(Playerid)
                    if Playerid in squad:
                        oldpos = squad.index(int(Playerid))
                        with open(metadatajson,"r") as f:
                            data = json.loads(f.read())
                            Gamerinfo = data
                        for i in Gamerinfo:
                            if i['UserID'] == str(userid):
                                squad = i['Squad']
                                squad[int(oldpos)] = ""
                    with open(metadatajson,"r") as f:
                        data = json.loads(f.read())
                        Gamerinfo = data
                        for i in Gamerinfo:
                            if i['UserID'] == str(userid):
                                i['Money'] = int(money) + int(Price)
                                i['Players'].pop(pos)
                                i['Squad'] = squad
                    with open(metadatajson,"w") as g:
                        json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                        g.close()
                    message = "burnt Player #" + str(Playerid) + " for $" + str("{:,}".format(int(Price))) + "\n \n"
                    message = message + "You now have $" + str("{:,}".format(int(money) + int(Price)))
                    messagebox = discord.Embed(color = 0xff0000)
                    messagebox.set_author(name = f'Free Mint')
                    username = client.get_user(userid)
                    messagebox.add_field(name= username, value = message, inline = False)
                    messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                    await interaction.followup.send(embed = messagebox)


@client.tree.command(name="list", description="Show Full List of Your Players")
@app_commands.describe(sortkey = "Attack / Defend / Vision / Goalkeeping / Physical")
async def list(interaction:discord.Interaction, sortkey:str = None):
    # Show player list
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            playerlist = i['Players']
            profile = i['Profile']
            squad = i['Squad']
            found = True
    f.close()
    if found == False:
        message = "Cannot find your gamer profile.\n Please create a profile using /create."
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Player List')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    else:
        empty = True
        for i in playerlist:
            if i != "":
                empty = False
        if empty == True:
            message = "You dont have any player in your club"
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Player List')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)
        else:
            sortplayer = []
            message = "<@"+ str(userid) + "> You have below players: \n"
            with open(playeridjson) as f:
                data = json.loads(f.read())
                Playerinfo = data["HolyShxxtPlayers"]
            for i in playerlist:
                  Playerid = int(i)
                  Playerinfoid = Playerinfo[Playerid]
                  sortplayer.append(Playerinfoid)
            if sortkey == None:
                sortplayer.sort(key=lambda x: x.get('Price'), reverse=True)
            elif sortkey == "Attack":
                sortplayer.sort(key=lambda x: x.get('Attacking'), reverse=True)
            elif sortkey == "Defend":
                sortplayer.sort(key=lambda x: x.get('Defending'), reverse=True)
            elif sortkey == "Vision":
                sortplayer.sort(key=lambda x: x.get('Vision'), reverse=True)
            elif sortkey == "Goalkeeping":
                sortplayer.sort(key=lambda x: x.get('Goalkeeping'), reverse=True)
            elif sortkey == "Physical":
                sortplayer.sort(key=lambda x: x.get('Physical'), reverse=True)
            else: sortplayer.sort(key=lambda x: x.get('Price'), reverse=True)
            f.close()
            text = ""
            for i in sortplayer:
                  Playerid = i['PlayerID']
                  Position = i['Position']
                  Rating = i['Rating']
                  Attacking = i['Attacking']
                  Vision = i['Vision']
                  Defending = i['Defending']
                  Goalkeeping = i['Goalkeeping']
                  Physical = i['Physical']
                  Price = i['Price']
                  if i['PlayerID'] in squad:
                      text = text + "Player #" + str(Playerid) + " (" + str(Rating) + "* " + str(Position) + ")" + " - Burn: $" + str("{:,}".format(round(int(Price)/3))) + " - Starter 11 \n"
                  else:
                      text = text + "Player #" + str(Playerid) + " (" + str(Rating) + "* " + str(Position) + ")" + " - Burn: $" + str("{:,}".format(round(int(Price)/3))) + "\n"
                  text = text + "  Attack: " + str(Attacking) + "  Vision: " + str(Vision) + "  Defend: " + str(Defending) + "  Goalkeeping: " + str(Goalkeeping) + "  Physical: " + str(Physical) + "\n \n"
            long = int(4000 / 22 * len(playerlist) )
            img = Image.new('RGB', (2200, long), color=(0,0,0))  
            draw = ImageDraw.Draw(img)
            fonttype = ImageFont.truetype("arial.ttf", 60) 
            draw.text((250, 60), text=text, fill=(255, 255 ,255), font=fonttype)
            imagefile = "List" + str(profile) + ".png"
            img.save(listimageloc + imagefile)
            thumbnailposition = 50
            for i in sortplayer:
                thumbnailimage = thumbnailimageloc + str(i['PlayerID']) + ".png"
                thumbnail = Image.open(thumbnailimage)
                thumbnail = thumbnail.resize((150,150))
                img.paste(thumbnail,(50,thumbnailposition))
                thumbnailposition = thumbnailposition + 176
            img.save(listimageloc + imagefile)
            os.chdir(listimageloc)
            await interaction.response.send_message(message, file=discord.File(imagefile))

@client.tree.command(name="mint", description="Pay and Mint a Player")
@app_commands.describe(mintid = "PlayerID of the HolyShxxt Card Fantasy Player")
async def mint(interaction:discord.Interaction, mintid:str):
    # Pay and get the player 
    channel = interaction.channel
    userid = interaction.user.id
    if mintid == None:
        message = "Please input PlayerID"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Mint Player')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    else:
        mintplayer = int(mintid)
        if mintplayer < 0 or mintplayer > maxplayerlimit:
            message = "Cannot find the player"
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Mint Player')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)
        else:
            with open(metadatajson,"r") as f:
              data = json.loads(f.read())
              Gamerinfo = data
            found = False
            for i in Gamerinfo:
                if i['UserID'] == str(userid):
                    playerlist = i['Players']
                    money = i['Money']
                    found = True
            if found == False:
                message = "Cannot find your gamer profile.\n Please create a profile using /create."
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'Mint Player')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
            elif found == True:
                if len(playerlist) >= 20:
                  message = "You cannot have more than 20 players in your team. \n Please consider burn some players first."
                  messagebox = discord.Embed(color = 0xff0000)
                  messagebox.set_author(name = f'Mint Player')
                  username = client.get_user(userid)
                  messagebox.add_field(name= username, value = message, inline = False)
                  messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                  await interaction.response.send_message(embed = messagebox)
                elif mintplayer in playerlist:
                    message = "You have already owned this player"
                    messagebox = discord.Embed(color = 0xff0000)
                    messagebox.set_author(name = f'Mint Player')
                    username = client.get_user(userid)
                    messagebox.add_field(name= username, value = message, inline = False)
                    messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                    await interaction.response.send_message(embed = messagebox)
                else:
                    os.chdir(playerimage)
                    with open(playeridjson) as f:
                        data = json.loads(f.read())
                        Playerinfo = data["HolyShxxtPlayers"]
                        Playerid = int(mintid)
                        Playerinfoid = Playerinfo[Playerid]
                        Price = Playerinfoid['Price']
                    await interaction.response.send_message("\n Are you sure you want to **mint** this Player# "+ str(mintid) + " ? ")
                    message = await channel.send("<@"+str(userid)+"> Mint Price for Player#" + str(mintid) + ": $" + str("{:,}".format(int(Price))) + "\n \n Click ✅ in 10s to Mint or Wait to Cancel" ,file=discord.File(str(mintid)+".png"))
                    await message.add_reaction("✅")
                    def check(reaction, user):
                        return user == interaction.user and str(reaction.emoji) in ["✅"] and reaction.message == message
                    try: # waiting for message
                        confirm = await client.wait_for("reaction_add", check=check,timeout = 10.0)
                    except asyncio.TimeoutError: # returning after timeout
                        message = "You have cancelled your mint action."
                        messagebox = discord.Embed(color = 0xff0000)
                        messagebox.set_author(name = f'Mint Player')
                        username = client.get_user(userid)
                        messagebox.add_field(name= username, value = message, inline = False)
                        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                        await interaction.followup.send(embed = messagebox)
                        return
                    if confirm:
                        with open(playeridjson) as f:
                            data = json.loads(f.read())
                            Playerinfo = data["HolyShxxtPlayers"]
                            Playerid = int(mintplayer)
                            Playerinfoid = Playerinfo[Playerid]
                            Price = Playerinfoid['Price']
                        if int(Price) > int(money):
                            message = "You still need $" + str("{:,}".format(int(Price)-int(money)))
                            messagebox = discord.Embed(color = 0xff0000)
                            messagebox.set_author(name = f'Mint Player')
                            username = client.get_user(userid)
                            messagebox.add_field(name= username, value = message, inline = False)
                            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                            await interaction.followup.send(embed = messagebox)
                        elif mintplayer >= 0 and mintplayer <= maxplayerlimit:
                            with open(metadatajson,"r") as f:
                                data = json.loads(f.read())
                                Gamerinfo = data
                            for i in Gamerinfo:
                                if i['UserID'] == str(userid):
                                    i['Money'] = int(money) - int(Price)
                                    i['Players'].append(mintplayer)
                            with open(metadatajson,"w") as g:
                                json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                                g.close()
                            message = "minted Player #" + str(mintplayer) + " for $" + str("{:,}".format(int(Price))) + "\n \n"
                            message = message + "You now have $" + str("{:,}".format(int(money)-int(Price)))
                            os.chdir(playerimage)
                            messagebox = discord.Embed(color = 0xff0000)
                            messagebox.set_author(name = f'Mint Player')
                            username = client.get_user(userid)
                            messagebox.add_field(name= username, value = message, inline = False)
                            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                            await interaction.followup.send(embed = messagebox, file=discord.File(str(Playerid)+".png"))


@client.tree.command(name="burn", description="Burn and Sell a Player")
@app_commands.describe(burnid = "PlayerID of the HolyShxxt Card Fantasy Player")
async def burn(interaction:discord.Interaction, burnid:str):
    channel = interaction.channel
    userid = interaction.user.id
    if burnid == None:
        message = "Please input PlayerID"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Burn Player')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    else:
        burnplayer = int(burnid)
        with open(metadatajson,"r") as f:
          data = json.loads(f.read())
          Gamerinfo = data
        found = False
        for i in Gamerinfo:
            if i['UserID'] == str(userid):
                playerlist = i['Players']
                money = i['Money']
                squad = i['Squad']
                found = True
        if found == False:
            message = "Cannot find your gamer profile.\n Please create a profile using /create."
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Burn Player')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)
        elif found == True:
            if burnplayer not in playerlist:
                message = "You don't have this player"
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'Burn Player')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
            else:
                os.chdir(playerimage)
                with open(playeridjson) as f:
                    data = json.loads(f.read())
                    Playerinfo = data["HolyShxxtPlayers"]
                    Playerid = int(burnid)
                    Playerinfoid = Playerinfo[Playerid]
                    Price = round(Playerinfoid['Price']/3)
                if int(burnid) in squad:
                    await interaction.response.send_message("\n **The player is in your squad.** \n Are you sure you want to burn Player# "+ str(burnid) + " ?")
                else:
                    await interaction.response.send_message("\n Are you sure you want to **burn** Player# "+ str(burnid) + " ? ")
                message = await channel.send("<@"+str(userid)+"> Burn Price for Player#" + str(burnid) + ": $" + str("{:,}".format(int(Price))) + "\n \n Click ✅ in 10s to Burn or Wait to Cancel" ,file=discord.File(str(burnid)+".png"))
                await message.add_reaction("✅")
                def check(reaction, user):
                    return user == interaction.user and str(reaction.emoji) in ["✅"] and reaction.message == message
                try: # waiting for message
                    confirm = await client.wait_for("reaction_add", check=check,timeout = 10.0)
                except asyncio.TimeoutError: # returning after timeout
                    message = "You have cancelled your burn action."
                    messagebox = discord.Embed(color = 0xff0000)
                    messagebox.set_author(name = f'Burn Player')
                    username = client.get_user(userid)
                    messagebox.add_field(name= username, value = message, inline = False)
                    messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                    await interaction.followup.send(embed = messagebox)
                    return
                if confirm:
                    with open(playeridjson) as f:
                        data = json.loads(f.read())
                        Playerinfo = data["HolyShxxtPlayers"]
                        Playerid = int(burnplayer)
                        Playerinfoid = Playerinfo[Playerid]
                        Price = round(int(Playerinfoid['Price'])/3)
                    f.close()
                    pos = playerlist.index(burnplayer)
                    if burnplayer in squad:
                        oldpos = squad.index(int(burnplayer))
                        with open(metadatajson,"r") as f:
                            data = json.loads(f.read())
                            Gamerinfo = data
                        for i in Gamerinfo:
                            if i['UserID'] == str(userid):
                                squad = i['Squad']
                                squad[int(oldpos)] = ""
                    with open(metadatajson,"r") as f:
                        data = json.loads(f.read())
                        Gamerinfo = data
                        for i in Gamerinfo:
                            if i['UserID'] == str(userid):
                                i['Money'] = int(money) + int(Price)
                                i['Players'].pop(pos)
                                i['Squad'] = squad
                    with open(metadatajson,"w") as g:
                        json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                        g.close()
                    message = "burnt Player #" + str(burnplayer) + " for $" + str("{:,}".format(int(Price))) + "\n \n"
                    message = message + "You now have $" + str("{:,}".format(int(money) + int(Price)))
                    os.chdir(playerimage)
                    messagebox = discord.Embed(color = 0xff0000)
                    messagebox.set_author(name = f'Burn Player')
                    username = client.get_user(userid)
                    messagebox.add_field(name= username, value = message, inline = False)
                    messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                    await interaction.followup.send(embed = messagebox)
            
@client.tree.command(name="formation", description="Set Your Team Formation")
@app_commands.describe(formation = "433 / 442 / 541 / 343")
async def formation(interaction:discord.Interaction, formation:str =None):
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            form = i['Formation']
            found = True
    if found == False:
        message = "Cannot find your gamer profile.\n Please create a profile using /create."
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Formation')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    elif found == True:
        if formation == None and form == "":
            print(formation)
            message = "You can select the formation of \n 433 \n 442 \n 541 \n 343 \n /formation [formation]"
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Formation')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)
        elif formation == None and form != "":
            message = "You are using the formation of " + str(form)
            message = message + "\n \n You can select the formation of \n 433 \n 442 \n 541 \n 343 \n /formation [formation]"
            os.chdir(formationimage)
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Formation')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox, file=discord.File(str(form)+".png"))
        elif formation == "433" or formation == "442" or formation == "541" or formation == "343":
            with open(metadatajson,"r") as f:
                data = json.loads(f.read())
                Gamerinfo = data
            for i in Gamerinfo:
                    if i['UserID'] == str(userid):
                        i['Formation'] = formation
            with open(metadatajson,"w") as g:
                    json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                    g.close()
            message = "You are now using the formation of " + str(formation)
            os.chdir(formationimage)
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Formation')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox, file=discord.File(str(formation)+".png"))
        else:
            message = "You cannot select the formation of " + str(formation)
            message = message + "\n \n You can select the formation of \n 433 \n 442 \n 541 \n 343 \n /formation [formation]"
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Formation')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)
            
@client.tree.command(name="squad", description="Set Your Squad")
@app_commands.describe(position = "Position Number", playerid = "PlayerID of the HolyShxxt Card Fantasy Player")
async def squad(interaction:discord.Interaction, position:str=None, playerid:str=None):
    pos = position
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            form = i['Formation']
            playerlist = i['Players']
            squad = i['Squad']
            found = True
            profile = i['Profile']
    if found == False:
        message = "Cannot find your gamer profile.\n Please create a profile using /create."
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Squad')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    elif found == True:
        if pos==None and playerid==None:
            empty = True
            for i in squad:
                if i != "":
                    empty = False
            if empty == False:
                totalvalue = 0
                for i in squad:
                        Price = 0
                        if i != "":
                            playeridvalue = i
                            with open(playeridjson) as f:
                                data = json.loads(f.read())
                                Playerinfo = data["HolyShxxtPlayers"]
                                Playerid = int(playeridvalue)
                                Playerinfoid = Playerinfo[Playerid]
                                Price = Playerinfoid['Price']
                        totalvalue = totalvalue + Price
                message = "<@"+ str(userid) + "> You are using the formation of " + str(form) + " and current squad: \n" + "Total value: **$" + str("{:,}".format(int(totalvalue))) + "** \n \n"
                message = message + "Type /squad [Position_Number] [Playerid] to build the squad \n \n"
                a = 1
                for i in squad:
                    if i != "":
                        playeridvalue = i
                        with open(playeridjson) as f:
                            data = json.loads(f.read())
                            Playerinfo = data["HolyShxxtPlayers"]
                            Playerid = int(playeridvalue)
                            Playerinfoid = Playerinfo[Playerid]
                            Position = Playerinfoid['Position']
                            Rating = Playerinfoid['Rating']
                            message = message + str(a) + ": Player #" + str(i) + " (" + str(Rating) + "* " + str(Position) + ")\n"
                    if i == "":
                        message = message + str(a) + ": Player #" + str(i) +"\n"
                    a = a + 1
                img = Image.open(formationimage + str(form)+".png")
                position = 0
                for i in squad:
                    if str(form) == "433" : 
                        if i != "":
                            position = position + 1
                            if position == 1:
                                thumbnailposition = 480
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(210,thumbnailposition))
                            if position == 2:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(70,thumbnailposition))
                            if position == 3:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(160,thumbnailposition))
                            if position == 4:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(255,thumbnailposition))
                            if position == 5:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(350,thumbnailposition))
                            if position == 6:
                                thumbnailposition = 292
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(200,thumbnailposition))
                            if position == 7:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(150,thumbnailposition))
                            if position == 8:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(255,thumbnailposition))
                            if position == 9:
                                thumbnailposition = 145
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(70,thumbnailposition))
                            if position == 10:
                                thumbnailposition = 145
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(350,thumbnailposition))
                            if position == 11:
                                thumbnailposition = 30
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(210,thumbnailposition))
                    elif str(form) == "442" :
                        if i != "":
                            position = position + 1
                            if position == 1:
                                thumbnailposition = 480
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(210,thumbnailposition))
                            if position == 2:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(70,thumbnailposition))
                            if position == 3:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(160,thumbnailposition))
                            if position == 4:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(255,thumbnailposition))
                            if position == 5:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(350,thumbnailposition))
                            if position == 6:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(70,thumbnailposition))
                            if position == 7:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(160,thumbnailposition))
                            if position == 8:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(255,thumbnailposition))
                            if position == 9:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(350,thumbnailposition))
                            if position == 10:
                                thumbnailposition = 30
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(160,thumbnailposition))
                            if position == 11:
                                thumbnailposition = 30
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(250,thumbnailposition))
                    elif str(form) == "343" :
                        if i != "":
                            position = position + 1
                            if position == 1:
                                thumbnailposition = 480
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(210,thumbnailposition))
                            if position == 2:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(108,thumbnailposition))
                            if position == 3:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(198,thumbnailposition))
                            if position == 4:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(293,thumbnailposition))
                            if position == 5:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(70,thumbnailposition))
                            if position == 6:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(160,thumbnailposition))
                            if position == 7:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(255,thumbnailposition))
                            if position == 8:
                                thumbnailposition = 213
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(350,thumbnailposition))
                            if position == 9:
                                thumbnailposition = 105
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(70,thumbnailposition))
                            if position == 10:
                                thumbnailposition = 105
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(350,thumbnailposition))
                            if position == 11:
                                thumbnailposition = 30
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(200,thumbnailposition))
                    elif str(form) == "541" :
                        if i != "":
                            position = position + 1
                            if position == 1:
                                thumbnailposition = 480
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(210,thumbnailposition))
                            if position == 2:
                                thumbnailposition = 300
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(70,thumbnailposition))
                            if position == 3:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(108,thumbnailposition))
                            if position == 4:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(203,thumbnailposition))
                            if position == 5:
                                thumbnailposition = 379
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(293,thumbnailposition))
                            if position == 6:
                                thumbnailposition = 300
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(350,thumbnailposition))
                            if position == 7:
                                thumbnailposition = 145
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(60,thumbnailposition))
                            if position == 8:
                                thumbnailposition = 215
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(150,thumbnailposition))
                            if position == 9:
                                thumbnailposition = 215
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(255,thumbnailposition))
                            if position == 10:
                                thumbnailposition = 145
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(355,thumbnailposition))
                            if position == 11:
                                thumbnailposition = 30
                                thumbnailimage = thumbnailimageloc + str(i) + ".png"
                                thumbnail = Image.open(thumbnailimage)
                                thumbnail = thumbnail.convert("RGBA")
                                thumbnail = thumbnail.resize((70,70))
                                img.paste(thumbnail,(200,thumbnailposition))
                imagefile = "Squad" + str(profile) + ".png"
                img.save(squadimage + imagefile)
                os.chdir(squadimage)
                await interaction.response.send_message(message, file=discord.File(imagefile))
            elif empty == True and form != "":
                message = "<@"+ str(userid) + "> You are using the formation of " + str(form) + "\n"
                message = message + "Type /squad [Jersey_Number] [Playerid] to build a squad."
                os.chdir(formationimage)
                await interaction.response.send_message(message, file=discord.File(str(form)+".png"))
            elif empty == True and form == "":
                message = "<@"+ str(userid) + "> You don't have any formation \n"
                message = message + "Type /formation to set a formation for the squad first"
                await interaction.response.send_message(message)
        elif pos!=None and playerid!=None:
                if int(playerid) not in playerlist:
                    message = "<@"+ str(userid) + "> You don't have this player #" + str(playerid)
                    await interaction.response.send_message(message)
                elif int(playerid) in squad:
                    oldpos = squad.index(int(playerid))
                    with open(metadatajson,"r") as f:
                        data = json.loads(f.read())
                        Gamerinfo = data
                    for i in Gamerinfo:
                        if i['UserID'] == str(userid):
                            squad = i['Squad']
                        squad[int(oldpos)] = ""
                    with open(metadatajson,"w") as g:
                        json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                        g.close()
                    with open(metadatajson,"r") as f:
                        data = json.loads(f.read())
                        Gamerinfo = data
                    for i in Gamerinfo:
                        if i['UserID'] == str(userid):
                             squad = i['Squad']
                        squad[int(pos)-1] = int(playerid)
                    with open(metadatajson,"r") as f:
                        data = json.loads(f.read())
                        Gamerinfo = data
                    for i in Gamerinfo:
                        if i['UserID'] == str(userid):
                            i['Squad'] = squad
                    with open(metadatajson,"w") as g:
                        json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                        g.close()
                    message = "<@"+ str(userid) + "> Player #" + str(playerid) + " has assigned to number " + str(pos) + "\n"
                    a = 1
                    for i in squad:
                        if i != "":
                            playeridvalue = i
                            with open(playeridjson) as f:
                                data = json.loads(f.read())
                                Playerinfo = data["HolyShxxtPlayers"]
                                Playerid = int(playeridvalue)
                                Playerinfoid = Playerinfo[Playerid]
                                Position = Playerinfoid['Position']
                                Rating = Playerinfoid['Rating']
                                message = message + str(a) + ": Player #" + str(i) + " (" + str(Rating) + "* " + str(Position) + ")\n"
                        if i == "":
                            message = message + str(a) + ": Player #" + str(i) +"\n"
                        a = a + 1
                    os.chdir(formationimage)
                    await interaction.response.send_message(message, file=discord.File(str(form)+".png")) 
                else:
                    with open(metadatajson,"r") as f:
                        data = json.loads(f.read())
                        Gamerinfo = data
                    for i in Gamerinfo:
                        if i['UserID'] == str(userid):
                             squad = i['Squad']
                        squad[int(pos)-1] = int(playerid)
                    with open(metadatajson,"r") as f:
                        data = json.loads(f.read())
                        Gamerinfo = data
                    for i in Gamerinfo:
                        if i['UserID'] == str(userid):
                            i['Squad'] = squad
                    with open(metadatajson,"w") as g:
                        json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                        g.close()
                    message = "<@"+ str(userid) + "> Player #" + str(playerid) + " has assigned to number " + str(pos) + "\n"
                    a = 1
                    for i in squad:
                        if i != "":
                            playeridvalue = i
                            with open(playeridjson) as f:
                                data = json.loads(f.read())
                                Playerinfo = data["HolyShxxtPlayers"]
                                Playerid = int(playeridvalue)
                                Playerinfoid = Playerinfo[Playerid]
                                Position = Playerinfoid['Position']
                                Rating = Playerinfoid['Rating']
                                message = message + str(a) + ": Player #" + str(i) + " (" + str(Rating) + "* " + str(Position) + ")\n"
                        if i == "":
                            message = message + str(a) + ": Player #" + str(i) +"\n"
                        a = a + 1
                    os.chdir(formationimage)
                    await interaction.response.send_message(message, file=discord.File(str(form)+".png"))

                    
@client.tree.command(name="gm", description="Get Daily Reward")
async def gm(interaction:discord.Interaction):
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            found = True
            lastDailytime = i['LastDailyTime']
            money = i['Money']
    if found == False:
        message = "Cannot find your gamer profile.\n Please create a profile using /create"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'GM')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    elif found == True:
        currenttime = time.time()
        timegap = int(currenttime) - int(lastDailytime)
        if  timegap < 86400:
            if (int(lastDailytime) + 86400 - int(currenttime))/3600 != 0:
                message = "Please claim again after " + str(round((int(lastDailytime) + 86400 - int(currenttime))/3600) ) + " hours."
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'GM')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
            else:
                message = "Please claim again after 1 hour."
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'GM')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
        elif timegap >= 86400:
            f.close()
            ran = random.randint(1,100)
            if ran <= 95:
                Daily = random.randint(1000,5000)
            elif ran <= 100:
                Daily = random.randint(1000,20000)
            print(Daily)
            with open(metadatajson,"r") as f:
                data = json.loads(f.read())
                Gamerinfo = data
            for i in Gamerinfo:
                if i['UserID'] == str(userid):
                    i['Money'] = money + Daily
            print(Gamerinfo)
            with open(metadatajson,"w") as f:
                json.dump(Gamerinfo, f,indent=4, separators=(',',':'))
                f.close()
            with open(metadatajson,"r") as g:
                gdata = json.loads(g.read())
                Gamerinfo = gdata
                for i in Gamerinfo:
                    if i['UserID'] == str(userid):
                        i['LastDailyTime'] = str(int(currenttime))
                g.close()
            with open(metadatajson,"w") as g:
                json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                g.close()
            message = "get the Daily of $" + str("{:,}".format(int(Daily))) +".\n \n"
            message = message + "You now have $" + str("{:,}".format(int(money+Daily)))
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'GM')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)                  
                
@client.tree.command(name="match", description="Match with Your Opponent")
@app_commands.describe(opponent = "@ Your Opponent")
async def match(interaction:discord.Interaction, opponent:str):
    channel = interaction.channel
    userid = interaction.user.id
    opponentid = opponent.replace("<@", "")
    opponentid = opponentid.replace(">", "")
    if str(userid) == str(opponentid):
        message = "You cannot compete with yourself."
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Match')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    else:
        with open(metadatajson,"r") as f:
          data = json.loads(f.read())
          Gamerinfo = data
        found = False
        for i in Gamerinfo:
            if i['UserID'] == str(userid):
                found = True
                hometeam = i['Squad']
                homeformation = i['Formation']
                money = i['Money']
                lastmatchtime = i['LastMatchTime']
        if found == False:
            message = "Cannot find your gamer profile.\n Please create a profile using /create."
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Match')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)                  
        else:
            currenttime = time.time()
            timegap = int(currenttime) - int(lastmatchtime)
            if  timegap < 1800:
                message = "Please start a match again after " + str(round((int(lastmatchtime) + 1800 - int(currenttime))/60) ) + " minutes."
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'Match')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox) 
            elif timegap >= 1800:
                [-- Match Algo --]

@client.tree.command(name="help", description="Show Helps for the Bot")
async def help(interaction:discord.Interaction):
    channel = interaction.channel
    userid = interaction.user.id
    message = "/create - Create initial gamer profile \n \n "
    message = message + "/show [Playerid] - Show data of the player \n \n "
    message = message + "/freemint - Claim free player each hour \n \n "
    message = message + "/gm - Claim daily reward \n \n "
    message = message + "/mint [Playerid] - Buy player \n \n "
    message = message + "/burn [Playerid] - Sell player \n \n "
    message = message + "/formation  - Set the formation of your squad \n \n "
    message = message + "/squad - Set your team squad \n \n "
    message = message + "/list - List all players in your club \n \n "
    message = message + "/match [Opponent] - Match with other team \n \n "
    message = message + "/money - Check your current balance \n \n "
    message = message + "/cooldown - Check the cooldown of action \n \n "
    message = message + "/blessing - Pay $10,000 to get the blessing \n \n "
    messagebox = discord.Embed(color = 0xff0000)
    messagebox.set_author(name = f'Help')
    username = client.get_user(userid)
    messagebox.add_field(name= username, value = message, inline = False)
    messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
    await interaction.response.send_message(embed = messagebox)

@client.tree.command(name="cooldown", description="Show Cooldown of the Commands")
async def cooldown(interaction:discord.Interaction):
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            found = True
            lastmatchtime = i['LastMatchTime']
            lastclaimtime = i['LastClaimTime']
            lastdailytime = i['LastDailyTime']
    if found == True:
        currenttime = time.time()
        matchwaittime = int(currenttime) - int(lastmatchtime)
        if matchwaittime >= 1800:
            message = 'Match: \n **Ready** \n \n'
        else:
            message = "Match: \n" + str(round((int(lastmatchtime) + 1800 - int(currenttime))/60) ) + " minutes \n \n"
        freemintwaititme = int(currenttime) - int(lastclaimtime)
        if freemintwaititme >= 3600:
            message = message + 'Freemint: \n **Ready** \n \n'
        else:
            message = message + "Freemint: \n" + str(round((int(lastclaimtime) + 3600 - int(currenttime))/60)) + " minutes \n \n"
        gmwaittime = int(currenttime) - int(lastdailytime)
        if gmwaittime >= 86400:
            message = message + 'GM: \n **Ready** \n \n'
        else:
            message = message + "GM: \n" + str(round((int(lastdailytime) + 86400 - int(currenttime))/3600) ) + " hours \n \n"  
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Cooldown')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    else:
        message = "Cannot find your gamer profile.\n Please create a profile using /create."
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Cooldown')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    f.close()

@client.tree.command(name="airdrop")
async def airdrop(interaction:discord.Interaction, guest:str, amount:int):
    channel = interaction.channel
    userid = interaction.user.id
    guestid = guest.replace("<@", "")
    guestid = guestid.replace(">", "")
    receiver = str(guestid)
    reward = int(amount)
    if str(userid) == str(477467813640929310):
        with open(metadatajson,"r") as f:
          data = json.loads(f.read())
          Gamerinfo = data
        for i in Gamerinfo:
            if i['UserID'] == str(receiver):
                money = i['Money']
                i['Money'] = money + reward
        with open(metadatajson,"w") as f:
            json.dump(Gamerinfo, f,indent=4, separators=(',',':'))
            f.close()
        message = "$" + str("{:,}".format(int(reward))) + " has been airdropped to <@" + str(receiver) +">"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Airdrop')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)                
    else:
        message = "You don't have permission to use this command"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'Airdrop')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    f.close()

@client.tree.command(name="blessing", description="Pay $10,000 - Win Big or Nothing")
async def blessing(interaction:discord.Interaction):
    channel = interaction.channel
    userid = interaction.user.id
    with open(metadatajson,"r") as f:
      data = json.loads(f.read())
      Gamerinfo = data
    found = False
    for i in Gamerinfo:
        if i['UserID'] == str(userid):
            found = True
            money = i['Money']
    if found == False:
        message = "Cannot find your gamer profile.\n Please create a profile using /create"
        messagebox = discord.Embed(color = 0xff0000)
        messagebox.set_author(name = f'GM')
        username = client.get_user(userid)
        messagebox.add_field(name= username, value = message, inline = False)
        messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
        await interaction.response.send_message(embed = messagebox)
    elif found == True:
        if  int(money) < 10000:
            message = "You don't have enough money."
            messagebox = discord.Embed(color = 0xff0000)
            messagebox.set_author(name = f'Blessing')
            username = client.get_user(userid)
            messagebox.add_field(name= username, value = message, inline = False)
            messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
            await interaction.response.send_message(embed = messagebox)
        elif int(money) >= 10000:
            f.close()
            ran = random.randint(1,100)
            if ran <= 5:
                blessing = 100000
            elif ran <= 40:
                blessing = 15000
            else: blessing = 0
            with open(metadatajson,"r") as f:
                data = json.loads(f.read())
                Gamerinfo = data
            for i in Gamerinfo:
                if i['UserID'] == str(userid):
                    i['Money'] = money - 10000 + blessing
            with open(metadatajson,"w") as g:
                json.dump(Gamerinfo, g,indent=4, separators=(',',':'))
                g.close()
            if blessing == 0:
                message = "lose $10,000 in the blessing \n \n"
                message = message + "You now have $" + str("{:,}".format(int(money+blessing)))
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'Blessing')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
            elif blessing == 15000:
                message = "get the blessing of $15,000 \n \n"
                message = message + "You now have $" + str("{:,}".format(int(money+blessing)))
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'Blessing')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
            else:
                message = "get the blessing of $100,000 \n \n"
                message = message + "You now have $" + str("{:,}".format(int(money+blessing)))
                messagebox = discord.Embed(color = 0xff0000)
                messagebox.set_author(name = f'Blessing')
                username = client.get_user(userid)
                messagebox.add_field(name= username, value = message, inline = False)
                messagebox.set_footer(text = f'HolyShxxt Card Fantasy')
                await interaction.response.send_message(embed = messagebox)
                
client.run([Token])
