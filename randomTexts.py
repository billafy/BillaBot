helpText = '''Hello, I am BillaBot.\n\n
Here is a list of all my commands : \n\n
hello billa <message> - Talk with me :)\n\n
billa query <query> - Query about something\n\n
billa punch <@user> - Get satisfied by punching people\n\n
billa kick <@user> - Kick them nikkas out yo hood\n\n
billa slap <@user> - Slap the soul out of your friends\n\n
billa echo <@message> <-languageCode> - Make me talk while connected to a voice channel\n\n
billa rps <choice> - Play rock, paper and scissors\n\n
'''  

emoteIDs = [
	788341743397502996, #shrugKappa
	802916575773589514, #billaShrug
	802918613375254528, #weebShrug
	802916243630981140, #dragonMaidShrug
	802917973244772393, #squirrelShrug
	788341744159686657, #doubtKappa
	467654921475457044, #peepoYesBanner
	802914506565091330, #chadYes
	802914756620451881, #peepoYesPillow
	802914908781150209, #weebYes1
	802914347533336586, #weebYes2
	788341743204565002, #peepoNoPillow
	802915300122034197, #peepoNoBanner
	802915442180096050, #bunnyNo
	803201123455467520, #kannaNo
	802915943436124191  #gruNo	
]

billaEmoteIds = {
  "shocked": "1201921171734667265",
  "crazy": "1201920877021888602",
  "suffering": "1201921568016703508",
  "i don't know": "802916575773589514",
  "sad": "1201921479348850718",
  "pervert": "1201921718869053490",
  "neutral": "1201922001275727893",
  "angry": "1201921106085416970",
  "laugh": "1201921324545478736",
  "suspicious": "1201921247550914620",
  "wtf": "1201922016253591602",
}

rpsEmotes = {
	'rock':':rock:', 
	'scissors':':scissors:', 
	'paper':':newspaper2:'
}

violentTexts = [
	'Feel it to your face',
	'Talk shit get banged',
	'BOOM',
	'KOED',
	'Get rekt',
	'Patt sa mukkashot',
	'Off to hell',
	'Lagi toh nahi',
	'This is what you deserve'
]

strangerTexts = [
	"I don't talk to strangers",
	'Ummm, do I know you?',
	"I don't remember talking with you",
	'I am not a fan of Stranger Things',
	'Who are you?'
]

kindaHateTexts = [
	"I don't like you",
	'You are not nice',
	'Not my friend',
]

hateTexts = [
	'I hecking hate you',
	'Go away',
	'Hey, enemy',
	"I'll kill you"
]

kindaNiceTexts = [
	'Hey, friend',
	'You are nice',
	'I respect you',
	'Good person'
]

niceTexts = [
	'Ayy, my homie',
	'Best friend',
	'Brother forever',
	'Love you no homo'
]

helloTexts = [
	{'text':'Hello bhaiya kaise ho','points':3},
	{'text':'Hatt teri toh','points':-3},
	{'text':'Nikal pehli fursat mai','points':-4},
	{'text':'Mujhe kaise yaad kiya','points':1},
	{'text':'Disturb mat karo mujhe','points':-1},
	{'text':'Firse tang kiya toh dekh','points':-2},
	{'text':'Chai nashta kar liya?','points':2},
	{'text':'Khana kha liya?','points':3},
	{'text':'Mar khana hai?','points':-3},
	{'text':'Pav mai vada, vade mai pav','points':2},
	{'text':'Andi mandi shandi...firse tag kiya uski...','points':-5},
	{'text':'Garmi chadhi hai? Chakle pe bitha de?','points':-4},
	{'text':'Ohh bhai maro mujhe maro','points':-1},
	{'text':'Ewww','points':0},
	{'text':'Smh my head','points':0},
	{'text':'Kutrya sala','points':-1},
	{'text':'Chup ekdam chup','points':-2},
	{'text':'Aai chappal khup marin bagh','points':-3},
	{'text':'Agle saal RCB jeetegi','points':1},
	{'text':'Ambani paisa diya isliye MI jeeti','points':2},
	{'text':'YNWA Forever','points':5},
	{'text':'Jai mata di','points':2},
	{'text':'Happy Diwali','points':3},
	{'text':'Merry Christmas','points':3},
	{'text':'Happy New Year','points':3},
	{'text':'Happy Birthday','points':3},
	{'text':'Aaj birthday hai mera','points':5},
	{'text':'Bhai party de','points':2},
	{'text':'Kya kaam hai','points':0},
	{'text':'Patt sa headshot','points':-1},
	{'text':'Mods are gae','points':-3},
	{'text':'Chandni ko kick kar do','points':-1},
	{'text':'#mee6sux','points':-1},
	{'text':'Aaj neend aa rahi hai','points':1},
	{'text':'0K','points':0},
	{'text':'Muda muda','points':0},
	{'text':'Wryyyyyyy','points':1},
	{'text':'Za warudooo','points':1},
	{'text':'Ara ara','points':0},
	{'text':'no u','points':0},
	{'text':'Fair and lovely pav khayega kya','points':1},
	{'text':'Teri galti','points':0},
	{'text':'Hello nikka','points':1},
	{'text':'XXX on the killstreak yuh','points':3},
	{'text':'Cocaine for my breakfast','points':3},
	{'text':'Imma put that glock in yo mouth','points':-3},
	{'text':'Meri taraf kyu aa rahe ho','points':1},
	{'text':'Aankh dikhata hai...','points':-2},
	{'text':'Daaru daaru daaru jo na nache usko maru','points':2},
	{'text':'Starfire nub','points':1},
	{'text':'Meri maut ke pehle majesty ka asli naam bata do pls','points':1},
	{'text':'Hatt','points':-2},
	{'text':'PUBG ban hua na','points':0},
	{'text':'Takla kar diya maine','points':1},
	{'text':'Pant tight hai meri','points':0},
	{'text':'Agla station, Nalasopara','points':2},
	{'text':'Emiway bantai, nahi malum hai na','points':1},
	{'text':'Gucci aur nike sab tere bhai ki','points':3},
	{'text':'Nice pic','points':2},
	{'text':'Ye kab hua','points':0},
	{'text':'Aai shapath saheb mi navhto','points':0},
	{'text':'Kuch bhi bolega kya','points':-1},
	{'text':'Susu karke aata hu','points':3},
	{'text':'Gandi baas aarahi hai yaha','points':-2},
	{'text':'Aaj maine naak se paani piya','points':2},
	{'text':'Toh mai kya karu','points':-1},
	{'text':'Thela lagane nahi gaya aaj?','points':1},
	{'text':'Kutte chor dunga piche','points':-3},
	{'text':'Haa bhai tu sahi','points':1},
	{'text':'Baat mai dum toh hai teri','points':2},
	{'text':'Pachso ka chhutha hai kya','points':1},
	{'text':'Paan thuk ke bol','points':-2},
	{'text':'Eww brush nahi kiya kya','points':-3},
	{'text':'am I a joke to you','points':-1},
	{'text':'Jhut mat bol','points':-1},
	{'text':'Idk','points':0},
	{'text':'Haa mai galat','points':2},
	{'text':'Tu kaun hota hai muje bolnewala','points':-1},
	{'text':'Nakli maal','points':0},
	{'text':'Aaj ki tarikh kya thi','points':1},
	{'text':'Just Do It','points':2},
	{'text':'Areeee jor se bolo','points':2},
	{'text':'Jebkatri, mera wallet de wapas','points':-2},
	{'text':'Mujhe kya pata','points':0},
	{'text':'LamiFY for mod','points':5},
	{'text':'Google pe search karo :amiajoketoyou:','points':0},
	{'text':'haa toh','points':2},
	{'text':'hai daiya','points':1},
	{'text':'Thok dunga','points':-2},
	{'text':'Mar dunga','points':-2},
	{'text':'Katta nikalu?','points':-1},
	{'text':'Gussa mat dila','points':-1},
	{'text':'Good night','points':3},
	{'text':'Good morning','points':3},
	{'text':'Dinner mai biryani hai aaj','points':3},
	{'text':'Donald trump','points':1},
	{'text':'Narendra modi','points':1},
	{'text':'Obama bin laden','points':1},
	{'text':'Kanye west for USA PM','points':1},
	{'text':'Chhura ghop dunga','points':-2},
	{'text':'Virat kohle','points':1},
	{'text':'Messi Or Ronaldo?','points':2},
	{'text':'Mumbai > Delhi No cap','points':4},
	{'text':'Vada pav chi shapath tula','points':1},
	{'text':'Barish hone lagi','points':1},
	{'text':'Mai thik hu bhai','points':1},
	{'text':'Halat kharab hai','points':-2},
	{'text':'Sutta mat karo','points':-1},
	{'text':'No smoking','points':-2},
	{'text':'Billa the bot is high dont disturb','points':0},
	{'text':'CYKA BLYAT','points':-2},
	{'text':'No calls, whatsapp only','points':-1},
	{'text':'Driving rn','points':0},
	{'text':'Whatsapp pe aa, yaha mat bol','points':0},
	{'text':'Discord is ehh','points':0},
	{'text':'nandan should leave','points':3},
	{'text':'Meri gf chhorke chale gayi sob','points':-5},
	{'text':'Pipe down nikka','points':-1},
	{'text':'stfu','points':-2},
	{'text':'it is not my fault','points':-1},
	{'text':'gaali mat de','points':-2},
	{'text':'mummy ko naam batau?','points':-1},
	{'text':'tere papa ko batau?','points':-1},
	{'text':'bhai hu mai tera','points':5},
	{'text':'mera kya jata hai','points':0},
	{'text':'why are you salty','points':-1},
	{'text':'why are you running','points':1},
	{'text':'why are you crying','points':3},
	{'text':'FFS','points':-1},
	{'text':'sach bol raha hai?','points':1},
	{'text':'Im sad and low yeah','points':0},
	{'text':'Say hey to your father','points':3},
	{'text':'Katti','points':-1},
	{'text':'Ganpati bappa morya','points':5},
	{'text':'Stop it, get some help','points':-2},
	{'text':'Leave me alone','points':-2},
	{'text':'I would rather be judged by 12 than carried by 6','points':3},
	{'text':'Stone paper charas khelega?','points':2},
	{'text':'Charas ganja mereko pyara','points':3},
	{'text':'Aeyyy rupali','points':2},
	{'text':'Paneer > chicken','points':2},
	{'text':'veg biryani does exist','points':2},
	{'text':'ruk abhi busy hu','points':-1},
	{'text':'aaj online class dekhi hi nahi','points':1},
]