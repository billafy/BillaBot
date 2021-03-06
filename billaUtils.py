import discord
import requests
import json
import youtube_dl
from numpy import random
from randomTexts import violentTexts
from gtts import gTTS

YDL_OPTIONS = {'audio-format': 'mp3', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

async def sendEmbed(ctx,title,description) : 
    await ctx.send(embed=discord.Embed(title=title,description=description,colour=discord.Colour(0xE5E242)))

async def sendGif(ctx,term) :
	mentions = ctx.message.mentions
	if len(mentions) == 0 :
		await sendEmbed(ctx,title='',description=f'Usage : billa {term} <@user>')
		return
	apikey = '8JAA7V1AF5MX'
	limit = 1 
	request = requests.get("https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (term, apikey, limit))
	gif = None
	if request.status_code == 200:
		gif = json.loads(request.content) 
	gifMsg = mentions[0].mention + ' ' + random.choice(violentTexts) + '\n' + gif['results'][0]['url']
	await ctx.send(content=gifMsg)

async def echo(ctx,voiceClient,message) :
	tts = gTTS(message,lang='en')
	with open('audio.mp3','wb') as file :
		tts.write_to_fp(file)
	await ctx.message.delete();
	try:
		voiceClient.play(discord.FFmpegPCMAudio('audio.mp3'),after=None)
		voiceClient.source = discord.PCMVolumeTransformer(voiceClient.source)
		voiceClient.source.volume = 1
	except discord.ClientException :
		await sendEmbed(ctx=ctx,title='Error',description='I am playing something else right now.')

def getVoiceClient(billaBot,ctx) : 
	for vc in billaBot.voice_clients : 
		if vc.guild == ctx.guild :
			return vc
	return None	

def searchSong(songName) :
	with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl :
		song = ydl.extract_info(f'ytsearch:{songName}',download=False)['entries'][0]
	return {'source':song['formats'][0]['url'],'title':song['title']}

def playNextSong(ctx,voiceClient,songQueueMap) :
	del songQueueMap[ctx.guild.name][0]
	if len(songQueueMap[ctx.guild.name]) > 0 :
		voiceClient.play(discord.FFmpegPCMAudio(songQueueMap[ctx.guild.name][0]['source'],**FFMPEG_OPTIONS),after=lambda e: playNextSong(ctx,voiceClient,songQueueMap))
		voiceClient.is_playing()

async def checkVoiceExceptions(billaBot,ctx,command) :
	if ctx.author.voice is None :
		await sendEmbed(ctx=ctx,title='',description='Please connect to a voice channel first.')
		return True
	voiceClient = getVoiceClient(billaBot,ctx)
	voiceChannel = ctx.author.voice.channel
	if command in {'skip','remove','disconnect'} :
		if voiceClient is None :
			await sendEmbed(ctx=ctx,title='',description='I am not connected to any voice channel.')
			return True
	if not voiceClient is None :
		if voiceClient.channel != voiceChannel :
			await sendEmbed(ctx=ctx,title='',description='You are connected to some other voice channel.')
			return True
	if command in {'play','echo'} :
		if len(ctx.message.content) < 12 :
			await sendEmbed(ctx=ctx,title='',description=f'Usage - billa {command} <args>.')
			return True
	if command == 'remove' :
		if len(ctx.message.content) < 14 :
			await sendEmbed(ctx=ctx,title='',description='Usage - billa remove <args>.')
			return True
	return False
		