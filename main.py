import os
import discord
import json
from dotenv import load_dotenv
from numpy import random
from webserver import keep_alive
from discord.ext import commands
from randomTexts import helpText, helloTexts, emoteIDs, niceTexts, kindaNiceTexts, strangerTexts, kindaHateTexts, hateTexts
import billaUtils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
billaBot = commands.Bot(command_prefix='billa ')
billaBot.remove_command('help')

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
songQueueMap = dict({})
emotes = []

@billaBot.event
async def on_ready() : 
    for emoteID in emoteIDs:
        emotes.append(billaBot.get_emoji(emoteID))
    userSynergy = dict({})
    with open('synergy.json','w') as file :
        json.dump(userSynergy,file)
    print(f'{billaBot.user} has connected to Discord!')

@billaBot.event
async def on_message(message) :
    if message.content.find('?') != -1 and len(message.content) > 1 :
        lottery = random.randint(1,10)
        if lottery <= 3 :
            await message.add_reaction(random.choice(emotes))

    if message.content.lower().startswith('hello billa') and len(message.content) > 12 :
        response = random.choice(helloTexts)
        with open('synergy.json') as file :
            userSynergy = json.load(file)
        if message.author.id in userSynergy :
            userSynergy[str(message.author.id)] += response['points']
        else :
            userSynergy[str(message.author.id)] = 0
            userSynergy[str(message.author.id)] += response['points']
        with open('synergy.json','w') as jsonFile :
            json.dump(userSynergy,jsonFile)
        await message.channel.send(content=response['text'])

    await billaBot.process_commands(message)

@billaBot.command(name='help')
async def billaHelp(ctx) : 
    await billaUtils.sendEmbed(ctx=ctx,title='BillaBot Commands',description=helpText)

@billaBot.command(name='mybro')
async def billaMyBro(ctx) :
    userSynergy = None
    with open('synergy.json') as file :
        userSynergy = json.load(file)
    try :
        synergy = userSynergy[str(ctx.author.id)]
        response = ''
        if synergy == 0 :
            response = random.choice(strangerTexts) + ' :neutral_face::pinched_fingers:'
        elif synergy > 0 and synergy <= 20 :
            response = random.choice(kindaNiceTexts) + ' :smiley_cat::thumbsup:'
        elif synergy > 20 :
            response = random.choice(niceTexts) + ' :heart_eyes_cat::blue_heart:'
        elif synergy < 0 and synergy >= -20 :
            response = random.choice(kindaHateTexts) + ' :crying_cat_face::thumbsdown:'
        elif synergy < -20 :
            response = random.choice(hateTexts) + ' :pouting_cat::punch:'
        await billaUtils.sendEmbed(ctx=ctx,title=ctx.author.name,description=response+f'\nSynergy : {synergy}:star:')
    except :
        await billaUtils.sendEmbed(ctx=ctx,title=ctx.author.name,description=random.choice(strangerTexts) + ' :neutral_face::pinched_fingers:' + f'\nSynergy : 0:star:')

@billaBot.command(name='join')
async def billaJoin(ctx) : 
    if await billaUtils.checkVoiceExceptions(billaBot,ctx,'join') :
        return
    voiceClient = billaUtils.getVoiceClient(billaBot,ctx)
    voiceChannel = ctx.author.voice.channel
    if voiceClient is None : 
        voiceClient = await voiceChannel.connect()
    joinTexts = ['I am ready',f'Joined {voiceChannel.name}',f'Connected to {voiceChannel.name}']
    await billaUtils.echo(ctx=ctx,voiceClient=voiceClient,message=random.choice(joinTexts)) 
    await billaUtils.sendEmbed(ctx=ctx,title='',description=f'Joined {voiceChannel.name}')

@billaBot.command(name='play')
async def billaPlay(ctx) :
    if await billaUtils.checkVoiceExceptions(billaBot,ctx,'play') :
        return
    voiceClient = billaUtils.getVoiceClient(billaBot,ctx)
    voiceChannel = ctx.author.voice.channel
    if voiceClient is None : 
        voiceClient = await voiceChannel.connect()
    songName = ctx.message.content[11:]
    song = billaUtils.searchSong(songName)
    songTitle = song['title']

    if ctx.guild.name in songQueueMap :
        songQueueMap[ctx.guild.name].append(song)
    else : 
        songQueueMap[ctx.guild.name] = []
        songQueueMap[ctx.guild.name].append(song)

    if not voiceClient.is_playing() :    
        await billaUtils.sendEmbed(ctx=ctx,title='Playing',description=f'{songTitle}')
        audio = discord.FFmpegPCMAudio(songQueueMap[ctx.guild.name][0]['source'],**FFMPEG_OPTIONS)
        voiceClient.play(audio,after=lambda e : billaUtils.playNextSong(ctx,voiceClient,songQueueMap))
        voiceClient.is_playing()        
    else :
        await billaUtils.sendEmbed(ctx=ctx,title='Queued',description=f'{songTitle}')

@billaBot.command(name='skip')
async def billaSkip(ctx) :
    if await billaUtils.checkVoiceExceptions(billaBot,ctx,'skip') :
        return 
    voiceClient = billaUtils.getVoiceClient(billaBot,ctx)
    voiceChannel = ctx.author.voice.channel
    if len(songQueueMap[ctx.guild.name]) > 0 :
        songTitle = songQueueMap[ctx.guild.name][0]['title']
        await voiceClient.disconnect()
        voiceClient = await voiceChannel.connect()
        await billaUtils.sendEmbed(ctx=ctx,title='Skipped',description=songTitle)
        if len(songQueueMap[ctx.guild.name]) > 0 :
            voiceClient.play(discord.FFmpegPCMAudio(songQueueMap[ctx.guild.name][0]['source'],**FFMPEG_OPTIONS),after=lambda e: billaUtils.playNextSong(ctx,voiceClient,songQueueMap))
    else :
        await billaUtils.sendEmbed(ctx=ctx,title='',description='Nothing to skip.')

@billaBot.command(name='remove')
async def billaRemove(ctx,arg) :
    if await billaUtils.checkVoiceExceptions(billaBot,ctx,'remove') :
        return
    voiceClient = billaUtils.getVoiceClient(billaBot,ctx)
    voiceChannel = ctx.author.voice.channel
    if arg.isnumeric() :
        if int(arg) > len(songQueueMap[ctx.guild.name]) or int(arg) < 1 :
            await billaUtils.sendEmbed(ctx=ctx,title='Invalid argument',description='Index position out of bounds.')
            return
        if int(arg) == 1 :
            await billaUtils.sendEmbed(ctx=ctx,title='',description='Just use skip instead smh.')
            return
        songTitle = songQueueMap[ctx.guild.name][int(arg)-1]['title']
        del songQueueMap[ctx.guild.name][int(arg)-1]
        await billaUtils.sendEmbed(ctx=ctx,title='Removed',description=f'{songTitle}')
    else :
        await billaUtils.sendEmbed(ctx=ctx,title='Invalid argument',description='Please enter a valid index position.')

@billaBot.command(name='queue')
async def billaQueue(ctx) :
    if ctx.guild.name in songQueueMap :
        queue = ''
        i = 1
        for song in songQueueMap[ctx.guild.name] :
            queue += str(i) + '. ' + song['title'] + '\n'
            i+=1
        await billaUtils.sendEmbed(ctx=ctx,title=f'{ctx.guild.name} Queue',description=queue)
    else :
        await billaUtils.sendEmbed(ctx=ctx,title='',description='Nothing queued.')

@billaBot.command(name='echo')
async def billaEcho(ctx) : 
    if await billaUtils.checkVoiceExceptions(billaBot,ctx,'echo') :
        return
    voiceClient = billaUtils.getVoiceClient(billaBot,ctx)
    voiceChannel = ctx.author.voice.channel
    if voiceClient is None : 
        voiceClient = await voiceChannel.connect()
    await billaUtils.echo(ctx,voiceClient,ctx.message.content[11:])

@billaBot.command(name='disconnect')
async def billaDisconnect(ctx) : 
    if await billaUtils.checkVoiceExceptions(billaBot,ctx,'disconnect') :
        return
    voiceClient = billaUtils.getVoiceClient(billaBot,ctx)
    if ctx.guild.name in songQueueMap : 
        songQueueMap[ctx.guild.name] = []
    await voiceClient.disconnect()
    await billaUtils.sendEmbed(ctx=ctx,title='',description='Disconnected')

@billaBot.command(name='kick')
async def billaKick(ctx) : 
    await billaUtils.sendGif(ctx=ctx,term='kick')

@billaBot.command(name='punch')
async def billaPunch(ctx) : 
    await billaUtils.sendGif(ctx=ctx,term='punch')

@billaBot.command(name='slap')
async def billaSlap(ctx) : 
    await billaUtils.sendGif(ctx=ctx,term='slap')

keep_alive()
billaBot.run(TOKEN)