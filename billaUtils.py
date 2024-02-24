import discord
import requests
import json
from numpy import random
from randomTexts import violentTexts
from gtts import gTTS
from datetime import datetime, timezone

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

def getLiveMatches() :
	headers = {
        'apiKey': '244e8680-e269-11eb-8c1d-839c7cad03c5'
    }
	params = {
		'live': True
	}
	response = requests.get('https://app.sportdataapi.com/api/v1/soccer/matches', headers=headers, params=params)
	matches = response.json()['data']
	matchesText = []
	for match in matches :
		homeTeam = match['home_team']['name']
		awayTeam = match['away_team']['name']
		homeScore = match['stats']['home_score']
		awayScore = match['stats']['away_score']
		time = match['minute']
		league = match['group']['group_name']
		matchesText.append(f"{time}' {homeTeam} {homeScore}-{awayScore} {awayTeam} ({league})")
	if len(matchesText) == 0 :
		matchesText = 'No live games'
	else :
		matchesText = '\n\n'.join(matchesText)
	return matchesText

def getImage(url) :
	response = requests.get(url, stream = True)
	return response.raw

async def get_latest_conversation(channel, client, message_count=100): 
	conversation = "--- start of conversation ---\n" 
	messages = client.get_channel(channel.id).history(limit=message_count)
	messages = [message async for message in messages]
	messages.reverse()
	users = set(["lamify"])
	for i in range(len(messages)): 
			if messages[i].author.name != "BillaBot": 
					try: 
						users.add(messages[i].author.nick)
					except Exception as e:  
						users.add(messages[i].author.name)
			if messages[i].content == "billa summary" or (i - 1 >= 0 and messages[i - 1].content == "billa summary"): 
					continue
			duration = datetime.now(timezone.utc) - messages[i].created_at
			if duration.total_seconds() <= 12 * 60 * 60: 
					conversation += f'{messages[i].author.name} : {messages[i].content}'
					conversation += "\n"
	conversation += "--- end of conversation ---\n"
	return conversation, users
