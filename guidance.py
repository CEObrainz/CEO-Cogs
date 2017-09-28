import discord
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
from collections import namedtuple, defaultdict, deque
import platform, asyncio, string, operator, random, textwrap
import os, re, aiohttp
from .utils.dataIO import fileIO
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
import threading
from datetime import datetime
import time
from random import randint
import math

class Guidance:


    def reward(user, reward):
        guild = self.bot.get_cog("Guild")
        if reward == "Easy":
            item = "Amethyst Stone"
            price = 20000
        elif reward = "Medium"
            item = "Garnet Stone"
            price = 30000
        else reward = "Hard"
            item = "Sapphire Stone"
            price = 50000
        guild.add_item(user, item, 1, price)    

    def checking(user, line, number, server): 
        author = user
        self.users = fileIO("data/guild/users.json", "load")
        type = line.rsplit('-', 5)[1]
        if type == "Money":
            amount = line.rsplit('-', 5)[2]
            if guild.can_spend(author, int(amount)):
                reward = line.rsplit('-', 5)[3]
                self.reward(author, reward)
                self.users[server.id][author.id]["Guidance of Baraka"][number]["complete"] = True
        elif type == "Level":
            amount = line.rsplit('-', 5)[2]
            if guild.getStat(user, "Level") >= amount:
                reward = line.rsplit('-', 5)[3]
                self.reward(author, reward)
                self.users[server.id][author.id]["Guidance of Baraka"][number]["complete"] = True
        elif type == "Sale":
            amount = line.rsplit('-', 5)[2]
            if guild.getStat(user, "Level") >= amount:
                reward = line.rsplit('-', 5)[3]
                self.reward(author, reward)
                self.users[server.id][author.id]["Guidance of Baraka"][number]["complete"] = True
        elif type == "BambooCopter":
            amount = line.rsplit('-', 5)[2]
            if guild.get_quantity(user, "BambooCopter") >= amount:
                reward = line.rsplit('-', 5)[3]
                self.reward(author, reward)   
                self.users[server.id][author.id]["Guidance of Baraka"][number]["complete"] = True
        elif type == "House":
            amount = line.rsplit('-', 5)[2]
            if guild.getStat(user, "house") == True:
                reward = line.rsplit('-', 5)[3]
                self.reward(author, reward) 
                self.users[server.id][author.id]["Guidance of Baraka"][number]["complete"] = True
        elif type == "Shop":
            amount = line.rsplit('-', 5)[2]
            if guild.getStat(user, "shop") == True:
                reward = line.rsplit('-', 5)[3]
                self.reward(author, reward)  
                self.users[server.id][author.id]["Guidance of Baraka"][number]["complete"] = True
        fileIO('data/guild/users.json', "save", self.users)
        
        
    @commands.command(pass_context=True, no_pm=True)
    async def checkGuidance(self, ctx):
        """Check Guidance for trackable Objectives."""
        author = ctx.message.author
        server = author.server
        id = author.id
        guild = self.bot.get_cog("Guild")
        self.users = fileIO("data/guild/users.json", "load")
        if guild.account_exists(author):
            fname = "data/guidance/guidance.txt"
            with open(fname, 'r') as inF:
                for line in inF:
                    number = line.rsplit('-', 5)[0]
                    if number in self.users[server.id][author.id]["Guidance of Baraka"]:
                        if self.users[server.id][author.id]["Guidance of Baraka"][number]["complete"] == False:
                            self.checking(user, line, number, server)
                    else:
                        self.checking(user, line, number, server)
            await self.bot.say("All the possible guidance's have been checked Goshujinsama, if you have completed them .")                    
        else:
            await self.bot.say("You have not been blessed yet Goshujinsama, therefore you need to do ``Diana vocation blessing`` first.")
    
    
    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def guidance(self, ctx):
        """Guidance of Baraka"""
        author = ctx.message.author
        server = author.server
        id = author.id
        file = "data/guidance/guidance.txt"
        guild = self.bot.get_cog("Guild")
        self.users = fileIO("data/guild/users.json", "load")
        if len(self.users[server.id][author.id]["Guidance of Baraka"]) == 30:
            await self.bot.say("Goshujinsama, there is nothing else you can do with this command.")
            return
        while True:
            task = random.choice(open(file).readlines())
            if task.rsplit('-', 5)[0] not in self.users[server.id][author.id]["Guidance of Baraka"]:
                break
        number = task.rsplit('-', 5)[0]
        new_guidance = {
                    "type" : task.rsplit('-', 5)[1],
                    "amount" : task.rsplit('-', 5)[2],
                    "reward" : task.rsplit('-', 5)[3],
                    "text" : task.rsplit('-', 5)[4].replace("\n", ""),
                    "complete" : False
                    }
        
        self.users[server.id][author.id]["Guidance of Baraka"][number] = new_guidance
        fileIO('data/guild/users.json', "save", self.users)
        await self.bot.say("Goshujinsama, you have recieved a new guidance!")








def setup(bot):
    n = Guidance(bot)
    bot.add_cog(n)