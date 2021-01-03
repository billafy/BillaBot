import os
import discord
from dotenv import load_dotenv
from numpy import random
import youtube_dl
import requests
import json
from webserver import keep_alive
from gtts import gTTS

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

songDict = dict({})
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'audio-format': 'mp3', 'noplaylist':'True'}

@client.event
async def on_ready() : 
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_member_join(member) : 
    dmChannel = member.create_dm()
    await dmChannel.send(content=f'Welcome to {member.guild.name}')
    
@client.event
async def on_message(message) : 
    random_txts = ['Hello bhaiya kaise ho','Hatt teri toh','Nikal pehli fursat mai','Mujhe kaise yaad kiya','Disturb mat karo mujhe','Firse tang kiya toh dekh','Chai nashta kar liya?','Khana kha liya?','Mar khana hai?','Pav mai vada, vade mai pav','Andi mandi shandi...firse tag kiya uski...','Garmi chadhi hai? Chakle pe bitha de?','Ohh bhai maro mujhe maro','Ewww','Smh my head','Kutrya sala','Chup ekdam chup','Aai chappal khup marin bagh','Agle saal RCB jeetegi','Ambani paisa diya isliye MI jeeti','YNWA Forever','Jai mata di','Happy Diwali','Merry Christmas','Happy New Year','Happy Birthday','Aaj birthday hai mera','Bhai party de','Kya kaam hai','Patt sa headshot','Mods are gae','Chandni ko kick kar do','#mee6sux','Aaj neend aa rahi hai','0K','Muda muda','Wryyyyyyy','Za warudooo','Ara ara','no u','Fair and lovely pav khayega kya','Teri galti','Hello nikka','XXX on the killstreak yuh','Cocaine for my breakfast','Imma put that glock in yo mouth','Meri taraf kyu aa rahe ho','Aankh dikhata hai...','Daaru daaru daaru jo na nache usko maru','Starfire nub','Meri maut ke pehle majesty ka asli naam bata do pls','Hatt','PUBG ban hua na','Takla kar diya maine','Pant tight hai meri','Agla station, Nalasopara','Emiway bantai, nahi malum hai na','Gucci aur nike sab tere bhai ki','Nice pic','Ye kab hua','Aai shapath saheb mi navhto','Kuch bhi bolega kya','Susu karke aata hu','Gandi baas aarahi hai yaha','Aaj maine naak se paani piya','Toh mai kya karu','Thela lagane nahi gaya aaj?','Kutte chor dunga piche','Haa bhai tu sahi','Baat mai dum toh hai teri','Pachso ka chhutha hai kya','Paan thuk ke bol','Eww brush nahi kiya kya','am I a joke to you','Jhut mat bol','Idk','Haa mai galat','Tu kaun hota hai muje bolnewala','Nakli maal','Aaj ki tarikh kya thi','Just Do It','Areeee jor se bolo','Jebkatri, mera wallet de wapas','Mujhe kya pata','LamiFY for mod','Google pe search karo :amiajoketoyou:',':haaToh:haa toh','hai daiya','Thok dunga','Mar dunga','Katta nikalu?','Gussa mat dila','Good night','Good morning','Dinner mai biryani hai aaj','Donald trump','Narendra modi','Obama bin laden','Kanye west for USA PM','Chhura ghop dunga','Virat kohle','Messi Or Ronaldo?','Mumbai > Delhi No cap','Vada pav chi shapath tula','Barish hone lagi','Mai thik hu bhai',f'Aur {message.author.name} didi','Halat kharab hai','Sutta mat karo','No smoking','Billa the bot is high dont disturb','CYKA BLYAT','No calls, whatsapp only','Driving rn','Whatsapp se aa, yaha mat bol','Discord is ehh','nandan should leave',f'{message.author.name}, You are the best! :slight_smile:',f'Have a good day, {message.author.name}','Meri gf chhorke chale gayi :sob:','Pipe down nikka','stfu','it is not my fault','gaali mat de','mummy ko naam batau?','tere papa ko batau?','bhai hu mai tera','mera kya jata hai','why are you salty','why are you running','why are you crying','FFS','sach bol raha hai?','Im sad and low yeah','Say hey to your father',f'{message.author.name} sux','Katti','Ganpati bappa morya','Stop it, get some help','Leave me alone','I would rather be judged by 12 than carried by 6','Stone paper charas khelega?','Charas ganja mereko pyara','Aeyyy rupali','Paneer > chicken','veg biryani does exist','ruk abhi busy hu','aaj online class dekhi hi nahi','lockdown khatam kyu nahi ho raha']
    
    if message.content.lower().startswith('hello billa') and len(message.content) > 12 : 
        response = random.choice(random_txts)
        await message.channel.send(content=response)
        
    if message.content.lower() == 'billa help' :
        commands = 'Hello, I am BillaBot.\n\nHere is a list of all my commands : \n\nhello billa <message> - Talk with me :)\n\nbilla meow - Cute Cat GIFS\n\nbilla punch <@user> - Get satisfied by punching people\n\nbilla kick <@user> - Kick them nikkas out yo hood\n\nbilla slap <@user> - Slap the soul out of your friends\n\nbilla echo <@message> <-languageCode> - Make me talk while connected to a voice channel\n\nbilla join - Make me join a voice channell\n\nbilla disconnect - Make me disconnect from a voice channel\n\nbilla play <songname> - Play a song\n\nbilla skip - Skip the song which is currently playing\n\nbilla queue - Shows a list of all the queued songs\n\nbilla remove <songindex> - Remove a song from the queue by specifying the index'    
        await message.channel.send(embed=discord.Embed(title='BillaBot Commands',description=commands,colour=discord.Colour(0xE5E242)))

    if message.content.lower() == 'billa join' : 
        if message.author.voice is None : 
            await message.channel.send(embed=discord.Embed(description='Please join a voice channel yourself before asking me to join.',colour=discord.Colour(0xE5E242)))
        else : 
            voc_channel = message.author.voice.channel
            voice_channel = await voc_channel.connect()
            joinMsgs = [f'Connected to {voc_channel.name}',f'Joined {voc_channel.name}','I am ready'] 
            msg = random.choice(joinMsgs)
            print(msg)
            tts = gTTS(msg,lang='en')
            with open('audio.mp3','wb') as f : 
                tts.write_to_fp(f)
            voice_channel.play(discord.FFmpegPCMAudio('audio.mp3'),after=None)
            voice_channel.source = discord.PCMVolumeTransformer(voice_channel.source)
            voice_channel.source.volume = 1
            await message.channel.send(embed=discord.Embed(description=f'Connected to {voc_channel}.',colour=discord.Colour(0xE5E242)))
            
    if message.content.lower().startswith('billa play') : 
        voice_channel = discord.utils.get(client.voice_clients,guild=message.guild)
        if len(message.content) < 12 : 
            await message.channel.send(embed=discord.Embed(description='Usage : billa play <songname>',colour=discord.Colour(0xE5E242)))
            return
        if message.author.voice is None : 
            await message.channel.send(embed=discord.Embed(description='Please join a voice channel yourself before asking me to play a song.',colour=discord.Colour(0xE5E242)))
            return
        if voice_channel and voice_channel.is_connected() :  
            await voice_channel.move_to(message.channel)
        else :
            voice_channel = await message.author.voice.channel.connect()
        command = message.content.lower()
        songname = command[11:]
        song = searchSong(songname)
        guild_name = message.guild.name
        if guild_name in songDict : 
            songDict[guild_name].append(song)
        else:
            songDict[guild_name] = []
            songDict[guild_name].append(song)        
        songtitle = song['title']
        audio_source = discord.FFmpegPCMAudio(songDict[guild_name][0]['source'],**FFMPEG_OPTIONS)
        if not voice_channel.is_playing() : 
            await message.channel.send(embed=discord.Embed(title='Playing',description=f'{songtitle}',colour=discord.Colour(0xE5E242)))
            voice_channel.play(audio_source,after=lambda e:playNextSong(message,voice_channel))
            voice_channel.is_playing()
        else : 
            await message.channel.send(embed=discord.Embed(title='Added to the queue',description=f'{songtitle}',colour=discord.Colour(0xE5E242)))

    if message.content.lower().startswith('billa echo') :
        if len(message.content) < 12 :
            await message.channel.send(embed=discord.Embed(description='Usage : billa echo <message>',colour=discord.Colour(0xE5E242)))
            return
        if message.author.voice is None : 
            await message.channel.send(embed=discord.Embed(description='Please join a voice channel.',colour=discord.Colour(0xE5E242)))
            return
        voice_channel = discord.utils.get(client.voice_clients,guild=message.guild)
        if voice_channel and voice_channel.is_connected() : 
            await voice_channel.move_to(message.channel)
        else : 
            voice_channel = await message.author.voice.channel.connect()
        echoMsg = message.content[11:]
        tts = gTTS(echoMsg,lang='en')
        with open('audio.mp3','wb') as f : 
            tts.write_to_fp(f)
        try : 
            audio = discord.FFmpegPCMAudio('audio.mp3')
            voice_channel.play(audio,after=None)
            voice_channel.source = discord.PCMVolumeTransformer(voice_channel.source)
            voice_channel.source.volume = 1            
        except discord.ClientException:
            await message.channel.send(embed=discord.Embed(description='I am playing something else rn.',colour=discord.Colour(0xE5E242)))
        except TypeError:
            await message.channel.send(embed=discord.Embed(description='Error',colour=discord.Colour(0xE5E242)))
            
    if message.content.lower() == 'billa queue' : 
        i = 1
        queue = ''
        songqueue = []
        guild_name = message.guild.name
        if guild_name in songDict : 
            songqueue = songDict[guild_name]
        for song in songqueue : 
            queue += str(i) + '. ' + song['title'] + '\n'
            i+=1 
        await message.channel.send(embed=discord.Embed(description=queue,colour=discord.Colour(0xE5E242)))
        
    if message.content.lower() == 'billa disconnect' : 
        if message.author.voice is None : 
            await message.channel.send(embed=discord.Embed(description='You are not connected to any voice channel, you cannot tell me what to do.',colour=discord.Colour(0xE5E242)))
        else : 
            voice_channel = discord.utils.get(client.voice_clients,guild=message.guild)
            if voice_channel and voice_channel.is_connected() :
                guild_name = message.guild.name
                if guild_name in songDict : 
                    songDict[guild_name].clear()
                await voice_channel.disconnect()
                await message.channel.send(embed=discord.Embed(description='Disconnected',colour=discord.Colour(0xE5E242)))
                
    if message.content.lower() == 'billa skip' : 
        if message.author.voice is None : 
            await message.channel.send(embed=discord.Embed(description='You are not connected to any voice channel, you cannot tell me what to do.',colour=discord.Colour(0xE5E242)))
            return
        voice_channel = discord.utils.get(client.voice_clients,guild=message.guild)
        guild_name = message.guild.name
        songqueue = []
        if guild_name in songDict : 
            songqueue = songDict[guild_name]
        if voice_channel and voice_channel.is_connected() and len(songqueue) > 0 : 
            songtitle = songqueue[0]['title']
            await voice_channel.disconnect()
            if len(songqueue) == 0 : 
                return
            voice_channel = await message.author.voice.channel.connect()
            voice_channel.play(discord.FFmpegPCMAudio(songDict[guild_name][0]['source'],**FFMPEG_OPTIONS),after=lambda e:playNextSong(message,voice_channel))
            await message.channel.send(embed=discord.Embed(title='Skipped',description=f'{songtitle}',colour=discord.Colour(0xE5E242)))
        else : 
            await message.channel.send(embed=discord.Embed(description='No song to skip.',colour=discord.Colour(0xE5E242)))
                
    if message.content.lower().startswith('billa remove') :
        if message.author.voice is None : 
            await message.channel.send(embed=discord.Embed(description='You are not connected to any voice channel, you cannot tell me what to do.',colour=discord.Colour(0xE5E242)))
            return
        if len(message.content) < 14 : 
            await message.channel.send(embed=discord.Embed(description='Usage : billa remove <songindex>',colour=discord.Colour(0xE5E242)))
            return
        songNumber = message.content[13:]
        if not songNumber.isnumeric() : 
            await message.channel.send(embed=discord.Embed(description='Invalid index.',colour=discord.Colour(0xE5E242)))
            return
        songNumber = int(songNumber)
        if songNumber == 1 : 
            await message.channel.send(embed=discord.Embed(description='Just use billa skip instead smh.',colour=discord.Colour(0xE5E242)))
            return
        guild_name = message.guild.name
        if songNumber > len(songDict[guild_name]) or songNumber <= 1 : 
            await message.channel.send(embed=discord.Embed(description='Index out of range.',colour=discord.Colour(0xE5E242)))
            return
        songtitle = songDict[guild_name][songNumber-1]['title']
        del songDict[guild_name][songNumber-1]
        await message.channel.send(embed=discord.Embed(title='Removed from the queue',description=f'{songtitle}',colour=discord.Colour(0xE5E242)))
        
    if message.content.lower() == 'billa meow' : 
        apikey = '8JAA7V1AF5MX'
        lmt = 1
        
        randomTerms = ['cat','kitty','kitten']        
        search_term = random.choice(randomTerms)
        
        r = requests.get("https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        gif = None
        if r.status_code == 200:
            gif = json.loads(r.content)
        url = gif['results'][0]['url']       
        await message.channel.send(content=url)
        
    if message.content.lower().startswith('billa punch') :
        apikey = '8JAA7V1AF5MX'
        lmt = 1
        
        randomTerms = ['punch']        
        search_term = random.choice(randomTerms)
        
        r = requests.get("https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        gif = None
        if r.status_code == 200:
            gif = json.loads(r.content)
        mentions = message.mentions
        if len(mentions) == 0 :
            await message.channel.send(content='`Usage : billa punch <@user>`')
            return
        randomPunchLines = ['Feel it to your face','Talk shit get banged','BOOM','KOED','Get rekt','Patt sa mukkashot','Off to hell','Lagi toh nahi','This what you deserve']
        gifMsg = mentions[0].mention + ' ' + random.choice(randomPunchLines) + '\n' + gif['results'][0]['url']
        await message.channel.send(content=gifMsg)
        
    if message.content.lower().startswith('billa kick') :
        apikey = '8JAA7V1AF5MX'
        lmt = 1
        
        randomTerms = ['kick']        
        search_term = random.choice(randomTerms)
        
        r = requests.get("https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        gif = None
        if r.status_code == 200:
            gif = json.loads(r.content)
        mentions = message.mentions
        if len(mentions) == 0 :
            await message.channel.send(content='`Usage : billa kick <@user>`')
            return
        randomKickLines = ['How does it feel?','Lagi kya jor se','Patt sa kickshot','Sweet chin music','BOOM','Get rekt','Chat shit get banged','Off to hell','This what you deserve']
        gifMsg = mentions[0].mention + ' ' + random.choice(randomKickLines) + '\n' + gif['results'][0]['url'] 
        await message.channel.send(content=gifMsg)
        
    if message.content.lower().startswith('billa slap') :
        apikey = '8JAA7V1AF5MX'
        lmt = 1
        
        randomTerms = ['slap']        
        search_term = random.choice(randomTerms)
        
        r = requests.get("https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        gif = None
        if r.status_code == 200:
            gif = json.loads(r.content)
        mentions = message.mentions
        if len(mentions) == 0 :
            await message.channel.send(content='`Usage : billa slap <@user>`')
            return
        randomSlapLines = ['How does it feel?','Lagi kya jor se','Patt sa chamatshot','Cheeks turned red','BOOM','Get rekt','Talk shit get banged','Off to hell','This what you deserve']
        gifMsg = mentions[0].mention + ' ' + random.choice(randomSlapLines) + '\n' + gif['results'][0]['url'] 
        await message.channel.send(content=gifMsg)
               
def searchSong(songname) :
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl : 
        info = ydl.extract_info(f'ytsearch:{songname}',download=False)['entries'][0]
    return {'source':info['formats'][0]['url'],'title':info['title']}
    
def playNextSong(message,voice_channel) :
    guild_name = message.guild.name
    if len(songDict[guild_name]) > 0 : 
        del songDict[guild_name][0]
        voice_channel.play(discord.FFmpegPCMAudio(songDict[guild_name][0]['source'],**FFMPEG_OPTIONS),after=lambda e:playNextSong(message,voice_channel))
        voice_channel.is_playing()

keep_alive()    
                
client.run(TOKEN)
