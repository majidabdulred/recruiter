"""
Hello this is created by majidabdulred. Below is the structural documentation of the program.

Variables:
    recruits:[] To store id of recruits.
    data:{} To store the data of the recruits.It contains one more dict which has keys given below:
        steps: Stores the steps recruiter has completed.
        username: Username.
        playstyle: Playstyle.
        screenshot_link: Link of the screenshot.
        comment: A comment

Flow of code:
    1)Whenever a member joins on_member_join() is triggered a channel is created in Recruits category with the name of the the user (like a ticket)) and a message is send.
    2)On getting the reaction on_raw_reaction add and checking it on_intro()
    3)Like wise every function runs controlled by the steps the user has completed.

Steps:
    This is the important key stored in data[<theusername>].
    If on_intro() function has ran the users steps is changed to 1.
    If add_username() function has ran the users steps is changed to 2.
    If add_playstyle() function has ran the users steps is changed to 3.
    If add_screenshot() function has ran the users steps is changed to 4.
    If add_comment() function has ran the users steps is changed to 5.

"""

import discord
import os
intent = discord.Intents.default()
intent.members = True
intent.typing = False

client = discord.Client(intents=intent)

recruits = []
data = {}
thecategory = 0
hrs = []
the_HR_role = 0
#theguildid = "632799582350475265" # Bot test server
theguildid = "745346902287188138" # True Grit


roles_for_hr = ["CEO","High Command","Corp Affairs Officer","HR"]

the_welcome_message="""Welcome! Just to go over a few things about GRIT.

We are Half-Indy, Half-PvP based (split into two corporations, GRIT for Indy/Mining/Trade and GR1T gritheads for PvP/PvE/Ratting). We do not have strict orders for people to play a certain way. Play how you want in either corporation and support the corporation when needed. That being said, we do have some requirements.
-------------------------------------------------------------
1. Do not be an asshole to corp members or alliance members, If something comes up. If someone says something dumb. If you get into an argument. Bring it over to @Corp Affairs Officer  or @Enoka and we will handle it

 2. Do not talk in local chat while out in Null-Sec All 1,000+ players in the alliance follows this rule. There are problems with the reporting system and it can lead to enemies spam reporting you and getting you banned. Just don’t.

3. Always pay attention to LOCAL while in null sec, it is not required but we do hope that you can post updated information on if you see reds/neuts in our system

4. We follow a Not Blue Shoot It policy meaning anyone who doesn't show as Green / Purple / Blue is free game to kill.

5. During a Fleet op or a CTA discord VOICE CHAT IS MANDATORY. This is for your safety. Just listen, if you can’t listen- don’t join the fleet op. We don’t want you dying and losing your ship because you were unable to organize with the fleet.
-------------------------------------------------------------"""

the_accpet_letter = """"[GRIT] ACCEPTANCE LETTER - PLEASE READ COMPLETELY

— PLEASE READ: ABOUT US —

Corporation Headquarters:  CZDJ-1 < DEKLEIN (North, Caldari)
Alliance Citadel: RG9-7U (Next to Corporation Headquarters)

— PLEASE READ: DISCORD —

Have a look through our discord server! 

- Specifically the "#about-us”,  and “#corp-announcements” channels are a great way to learn about our corporation and stay up to date on Corporation information

- If you have any questions please ping @Corp Affairs Officer  on discord, we will answer them to the best of our ability

— PLEASE READ: Fleet Doctrine — (Fleet doctrines will be reimbursed if lost during fleet ops)

Mandatory
https://docs.google.com/spreadsheets/d/15-HyOz-hCVI03cXMl2ngn3Iw1MvQVBc6XrWEYfE0Pto/edit?usp=sharing
https://docs.google.com/spreadsheets/d/1vGjTBW_tLRtusEohZIOmdtvCY_lYGV5HoZihTOuDhDM/edit?usp=sharing
https://docs.google.com/document/d/1Iulb8-2_2F10wwUBl-uY4nvSHNEQ4WsS5DPj76XdKrE/edit?usp=sharing

Optional
https://docs.google.com/document/d/1CS0ox5nuk4-WwjsMDEadg5UKxb4ammsPa40XylC9ksk/edit?usp=sharing
https://docs.google.com/document/d/1v6z626knWFoda5cNmuuPU3BRPNOOFjy7rghKg4PNBuI/edit?usp=sharing


JOIN ALLIANCE DISCORD - https://discord.gg/g4K6qrs

upon joining the alliance discord change your nickname to [GRIT] your name

Then react with "2" and say "requesting access"""

@client.event
async def on_ready():

    global the_HR_role,theredman, theguild, logsch , thecategory,hrs

    theguild = client.get_guild(int(theguildid)) # The Server
    logsch = client.get_guild(632799582350475265).get_channel(763674672105259008) #log channel in Bot test server for sending logs
    print("Started")

    # Crating the list of HR in the server
    for i in theguild.roles:
        if i.name in roles_for_hr:
            for j in i.members:
                hrs.append(j.id)
    print(hrs)
    the_HR_role = theguild.get_role(764360399977971722)
    for i in theguild.by_category():
        try:
            if i[0].name == "Recruits":
                thecategory = i[0] # The Recruits category (I didnt found any function like theguild.get_category(id))
                print("The category =",thecategory)
                break
        except:
            continue
    print("Ready")

@client.event
async def on_member_join(member):
    global data
    global recruits
    print("member joined")
    perm = discord.PermissionOverwrite(attach_files=True,embed_links=True ,read_message_history=True,read_messages=True,send_messages=True,add_reactions=True,manage_channels=True,manage_permissions=True)
    overwrites ={
        member: discord.PermissionOverwrite(attach_files=True,embed_links=True ,read_message_history=True,read_messages=True,send_messages=True,add_reactions=True,),
        theguild.default_role: discord.PermissionOverwrite(read_messages=False),
        theguild.me: perm,
        the_HR_role: perm} # Permission rules for the channel that will be created

    try:
        mem_ch = await theguild.create_text_channel(member.name,category=thecategory, overwrites=overwrites) # Creating a new channel for all purposes
    except Exception as E:
        print(E)
    print("A channel created")
    mem_mes = await mem_ch.send(f"{member.mention}",embed=discord.Embed(
        description="Welcome!, Hello looking to join?"))
    thename = str(member)
    data[thename] = {}
    data[thename]["steps"] = 0
    recruits.append(member.id)
    await mem_mes.add_reaction("\U00002714")
    await mem_mes.add_reaction("\U0000274C")
    await logsch.send("[+]{} joined the server . Sent the greet message".format(member.name))



@client.event
async def on_message(message):
    global data
    global recruits
    theuser = str(message.author)


    if message.author.bot or message.author.id == 757099374261305385: # Not a bot
        return

    if message.channel.id == 763674672105259008 and "!log" in message.content: # If its a message in log_recruits channels
        print("Devmode", message.content)
        await devmode(message)
        return

    if message.channel.category_id not in (766897112632918036,745346902287188140) :
        return

    print(str(message.author.name), " said :", message.content)

    if message.author.id in recruits:
        await logsch.send("{} : {}".format(message.author.name, message.content))
        if data[theuser]["steps"] == 1:
            await add_username(message, theuser)
        elif data[theuser]["steps"] == 2:
            await add_playstyle(message, theuser)
        elif data[theuser]["steps"] == 3:
            await add_screenshot(message, theuser)
        elif data[theuser]["steps"] == 4:
            await add_comment(message, theuser)
    elif message.channel.category_id == 766897112632918036 and message.author.id in hrs:
        if message.content == "!accept" :
            await message.channel.send(the_accpet_letter)
        elif message.content == "!close":
            await message.channel.delete(reason="Interview ended")


@client.event
async def on_raw_reaction_add(payload):
    global recruits
    global data
    theuser = client.get_user(payload.user_id)
    if theuser.bot or payload.user_id == 757099374261305385 or payload.channel_id == 763674672105259008:
        return

    await logsch.send("{} reacted with {}".format(theuser.name, payload.emoji))
    print(theuser, recruits)
    if theuser.id in recruits:
        thechannel = client.get_channel(payload.channel_id)
        theuser = str(theuser)
        if data[theuser]["steps"] == 0:
            if payload.emoji.name == "\U00002714":
                await on_intro(thechannel)
                data[theuser]["steps"] = 1
                return
            elif payload.emoji.name == "\U0000274C":
                await thechannel.send("No problem!")
            else:
                pass
                await thechannel.send("Please react with the given emojis")


@client.event
async def on_intro(thechannel):
    await thechannel.send(the_welcome_message)
    await thechannel.send(
        embed=discord.Embed(
            description="Hey I will just do your verification process then an HR will contact you. If you want to ask any questions or anything like that,  everything after the verification\nSo please co-ordinate with me."
                        "Please send your username in the format:.\n!u <username>\nExamples:\n!u "
                            "majidabdulred\n!u thename"))
    await logsch.send("Send welcome message to {}".format(thechannel.name))


@client.event
async def add_username(message, theuser):
    global data
    if "!u" in message.content or "!U" in message.content:
        data[theuser]["username"] = message.content.lstrip("!u")
        data[theuser]["steps"] = 2
        await message.channel.send(
            embed=discord.Embed(
                description="Thanks.\nNow please send your playstyle in format\n!t pve,pvp,miner,industry,"
                            "hauler\nExamples:\n"
                            "!t miner,pve\n!t pvp,industry\n!t pve,hauler"))
        await logsch.send("[+]Added username : {} : {}".format(theuser, message.content.lstrip("!u")))
    else:
        await message.channel.send(
            embed=discord.Embed(
                description="Please write your username in correct format.\n!u <username>\nExamples:\n!u "
                            "majidadublred\n!u thename"))
        await logsch.send("[-]Wrong username format send the retry message to {}".format(theuser))


@client.event
async def add_playstyle(message, theuser):
    global data
    if "!t" in message.content or "!T" in message.content:
        data[theuser]["playstyle"] = message.content[2:]
        data[theuser]["steps"] = 3
        await message.channel.send(embed=discord.Embed(
            description="Thanks.\nNow please send your in-game profile screenshot'''\nLike this.(or send anything "
                        "because this is Testing) ").set_image(
            url="https://cdn.discordapp.com/attachments/745295219175456888/761944550825918495/IMG-20201003-WA0036.jpg"))
        await logsch.send("[+]Added playstyle : {} : {}".format(theuser, message.content.lstrip("!t")))

    else:
        await message.channel.send(
            embed=discord.Embed(
                description=" Please write playstyle in correct format.\n!t pve,pvp,miner,industry,hauler\nExamples:\n"
                            "!t miner,pve\n!t pvp,industry\n!t pve,hauler"))
        await logsch.send("[-]Wrong playstyle format send the retry message to {}".format(theuser))


@client.event
async def add_screenshot(message, theuser):
    global data
    if len(message.attachments) > 0:
        data[theuser]["screenshot_link"] = message.attachments[0].url
        data[theuser]["steps"] = 4
        await message.channel.send(
            embed=discord.Embed(
                description="You interview is almost completed.\nJust tell something about you.\nFormat:\n!c your "
                            "comment goes here.\nExamples\n!c Hi I am a good eve echoes  player trying to live in "
                            "this world.\n!c Hey . I just want to move to null sec as soon as possible."))
        await logsch.send("[+]Added screenshot : {}".format(theuser))

    else:
        await message.channel.send(embed=discord.Embed(description=" PLease send the screenshot"))
        await logsch.send("[-]Didnt send the ss send the retry message to {}".format(theuser))


@client.event
async def add_comment(message, theuser):
    global data
    if "!c" in message.content or "!C" in message.content:
        data[theuser]["comment"] = message.content.lstrip("!c")
        data[theuser]["steps"] = 5
        await logsch.send("[+]Sending report of {}".format(theuser))

        await send_report(message, theuser)


@client.event
async def send_report(message, theuser):
    print("Generating Report")
    embed = discord.Embed(title=f"__{message.author}__",
                          type="rich",
                          description=f"Hey {message.author} wants to join our corp. \nUsername : {data[theuser]['username']}\nPlaystyle : {data[theuser]['playstyle']}\n{data[theuser]['comment']}",
                          colour=discord.Colour.blue())
    embed.set_image(url=f"{data[theuser]['screenshot_link']}")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/745295219175456888/760487391151652884/PicsArt_09-29-09.59.35.png")
    embed.set_author(name="Application",
                     url="https://cdn.discordapp.com/attachments/745295219175456888/760487391151652884/PicsArt_09-29-09.59.35.png")
    await message.channel.send(embed=embed)
    await message.channel.send("Thanks Now wait till an HR comes and contacts you.")
    del data[theuser]


@client.event
async def devmode(message):
    con = message.content
    if "var" in con:
        if "data" in con:
            await logsch.send(data)
        if "recruit" in con:
            await logsch.send(recruits)


token = os.environ['token']

client.run(token)
