import json

helpText = """Hello, I am BillaBot.\n\n
Here is a list of all my commands : \n\n
hello billa <message> - Talk with me :)\n\n
billa punch <@user> - Get satisfied by punching people\n\n
billa kick <@user> - Kick them nikkas out yo hood\n\n
billa slap <@user> - Slap the soul out of your friends\n\n
billa echo <@message> <-languageCode> - Make me talk while connected to a voice channel\n\n
billa join - Make me join a voice channell\n\n
billa disconnect - Make me disconnect from a voice channel\n\n
billa play <songname> - Play a song\n\n
billa skip - Skip the song which is currently playing\n\n
billa queue - Shows a list of all the queued songs\n\n
billa remove <songindex> - Remove a song from the queue by specifying the index\n\n
billa rps <choice> - Play rock, paper and scissors
billa live - Get live football scores"""

emoteIDs = [
    788341743397502996,  # shrugKappa
    802916575773589514,  # billaShrug
    802918613375254528,  # weebShrug
    802916243630981140,  # dragonMaidShrug
    802917973244772393,  # squirrelShrug
    788341744159686657,  # doubtKappa
    467654921475457044,  # peepoYesBanner
    802914506565091330,  # chadYes
    802914756620451881,  # peepoYesPillow
    802914908781150209,  # weebYes1
    802914347533336586,  # weebYes2
    788341743204565002,  # peepoNoPillow
    802915300122034197,  # peepoNoBanner
    802915442180096050,  # bunnyNo
    803201123455467520,  # kannaNo
    802915943436124191,  # gruNo
]

rpsEmotes = {"rock": ":rock:", "scissors": ":scissors:", "paper": ":newspaper2:"}

violentTexts = [
    "Feel it to your face",
    "Talk shit get banged",
    "BOOM",
    "KOED",
    "Get rekt",
    "Patt sa mukkashot",
    "Off to hell",
    "Lagi toh nahi",
    "This is what you deserve",
]

strangerTexts = [
    "I don't talk to strangers",
    "Ummm, do I know you?",
    "I don't remember talking with you",
    "I am not a fan of Stranger Things",
    "Who are you?",
]

kindaHateTexts = [
    "I don't like you",
    "You are not nice",
    "Not my friend",
]

hateTexts = ["I hecking hate you", "Go away", "Hey, enemy", "I'll kill you"]

kindaNiceTexts = ["Hey, friend", "You are nice", "I respect you", "Good person"]

niceTexts = ["Ayy, my homie", "Best friend", "Brother forever", "Love you no homo"]

helloTexts = [
    {"text": "Hello bhaiya kaise ho"},
    {"text": "Hatt teri toh"},
    {"text": "Nikal pehli fursat mai"},
    {"text": "Mujhe kaise yaad kiya"},
    {"text": "Disturb mat karo mujhe"},
    {"text": "Firse tang kiya toh dekh"},
    {"text": "Chai nashta kar liya?"},
    {"text": "Khana kha liya?"},
    {"text": "Mar khana hai?"},
    {"text": "Pav mai vada, vade mai pav"},
    {"text": "Andi mandi shandi...firse tag kiya uski..."},
    {"text": "Garmi chadhi hai? Chakle pe bitha de?"},
    {"text": "Ohh bhai maro mujhe maro"},
    {"text": "Ewww"},
    {"text": "Smh my head"},
    {"text": "Kutrya sala"},
    {"text": "Chup ekdam chup"},
    {"text": "Aai chappal khup marin bagh"},
    {"text": "Agle saal RCB jeetegi"},
    {"text": "Ambani paisa diya isliye MI jeeti"},
    {"text": "YNWA Forever"},
    {"text": "Jai mata di"},
    {"text": "Happy Diwali"},
    {"text": "Merry Christmas"},
    {"text": "Happy New Year"},
    {"text": "Happy Birthday"},
    {"text": "Aaj birthday hai mera"},
    {"text": "Bhai party de"},
    {"text": "Kya kaam hai"},
    {"text": "Patt sa headshot"},
    {"text": "Mods are gae"},
    {"text": "Chandni ko kick kar do"},
    {"text": "#mee6sux"},
    {"text": "Aaj neend aa rahi hai"},
    {"text": "0K"},
    {"text": "Muda muda"},
    {"text": "Wryyyyyyy"},
    {"text": "Za warudooo"},
    {"text": "Ara ara"},
    {"text": "no u"},
    {"text": "Fair and lovely pav khayega kya"},
    {"text": "Teri galti"},
    {"text": "Hello nikka"},
    {"text": "XXX on the killstreak yuh"},
    {"text": "Cocaine for my breakfast"},
    {"text": "Imma put that glock in yo mouth"},
    {"text": "Meri taraf kyu aa rahe ho"},
    {"text": "Aankh dikhata hai..."},
    {"text": "Daaru daaru daaru jo na nache usko maru"},
    {"text": "Starfire nub"},
    {"text": "Meri maut ke pehle majesty ka asli naam bata do pls"},
    {"text": "Hatt"},
    {"text": "PUBG ban hua na"},
    {"text": "Takla kar diya maine"},
    {"text": "Pant tight hai meri"},
    {"text": "Agla station, Nalasopara"},
    {"text": "Emiway bantai, nahi malum hai na"},
    {"text": "Gucci aur nike sab tere bhai ki"},
    {"text": "Nice pic"},
    {"text": "Ye kab hua"},
    {"text": "Aai shapath saheb mi navhto"},
    {"text": "Kuch bhi bolega kya"},
    {"text": "Susu karke aata hu"},
    {"text": "Gandi baas aarahi hai yaha"},
    {"text": "Aaj maine naak se paani piya"},
    {"text": "Toh mai kya karu"},
    {"text": "Thela lagane nahi gaya aaj?"},
    {"text": "Kutte chor dunga piche"},
    {"text": "Haa bhai tu sahi"},
    {"text": "Baat mai dum toh hai teri"},
    {"text": "Pachso ka chhutha hai kya"},
    {"text": "Paan thuk ke bol"},
    {"text": "Eww brush nahi kiya kya"},
    {"text": "am I a joke to you"},
    {"text": "Jhut mat bol"},
    {"text": "Idk"},
    {"text": "Haa mai galat"},
    {"text": "Tu kaun hota hai muje bolnewala"},
    {"text": "Nakli maal"},
    {"text": "Aaj ki tarikh kya thi"},
    {"text": "Just Do It"},
    {"text": "Areeee jor se bolo"},
    {"text": "Jebkatri, mera wallet de wapas"},
    {"text": "Mujhe kya pata"},
    {"text": "LamiFY for mod"},
    {"text": "Google pe search karo :amiajoketoyou:"},
    {"text": "haa toh"},
    {"text": "hai daiya"},
    {"text": "Thok dunga"},
    {"text": "Mar dunga"},
    {"text": "Katta nikalu?"},
    {"text": "Gussa mat dila"},
    {"text": "Good night"},
    {"text": "Good morning"},
    {"text": "Dinner mai biryani hai aaj"},
    {"text": "Donald trump"},
    {"text": "Narendra modi"},
    {"text": "Obama bin laden"},
    {"text": "Kanye west for USA PM"},
    {"text": "Chhura ghop dunga"},
    {"text": "Virat kohle"},
    {"text": "Messi Or Ronaldo?"},
    {"text": "Mumbai > Delhi No cap"},
    {"text": "Vada pav chi shapath tula"},
    {"text": "Barish hone lagi"},
    {"text": "Mai thik hu bhai"},
    {"text": "Halat kharab hai"},
    {"text": "Sutta mat karo"},
    {"text": "No smoking"},
    {"text": "Billa the bot is high dont disturb"},
    {"text": "CYKA BLYAT"},
    {"text": "No calls, whatsapp only"},
    {"text": "Driving rn"},
    {"text": "Whatsapp pe aa, yaha mat bol"},
    {"text": "Discord is ehh"},
    {"text": "nandan should leave"},
    {"text": "Meri gf chhorke chale gayi sob"},
    {"text": "Pipe down nikka"},
    {"text": "stfu"},
    {"text": "it is not my fault"},
    {"text": "gaali mat de"},
    {"text": "mummy ko naam batau?"},
    {"text": "tere papa ko batau?"},
    {"text": "bhai hu mai tera"},
    {"text": "mera kya jata hai"},
    {"text": "why are you salty"},
    {"text": "why are you running"},
    {"text": "why are you crying"},
    {"text": "FFS"},
    {"text": "sach bol raha hai?"},
    {"text": "Im sad and low yeah"},
    {"text": "Say hey to your father"},
    {"text": "Katti"},
    {"text": "Ganpati bappa morya"},
    {"text": "Stop it, get some help"},
    {"text": "Leave me alone"},
    {"text": "I would rather be judged by 12 than carried by 6"},
    {"text": "Stone paper charas khelega?"},
    {"text": "Charas ganja mereko pyara"},
    {"text": "Aeyyy rupali"},
    {"text": "Paneer > chicken"},
    {"text": "veg biryani does exist"},
    {"text": "ruk abhi busy hu"},
    {"text": "aaj online class dekhi hi nahi"},
]
