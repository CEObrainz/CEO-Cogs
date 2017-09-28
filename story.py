import discord
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
import platform, asyncio, string, operator, random, textwrap
import os, re, aiohttp, sys, json
import traceback
from .utils.dataIO import fileIO, dataIO
from cogs.utils import checks
import threading
from copy import deepcopy
from datetime import datetime
import time
import random
from random import randint
import logging
import math

weapons = "data/story/weapons/types.txt"
types = "data/story/background/types.txt"
factions = "data/story/background/factions/factions.txt"
#items = "data/story/items.txt"


class Story:

    #leaderboard stuff

    def __init__(self, bot):
        self.bot = bot
        self.users = fileIO("data/story/users.json", "load")
        self.settings = fileIO("data/story/settings.json", "load")

    def backstory(self, name, gender, floor, age, type, weapon, faction, personality, power, ParentWealth, LivingWith, UserLife, interest, goal):
        
        if gender == "Male":
            gender = "his"
            gend = "He"
            usegend = "he"
        else:
            gender = "her"
            gend = "She"
            usegend = "she"
        
        if ParentWealth == "Rich":
            homes = ["suburbs", "estates", "high-class homes", "castles", "villas", "palaces"]
            SS = ["rich", "wealthy", "successful", "well off"]
        elif ParentWealth == "Normal":
            homes = ["suburbs", "capital city", "one of the cities", "towns", "one of the towns", "quiet towns"]
            SS = ["normal", "average"]
        else:
            homes = ["streets", "slums", "flats", "abandoned houses", "run down parts of town, ", "below-average home"]
            SS = ["poor", "penniless", "impoverished", "poverty-stricken"]
        area = random.choice(homes)
        word1 = random.choice(SS)
        
        
        if LivingWith == "Orphan":
            pla = {}
            pla['1'] = 'Growing up without parents,'
            pla['2'] = 'Living without any parents,'
            pla['3'] = 'With {} parents dying very early,'.format(gender)
            pla['4'] = 'From a home with nothing,'
            pla['5'] = 'Having no parents at all,'
            part1 = random.choice([pla[i] for i in pla])
        elif LivingWith == "Parents":
            pla = {}
            pla['1'] = 'Growing up with {} parents,'.format(word1)
            pla['2'] = 'Living with {} parents,'.format(word1)
            pla['3'] = 'With {} parents,'.format(word1)
            pla['4'] = 'From a {} home,'.format(word1)
            pla['5'] = 'Having {} parents,'.format(word1)
            part1 = random.choice([pla[i] for i in pla])    
        elif LivingWith == "BrokenHome":
            pla = {}
            pla['1'] = 'Growing up in a troubled home,'
            pla['2'] = 'Living with parents that argued often,'
            pla['3'] = 'With parents that struggled to remain polite day after day,'
            pla['4'] = 'From a broken home,'
            pla['5'] = 'Having parents that argued non-stop,'
            part1 = random.choice([pla[i] for i in pla]) 
        elif LivingWith == "Mom":
            pla = {}
            pla['1'] = 'Growing up with only a mom,'
            pla['2'] = 'Living with {} mother,'.format(gender)
            pla['3'] = 'With a single mom,'
            pla['4'] = 'From a {} home that only had a mother-figure,'.format(word1)
            pla['5'] = 'Having a {} mom stay all the time,'.format(word1)
            part1 = random.choice([pla[i] for i in pla])         
        else:
            pla = {}
            pla['1'] = 'Growing up with only a dad,'
            pla['2'] = 'Living with {} father,'.format(gender)
            pla['3'] = 'With a single dad,'
            pla['4'] = 'From a {} home that only had a father-figure,'.format(word1)
            pla['5'] = 'Having a {} dad at home all-day long,'.format(word1)
            part1 = random.choice([pla[i] for i in pla])       
        pla2 = {}
        pla2['1'] = '{} lived in the {} of Floor {}.'.format(name, area, floor)
        pla2['2'] = '{} grew up in Floor {}.'.format(name, floor)
        pla2['3'] = '{} grew up in the {} of Floor {}.'.format(name, area, floor)
        pla2['4'] = '{} lived in Floor {}.'.format(name, floor)
        pla2['5'] = '{} made a life for themselves in Floor {}.'.format(name, floor)
        pla2['6'] = '{} spent {} early life in Floor {}.'.format(name, gender, floor)
        pla2['7'] = '{} spent {} early years in Floor {}.'.format(name, gender, floor)
        pla2['8'] = '{} spent {} early life in the {} of Floor {}.'.format(name, gender, area, floor)
        pla2['9'] = '{} spent {} early years in the {} of Floor {}.'.format(name, gender, area, floor)
        pla2['10'] = '{} was brought up in Floor {}.'.format(name, floor)
        pla2['11'] = '{} was brought up in the {} of Floor {}.'.format(name, area, floor)
        part2 = random.choice([pla2[i] for i in pla2])    
        
        times = ["time", "years", "early life", "childhood", "young years", "past"]   
        ti = random.choice(times)
        if UserLife == "Study":
            spent = ["studying", "reading about", "researching"] 
            spent2 = ["academics", "religion", "the world", "magic", "fighting", "martial arts"]   
            life1 = "{} {}".format(random.choice(spent), interest)
            while True:
                life2 = "{} {}".format(random.choice(spent), random.choice(spent2))
                if life2 != life1:
                    break
        elif UserLife == "Exploring":
            spent = ["exploring", "searching", "moving about"]   
            life1 = "{} {} home town".format(random.choice(spent), gender)   
            while True:
                spent2 = ["caves", "ruins", "abandoned houses"]   
                life2 = "{} nearby {}".format(random.choice(spent), random.choice(spent2))   
                if life2 != life1:
                    break    
        elif UserLife == "Gambling": 
            spent = ["betting on fights", "gambling", "playing risky games"]  
            life1 = random.choice(spent)
            while True:
                life2 = random.choice(spent)
                if life2 != life1:
                    break
        elif UserLife == "Fighting":
            spent = ["beating up", "fighting", "protecting"] 
            spent2 = ["bullies", "with {} best friend".format(gender), "strangers", "criminals", "stalkers", "wild animals"] 
            life1 = "{} {}".format(random.choice(spent), random.choice(spent2))  
            while True:
                life2 = "{} {}".format(random.choice(spent), random.choice(spent2))  
                if life2 != life1:
                    break
        else:
            life1 = "working"
            life2 = "making {} own money in life".format(gender)
            
        part3 = '{} spent most of {} {} {} and {}.'.format(gend, gender, ti, life1, life2)
        starters = ["But", "However,", "Later down the line,", "In time"]
        lasting = ["reaching the age of", "not long after turning", "when they were almost"]     
        aging = randint(10, (age - 2))
        last = random.choice(["was forced to leave home", "ran way from home", "left home", "was kicked out of {} home".format(gender), "found {} home destroyed".format(gender)])    
        part4 = "{} {} {} {} {}.".format(random.choice(starters), random.choice(lasting), str(aging), name, last)
        part5 = goal
        TheBackstory = "{} {} {} {} {}".format(part1, part2, part3, part4, part5)
        return TheBackstory
     

    def getGoal(self, name, ParentWealth, LivingWith, UserLife, personality, interest): 
        if name.endswith("s"):
            part1 = "{}' goal in life is to ".format(name)
        else:
            part1 = "{}'s goal in life is to ".format(name)
        if UserLife == "Study":
            words = ["learn more", "find out more", "study more", "research more", "collect as much information"]
            words2 = ["as possible", "", "as there is in the world", "as they can"]
            part2 = "{} about {} {}.".format(random.choice(words), interest, random.choice(words2))
        elif UserLife == "Exploring":
            words = ["explore", "search", "travel", "investigate", "traverse"]
            part2 = "{} all over the world in the name of {}.".format(random.choice(words), interest)
        elif UserLife == "Gambling":
            words = ["bet", "win", "gamble", "compete", "stake their life"]
            words2 = ["most expensive", "biggest", "most dangerous", "highest stake", "grandest"]
            part2 = "{} in the {} competition they can find.".format(random.choice(words), random.choice(words2))
        elif UserLife == "Fighting":
            words = ["get revenge on", "compete against", "fight against", "kill", "defeat"]
            words2 = ["the ruler of the tower", "the killer of their parents", "the strongest fighter in the world", "many strong opponents from their childhood"]
            part2 = "{} {}.".format(random.choice(words), random.choice(words2))
        else:
            words = ["a stable job", "the ultimate job", "love", "friendship", "a new family", "and build the ultimate harem"]
            part2 = "find {}.".format(random.choice(words))         
        goal = part1 + part2
        return goal
     
    def newCharacter(self, user, server):
        genders = ["Male", "Female", "Male", "Female", "Male"]
        gender = random.choice(genders)
        nameFile = "data/story/names/" + gender + ".txt"
        name = random.choice(open(nameFile).readlines()).replace("\n", "")
        type = random.choice(open(types).readlines())
        weapon = random.choice(open(weapons).readlines())
        nameFile = "data/story/weapons/" + weapon.replace("\n", "") + ".txt"
        PrimaryWeapon = random.choice(open(nameFile).readlines())
        faction = random.choice(open(factions).readlines())
        nameFile = "data/story/background/factions/" + faction.replace("\n", "") + ".txt"
        Role = random.choice(open(nameFile).readlines())
        personalities = ["Friendly", "Serious", "Smart", "Angry", "Carefree"]
        personality = random.choice(personalities)
        power = randint(100,500)
        age = randint(16, 25)
        floor = 1
        
        ParentMoney = ["Rich", "Normal", "Poor"]
        Parents = ["Orphan", "Parents", "Mom", "Dad", "BrokenHome"]
        Lifestype = ["Study", "Exploring", "Gambling", "Fighting", "Working"]
        ParentWealth = random.choice(ParentMoney)
        LivingWith = random.choice(Parents)
        UserLife = random.choice(Lifestype)
        
        interests = ["books", "religion", "love", "magic", "fighting", "martial arts", "gambling techniques", "cooking", "mechanics", "alchemy", "playing games", "friendship", "money"] 
        interest = random.choice(interests)
        
        goal = self.getGoal(name, ParentWealth, LivingWith, UserLife, personality, interest)
        
        #if server.id in self.settings:
            #floor = randint(1, self.settings[server.id]["Floor"])  
        backstory = self.backstory(name, gender, floor, age, type, weapon, faction, personality, power, ParentWealth, LivingWith, UserLife, interest, goal)    
        character = {
                "Floor" : floor,
                "CFloor" : floor,
                "Name" : name,
                "Weapon" : weapon,
                "PWeapon" : PrimaryWeapon,
                "CWeapon" : PrimaryWeapon,
                "Type" : type,
                "Personality" : personality,
                "Age" : age,
                "Health" : 100,
                "Power" : power,
                "Faction" : faction,
                "Role" : Role,
                "Goal" : goal,
                "Backstory" : backstory
            }
        return character
        
    def places(self, Name, Floor, AreaType):
        file = "data/story/" + AreaType + ".txt"
        area = random.choice(open(file).readlines())
        pla = {}
        pla['1'] = '{} woke up in the middle of a {}, Floor {}.'.format(Name, area, Floor)
        pla['2'] = '{} was wandering around a {}, a location in Floor {}.'.format(Name, area, Floor)
        pla['3'] = '{} stumbled around, finding a {} in Floor {} of the tower.'.format(Name, area, Floor)
        pla['4'] = 'It was Floor {} when {} found a {}'.format(Floor, Name, area) 
        pla['5'] = 'The {} was found in Floor {} where {} had been resting.'.format(area, Floor, Name)
        pla['6'] = '{} fell down, getting up just on the outskirts of a {}. They were on Floor {}.'.format(Name, area, Floor)
        pla['7'] = 'Floor {}, {} just left a {}.'.format(Floor, Name, area)
        return '{0}'.format(random.choice([pla[i] for i in pla]))  
        
    def items(self):
        file = "data/story/" + AreaType + ".txt"
        area = random.choice(open(file).readlines())
        pla = {}
        pla['1'] = '{} woke up in the middle of a {}, Floor {}.'.format(Name, area, Floor)
        pla['2'] = '{} was wandering around a {}, a location in Floor {}.'.format(Name, area, Floor)
        pla['3'] = '{} stumbled around, finding a {} in Floor {} of the tower.'.format(Name, area, Floor)
        pla['4'] = 'It was Floor {} when {} found a {}'.format(Floor, Name, area) 
        pla['5'] = 'The {} was found in Floor {} where {} had been resting.'.format(area, Floor, Name)
        pla['6'] = '{} fell down, getting up just on the outskirts of a {}. They were on Floor {}.'.format(Name, area, Floor)
        pla['7'] = 'Floor {}, {} just left a {}.'.format(Floor, Name, area)
        return '{0}'.format(random.choice([pla[i] for i in pla]))

    @commands.command(pass_context=True)
    async def tempcharacter(self, ctx):
        """Check your character"""
        user = ctx.message.author
        server = ctx.message.server
        character = self.newCharacter(user, server)
        embed = discord.Embed(colour=0xD8661A) 
        embed.title = "Test Character - " + user.name
        embed.add_field(name="Name", value=character["Name"])
        embed.add_field(name="Age", value=character["Age"])
        embed.add_field(name="Faction", value=character["Faction"])
        
        embed.add_field(name="Weapon Type", value=character["Weapon"])
        embed.add_field(name="Power", value=str(character["Power"]))
        embed.add_field(name="Role", value=character["Role"].capitalize())
        
        embed.add_field(name="Personal Weapon", value=character["PWeapon"].capitalize())
        embed.add_field(name="Player Type", value=str(character["Type"]))
        embed.add_field(name="Personality", value=character["Personality"])
        
        embed.add_field(name="Backstory", value=character["Backstory"])
        await self.bot.say(embed=embed)      
        
    @commands.command(pass_context=True)
    async def character(self, ctx):
        """Check your character"""
        user = ctx.message.author
        server = ctx.message.server
        return
        if server.id not in self.users:
            self.users[server.id] = {}
            fileIO('data/story/users.json', "save", self.users)
            await self.bot.say(user.mention + "You don't have a character and the story hasn't started on this server yet.")
            return
        if user.id in self.users[server.id]:
            character = self.newCharacter(user)
            self.users[server.id][user.id] = character
            fileIO('data/story/users.json', "save", self.users)
            await self.bot.say(user.mention + "Your character has been created.")
        else:
            await self.bot.say(user.mention + "Your character has not been created yet. Use the ``enterworld`` command.")    
        
    @commands.command(pass_context=True)
    async def enterworld(self, ctx):
        """Enter the story"""
        user = ctx.message.author
        server = ctx.message.server
        return
        if server.id not in self.users:
            self.users[server.id] = {}
            fileIO('data/story/users.json', "save", self.users)
        if user.id in self.users[server.id]:
            character = self.newCharacter(user)
            self.users[server.id][user.id] = character
            fileIO('data/story/users.json', "save", self.users)
            await self.bot.say(user.mention + "Your character has been created.")
        else:
            await self.bot.say(user.mention + "Your character has already been created.")
    
    @commands.command(pass_context=True)
    async def story(self, ctx):
        """Get a copy of the current story"""
        server = ctx.message.server
        channel = ctx.message.channel
        return
        if server.id not in self.users:
            self.users[server.id] = {}
            fileIO('data/story/users.json', "save", self.users)
            await self.bot.say(user.mention + "The story hasn't started on this server yet.")
            return
        file = "data/story/story/" + str(server.id) + ".txt"
        await self.bot.send_file(channel, file)
        
    @commands.command(pass_context=True)
    async def advance(self, ctx):
        """Move the story along"""
        user = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        return
        if server.id not in self.users:
            self.users[server.id] = {}
            fileIO('data/story/users.json', "save", self.users)
            await self.bot.say(user.mention + "You are not in this story, therefore you can't move it along.")
            return
        if user.id not in self.users[server.id]:
            await self.bot.say(user.mention + "You are not in this story, therefore you can't move it along.")
            return
        story = "data/story/story/" + str(server.id) + ".txt"
        if server.id not in self.settings:
            new_settings = {
                    "Floor" : 0,
                    "Chapter" : 1,
                    "AreaType" : "Plains",
                    "Objective" : "Reach the top.",
                    "CurrentObjective" : "Find the next floor"
                }
            self.settings[server.id] = new_settings
            fileIO('data/story/settings.json', "save", self.settings)
            Floor = self.settings[server.id]["Floor"]
            AreaType = self.settings[server.id]["AreaType"]
            Objective = self.settings[server.id]["Objective"]
            CurrentObjective = self.settings[server.id]["CurrentObjective"]
            Chapter = self.settings[server.id]["Chapter"] 
        else:
            Floor = self.settings[server.id]["Floor"]
            AreaType = self.settings[server.id]["AreaType"]
            Objective = self.settings[server.id]["Objective"]
            CurrentObjective = self.settings[server.id]["CurrentObjective"]
            Chapter = self.settings[server.id]["Chapter"] 
        msg = "**Chapter {}** \n\n".format(Chapter)
        msg += await self.getStart(server, Floor, AreaType, Objective, CurrentOnjective) + "\n"
        msg += await self.getMiddle(server, Floor, AreaType, Objective, CurrentOnjective) + "\n"
        msg += await self.getEnd(server, Floor, AreaType, Objective, CurrentOnjective)
        with open(story, "a") as myfile:
            myfile.write("\n" + msg + "\n")
        await self.bot.say(msg)
    
    async def getStart(self, server, Floor, AreaType, Objective, CurrentOnjective):
        users = self.users[server.id]
        count = randint(1,2)
        person = random.choice(users)
        name = person["Name"]
        place = self.places(name, Floor, AreaType)
        thing = self.items()
        msg = "{}".format(place)
        return msg
        
def check_folders():
    if not os.path.exists("data/story"):
        print("Creating data/story folder...")
        os.makedirs("data/story")  
        
def check_files():
  
    f = "data/story/settings.json"
    if not fileIO(f, "check"):
        print("Creating settings.json...")
        fileIO(f, "save", {})
  
    f = "data/story/users.json"
    if not fileIO(f, "check"):
        print("Creating users.json...")
        fileIO(f, "save", {})
        

def setup(bot):
    check_folders()
    check_files()
    n = Story(bot)
    bot.add_cog(n)   