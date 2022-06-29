import os
import discord
import json
from dotenv import load_dotenv
from numpy import random
from discord.ext import commands
from randomTexts import (
    helpText,
    helloTexts,
    emoteIDs,
    niceTexts,
    kindaNiceTexts,
    strangerTexts,
    kindaHateTexts,
    hateTexts,
    rpsEmotes,
)
from billaUtils import (
    sendEmbed,
    sendGif,
    echo,
    getVoiceClient,
    searchSong,
    playNextSong,
    checkVoiceExceptions,
    getLiveMatches,
    getImage,
)
from PIL import Image
from io import BytesIO
import requests

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True
intents.messages = True
billaBot = commands.Bot(command_prefix="billa ", intents=intents)
billaBot.remove_command("help")

discord.opus.load_opus()

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}
songQueueMap = dict({})
emotes = []


@billaBot.event
async def on_ready():
    for emoteID in emoteIDs:
        emotes.append(billaBot.get_emoji(emoteID))
    print(f"{billaBot.user} has connected to Discord!")
    await billaBot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"over {len(billaBot.guilds)} servers",
        )
    )


@billaBot.event
async def on_message(message):
    if message.content.find("?") != -1 and len(message.content) > 1:
        lottery = random.randint(1, 10)
        if lottery <= 3:
            await message.add_reaction(random.choice(emotes))

    if message.content.lower().startswith("hello billa") and len(message.content) > 12:
        response = random.choice(helloTexts)
        await message.channel.send(content=response["text"])

    await billaBot.process_commands(message)


@billaBot.command(name="help")
async def billaHelp(ctx):
    await sendEmbed(ctx=ctx, title="BillaBot Commands", description=helpText)


@billaBot.command(name="join")
async def billaJoin(ctx):
    if await checkVoiceExceptions(billaBot, ctx, "join"):
        return
    voiceClient = getVoiceClient(billaBot, ctx)
    voiceChannel = ctx.author.voice.channel
    if voiceClient is None:
        voiceClient = await voiceChannel.connect()
    joinTexts = [
        "I am ready",
        f"Joined {voiceChannel.name}",
        f"Connected to {voiceChannel.name}",
    ]
    await echo(ctx=ctx, voiceClient=voiceClient, message=random.choice(joinTexts))
    await sendEmbed(ctx=ctx, title="", description=f"Joined {voiceChannel.name}")


@billaBot.command(name="play")
async def billaPlay(ctx):
    if await checkVoiceExceptions(billaBot, ctx, "play"):
        return
    voiceClient = getVoiceClient(billaBot, ctx)
    voiceChannel = ctx.author.voice.channel
    if voiceClient is None:
        voiceClient = await voiceChannel.connect()
    songName = ctx.message.content[11:]
    song = searchSong(songName)
    songTitle = song["title"]

    if ctx.guild.name in songQueueMap:
        songQueueMap[ctx.guild.name].append(song)
    else:
        songQueueMap[ctx.guild.name] = []
        songQueueMap[ctx.guild.name].append(song)

    if not voiceClient.is_playing():
        await sendEmbed(ctx=ctx, title="Playing", description=f"{songTitle}")
        audio = discord.FFmpegPCMAudio(
            songQueueMap[ctx.guild.name][0]["source"], **FFMPEG_OPTIONS
        )
        voiceClient.play(
            audio, after=lambda e: playNextSong(ctx, voiceClient, songQueueMap)
        )
        voiceClient.is_playing()
    else:
        await sendEmbed(ctx=ctx, title="Queued", description=f"{songTitle}")


@billaBot.command(name="skip")
async def billaSkip(ctx):
    if await checkVoiceExceptions(billaBot, ctx, "skip"):
        return
    voiceClient = getVoiceClient(billaBot, ctx)
    voiceChannel = ctx.author.voice.channel
    if len(songQueueMap[ctx.guild.name]) > 0:
        songTitle = songQueueMap[ctx.guild.name][0]["title"]
        await voiceClient.disconnect()
        voiceClient = await voiceChannel.connect()
        await sendEmbed(ctx=ctx, title="Skipped", description=songTitle)
        if len(songQueueMap[ctx.guild.name]) > 0:
            voiceClient.play(
                discord.FFmpegPCMAudio(
                    songQueueMap[ctx.guild.name][0]["source"], **FFMPEG_OPTIONS
                ),
                after=lambda e: playNextSong(ctx, voiceClient, songQueueMap),
            )
    else:
        await sendEmbed(ctx=ctx, title="", description="Nothing to skip.")


@billaBot.command(name="remove")
async def billaRemove(ctx, arg):
    if await checkVoiceExceptions(billaBot, ctx, "remove"):
        return
    if arg.isnumeric():
        if int(arg) > len(songQueueMap[ctx.guild.name]) or int(arg) < 1:
            await sendEmbed(
                ctx=ctx,
                title="Invalid argument",
                description="Index position out of bounds.",
            )
            return
        if int(arg) == 1:
            await sendEmbed(ctx=ctx, title="", description="Just use skip instead smh.")
            return
        songTitle = songQueueMap[ctx.guild.name][int(arg) - 1]["title"]
        del songQueueMap[ctx.guild.name][int(arg) - 1]
        await sendEmbed(ctx=ctx, title="Removed", description=f"{songTitle}")
    else:
        await sendEmbed(
            ctx=ctx,
            title="Invalid argument",
            description="Please enter a valid index position.",
        )


@billaBot.command(name="queue")
async def billaQueue(ctx):
    if ctx.guild.name in songQueueMap:
        queue = ""
        i = 1
        for song in songQueueMap[ctx.guild.name]:
            queue += str(i) + ". " + song["title"] + "\n"
            i += 1
        await sendEmbed(ctx=ctx, title=f"{ctx.guild.name} Queue", description=queue)
    else:
        await sendEmbed(ctx=ctx, title="", description="Nothing queued.")


@billaBot.command(name="echo")
async def billaEcho(ctx):
    if await checkVoiceExceptions(billaBot, ctx, "echo"):
        return
    voiceClient = getVoiceClient(billaBot, ctx)
    voiceChannel = ctx.author.voice.channel
    if voiceClient is None:
        voiceClient = await voiceChannel.connect()
    await echo(ctx, voiceClient, ctx.message.content[11:])


@billaBot.command(name="disconnect")
async def billaDisconnect(ctx):
    if await checkVoiceExceptions(billaBot, ctx, "disconnect"):
        return
    voiceClient = getVoiceClient(billaBot, ctx)
    if ctx.guild.name in songQueueMap:
        songQueueMap[ctx.guild.name] = []
    await voiceClient.disconnect()
    await sendEmbed(ctx=ctx, title="", description="Disconnected")


@billaBot.command(name="kick")
async def billaKick(ctx):
    await sendGif(ctx=ctx, term="kick")


@billaBot.command(name="punch")
async def billaPunch(ctx):
    await sendGif(ctx=ctx, term="punch")


@billaBot.command(name="slap")
async def billaSlap(ctx):
    await sendGif(ctx=ctx, term="slap")


@billaBot.command(name="rps")
async def billaRps(ctx):
    args = ctx.message.content.split(" ")[2:]
    if len(args) == 0:
        await sendEmbed(
            ctx=ctx, title="", description="Choose between rock, paper and scissors."
        )
    userChoice = args[0]
    botChoice = random.choice(["rock", "paper", "scissors"])
    result = ""
    if userChoice == botChoice:
        result = "Tie"
    elif (
        userChoice == "rock"
        and botChoice == "scissors"
        or userChoice == "paper"
        and botChoice == "rock"
        or userChoice == "scissors"
        and botChoice == "paper"
    ):
        result = f"{ctx.author.name} wins."
    else:
        result = "BillaBot wins."
    await sendEmbed(
        ctx=ctx,
        title=result,
        description=f"{rpsEmotes[userChoice]} {rpsEmotes[botChoice]}",
    )


@billaBot.command(name="live")
async def billaFooty(ctx):
    matches = getLiveMatches()
    await sendEmbed(ctx=ctx, title="Live Matches", description=matches)


@billaBot.command(name="hit")
async def billaImage(ctx):
    mentions = ctx.message.mentions
    if len(mentions) < 2:
        await sendEmbed(
            ctx=ctx, title="", description="Usage : billa hit @user1 @user2"
        )
        return
    avatar1 = Image.open(getImage(mentions[0].avatar_url)).resize((290, 290))
    avatar2 = Image.open(getImage(mentions[1].avatar_url)).resize((290, 290))
    background = Image.open("./images/slap.jpg")

    background.paste(avatar1, (580, 400))
    background.paste(avatar2, (70, 120))

    with BytesIO() as binary:
        background.save(binary, "PNG")
        binary.seek(0)
        await ctx.send(file=discord.File(fp=binary, filename="oye.png"))


@billaBot.command(name="weebify")
async def billaWeeb(ctx):
    att = ctx.message.attachments
    if len(att) < 1:
        await sendEmbed(ctx=ctx, title="", description="Attach an image to the command")
        return
    image = att[0]
    filename = image.filename
    extension = filename.split(".")[-1]
    await image.save(fp=f"{filename}.{extension}")
    res = requests.post(
        "https://api.deepai.org/api/toonify",
        files={"image": open(f"{filename}.{extension}", "rb")},
        headers={"api-key": "a67cea80-7e4a-4957-a2fe-8e824ddfc1c8"},
    )
    try:
        outputUrl = res.json()["output_url"]
    except Exception as e:
        await sendEmbed(ctx=ctx, title="", description="Invalid attachment")
        return
    weebImage = Image.open(getImage(outputUrl))
    with BytesIO() as binary:
        weebImage.save(binary, "PNG")
        binary.seek(0)
        await ctx.send(file=discord.File(fp=binary, filename=f"{filename}.{extension}"))
    if os.path.exists(f"{filename}.{extension}"):
        os.remove(f"{filename}.{extension}")


billaBot.run(DISCORD_TOKEN)
