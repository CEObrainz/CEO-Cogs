import discord
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
import platform, asyncio, string, operator, random, textwrap
import os, re, aiohttp
from .utils.dataIO import fileIO
from cogs.utils import checks
from datetime import datetime
import time
from random import randint
from chatterbot import ChatBot


prefix = fileIO("data/red/settings.json", "load")['PREFIXES']   
greeting = {'hello', 'greetings', 'hi', 'hey', 'o/', 'sup'}
leaving = {'bye', 'cya', 'take care', 'good night', 'later'}
justname = {'renner', 'renner.', 'renner?', 'renner!'}
me = {'i\'m fine', 'i\'m doing well', 'i\'m ok', 'i\'m great', 'i\'m good',}

chatbot.train([
    'How can I help you?',
    'I want to create a chat bot',
    'Have you read the documentation?',
    'No, I have not',
])

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

class Affinity:

    def __init__(self, bot):
        self.bot = bot
        chatbot = ChatBot(
            'Renner',
            storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch'
                },
                {
                    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                    'threshold': 0.65,
                    'default_response': 'I am sorry, but I do not understand.'
                }
            ],
            trainer='chatterbot.trainers.ListTrainer'
        )

    async def get_response(self, msg):
        question = self.bot.loop.run_in_executor(None, self.clv.ask, msg)
        try:
            answer = await asyncio.wait_for(question, timeout=10)
        except asyncio.TimeoutError:
            answer = "We'll talk later..."
        return answer
                 
    def split_into_sentences(self, text):
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace(",",",<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences

    async def respond(self, user, text, channel, curr_time):
        if text.endswith('.') == False:
            text += '.'
        input = self.split_into_sentences(text)
        for i in range(len(input)):
            chatbot.train(input[i])
            response = chatbot.get_response(input[i])
            respond += str(response)
            respond += ' '
        respond = respond.rstrip()
        if respond == "<Nothing>":
            return
        else:
            respond = respond.replace("<Nothing>","")
            if respond.endswith(','):
                respond = respond[:-1] + '.'
            await self.bot.send_message(channel, respond) 
        
    async def on_message(self, message):
        text = message.content
        channel = message.channel
        user = message.author
        await self._create_user(user)
        text = text.lower()
        mention = message.server.me.mention 
        if mention in message.content: 
            await self.bot.send_typing(message.channel)
            content = message.content.replace(mention, "").strip()
            text = content.lower()
            await self.respond(user, text, channel)

  
def check_folders():
    if not os.path.exists("data/affinity"):
        print("Creating data/affinity folder...")
        os.makedirs("data/affinity")  
        
def check_files():
  
    f = "data/affinity/users.json"
    if not fileIO(f, "check"):
        print("Creating users.json...")
        fileIO(f, "save", {}) 

    f = "data/affinity/responses.json"
    if not fileIO(f, "check"):
        print("Creating responses.json...")
        fileIO(f, "save", {})      
         
         
def setup(bot):
    check_folders()
    check_files()
    n = Affinity(bot)
    bot.add_cog(n)     
        
        