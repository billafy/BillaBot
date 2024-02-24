import os
import discord
from dotenv import load_dotenv
from numpy import random
from discord.ext import commands
from get_gemini_response import generate_gemini_response
from get_google_images import get_google_images
from randomTexts import (
    helpText,
    helloTexts,
    emoteIDs,
    rpsEmotes,
    billaEmoteIds,
)
from billaUtils import (
    sendEmbed,
    sendGif,
    echo,
    getVoiceClient,
    checkVoiceExceptions,
    getLiveMatches,
    getImage,
    get_latest_conversation,
)
from PIL import Image
from io import BytesIO
import requests
from pagination import DiscordPagination
from datetime import datetime, timezone

load_dotenv()
intents = discord.Intents.all()
intents.members = True
intents.messages = True
billaBot = commands.Bot(command_prefix="billa ", intents=intents)
billaBot.remove_command("help")

emotes = []
billaEmotes = dict()
expression_string = ""
for expression in billaEmoteIds.keys(): 
    expression_string += expression
    expression_string += ", "

@billaBot.event
async def on_ready():
    for emoteID in emoteIDs:
        emotes.append(billaBot.get_emoji(emoteID))
    for expression in billaEmoteIds: 
        billaEmotes[expression] = billaBot.get_emoji(int(billaEmoteIds[expression]))
    for guild in billaBot.guilds:
        channel = guild.get_channel(528221649150017537)
        if channel:
            break
    print(f"{billaBot.user} has connected to Discord!")
    await billaBot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"over {len(billaBot.guilds)} servers",
        )
    )


@billaBot.event
async def on_message(message):
    if message.content.find("?") != -1 and len(message.content) > 1 and message.author.id != 776675605340094484:
        lottery = random.randint(1, 10)
        if lottery <= 3:
            await message.add_reaction(random.choice(emotes))

    is_lamify_mentioned = False
    for mention in message.mentions: 
        if mention.name == "lamify": 
            is_lamify_mentioned = True

    # if (
    #     (message.content.lower().find("lamify") != -1 or message.content.lower().find("yash") != -1 or message.content.lower().find("billa") != -1) and
    #     not is_lamify_mentioned and
    #     message.author.name != "lamify"
    # ):
    #     await message.channel.send(f'<@377832472697634817>')
    
    if message.content.lower().startswith("hello billa") and len(message.content) > 12: 
        conversation, users = await get_latest_conversation(message.channel, billaBot)
        query = conversation
        query += "\n"
        message_content = " ".join(message.content.split(" ")[2:])
        query += f'Query - {message_content}. Respond to this query in 1 to 3 short sentences. Take any context if needed from the above conversation. Do not repeat anything as it is from the conversation. Use UK roadman slang. Do not separate answer in points.'
        async with message.channel.typing(): 
            response = generate_gemini_response(query)
            emoji_query = f"Text - {response}. List of expressions - [{expression_string}]. Based on the text, tell which expression from list suits the text. Just send the expression name, nothing else at all."
            emoji_response = generate_gemini_response(emoji_query)
            
            if random.choice([1, 2, 3]) <= 2: 
                try: 
                    emoji = billaEmotes[emoji_response.lower()]
                    response += f" {emoji}"
                except: 
                    pass

            if len(response) == 0: 
                return

            if len(response) <= 2000:
                await message.channel.send(response)
            else:
                parts = [response[i:i + 2000] for i in range(0, len(response), 2000)]
                for part in parts:
                    await message.channel.send(part)

    if message.content.lower().startswith("hello billu") and len(message.content) > 12:        
        query = " ".join(message.content.split(" ")[2:])
        query = f'{query}. Give baby yoda language reply in 1 to 3 short sentences. Do not separate answer in points. Instead of Yoda or Baby Yoda call yourself Billu'

        async with message.channel.typing(): 
            response = generate_gemini_response(query)

            if len(response) == 0: 
                return

            if len(response) <= 2000:
                await message.channel.send(response)
            else:
                parts = [response[i:i + 2000] for i in range(0, len(response), 2000)]
                for part in parts:
                    await message.channel.send(part)

    await billaBot.process_commands(message)


@billaBot.command(name="help")
async def billaHelp(ctx):
    await sendEmbed(ctx=ctx, title="BillaBot Commands", description=helpText)

@billaBot.command(name="say")
async def billaSay(ctx): 
    content = ctx.message.content
    try: 
        await ctx.message.delete()
    except: 
        pass
    await ctx.channel.send(content.replace("billa say", "").strip())

@billaBot.command(name="echo")
async def billaEcho(ctx):
    if await checkVoiceExceptions(billaBot, ctx, "echo"):
        return
    voiceClient = getVoiceClient(billaBot, ctx)
    voiceChannel = ctx.author.voice.channel
    if voiceClient is None:
        voiceClient = await voiceChannel.connect()
    await echo(ctx, voiceClient, ctx.message.content[11:])

@billaBot.command(name="summary")
async def billaSummary(ctx): 
    conversation, users = await get_latest_conversation(ctx.channel, billaBot)
    query = conversation
    random_user = random.choice(list(users))
    query += f'Summarize the above conversation in 5 to 7 short sentences. Use UK roadman slang. Do not separate answer in points. Your name is BillaBot in this conversation. Only if the conversation is empty, roast {random_user} in a crazy way.'

    async with ctx.channel.typing(): 
        response = generate_gemini_response(query)

        if len(response) == 0: 
            return

        if len(response) <= 2000:
            await ctx.channel.send(response)
        else:
            parts = [response[i:i + 2000] for i in range(0, len(response), 2000)]
            for part in parts:
                await ctx.channel.send(part)

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


@billaBot.command(name="query")
async def billaQuery(ctx):
    args = ctx.message.content.split(" ")[2:]
    if len(args) == 0:
        await sendEmbed(ctx=ctx, title="", description="Enter a search query.")
        return
    query = " ".join(list(args))
    image_links = get_google_images(query)
    if len(image_links) == 0:
        await sendEmbed(ctx=ctx, title="", description="No results found.")
        return
    embeds = []
    for i in range(len(image_links)):
        embed = discord.Embed(title=image_links[i]["text"], url=image_links[i]["link"])
        embed.set_footer(text=f"Searching '{query}' - {i + 1}/{len(image_links)}")
        embed.set_image(url=image_links[i]["src"])
        embeds.append(embed)

    async def get_page(page: int):
        embed = embeds[page]
        return embed

    await DiscordPagination(ctx, get_page).navigate()


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


try: 
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    billaBot.run(DISCORD_TOKEN)
except discord.errors.HTTPException: 
    os.system("python restarter.py")
    os.system("kill 1")
