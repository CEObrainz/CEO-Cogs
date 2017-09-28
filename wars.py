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
from random import randint
import logging
import math

class War:

    #leaderboard stuff

    def __init__(self, bot):
        self.bot = bot
        self.users = fileIO("data/war/users.json", "load")
        self.settings = fileIO("data/war/settings.json", "load")
        self.nations = fileIO("data/war/nations.json", "load")
    
    def saveUsers(self):
        dataIO.save_json("data/war/users.json", self.users)
    
    def hasAccount(self, user):
        if user.id in self.users:
            return True
        return False
        
    def decreaseHealth(self, user, amount):
        self.users[user.id]["Health"] -= amount
        if self.users[user.id]["Health"] <= 0:
            self.users[user.id]["Health"] = 0
        self.saveUsers() 
    
    def getLevel(self, user):
        return self.users[user.id]["Level"]
        
    def canSpend(self, user, resource, amount):
        if self.users[user.id][resource] > amount:
            return True
        return False
        
    def addResource(self, user, resource, amount):
        self.users[user.id][resource] += amount
        self.saveUsers()    
        
    def removeResource(self, user, resource, amount):
        self.users[user.id][resource] -= amount
        if self.users[user.id][resource] < 0:
            self.users[user.id][resource] = 0
        self.saveUsers()      
        
    def addXP(self, user, amount):
        self.users[user.id]["XP"] += amount
        if self.users[user.id]["Level"] < 100:
            xpNeeded = self.users[user.id]["Level"] * 100
            if self.users[user.id]["XP"] > xpNeeded:
                self.users[user.id]["MaxHealth"] += 50
                self.users[user.id]["Health"] = self.users[user.id]["MaxHealth"]
        self.saveUsers()
    
    def roleLevel(self, user):
        roles = [x.name for x in user.roles if x.name != "@everyone"]
        if "Copper" in roles:
            return 1.2
        elif "Iron" in roles:
            return 1.4
        elif "Silver" in roles:
            return 1.6
        elif "Gold" in roles:
            return 1.8
        elif "Platinum" in roles:
            return 2.0
        elif "Mythril" in roles:
            return 2.2
        elif "Orichalcum" in roles:
            return 2.4
        elif "Adamantite" in roles:
            return 2.6
        elif "Hero" in roles:
            return 2.8
        elif "Nazarick" in roles:
            return 3.0  
        else:
            return 1
      
    def priceB(self, resource, UnitsDemanded):
        name = resource + "C-Rate"
        value = len(self.users)
        #Price = BasePrice * (LocalDemand + DemandFactor * UnitsDemanded) / (LocalSupply + SupplyFactor * UnitsSupplied)
        rn = resource + "C"
        LS = self.nations["Nazarick"][rn]
        rnn = rn + "-Sold"
        rnc = rn + "-Amount"
        DemandFactor = self.settings[rnn]
        SupplyFactor = self.settings[rnc]
        Price1 = 10 + int(self.settings[name]) * ((value + DemandFactor * 1) / (1 + (LS + SupplyFactor * 1)))
        Price2 = 10 + int(self.settings[name]) * ((value + DemandFactor * 1) / (1 + (LS - 1 + SupplyFactor * 1)))
        Price = int((Price1 + Price2) / 2) * UnitsDemanded
        return Price
        
    def priceS(self, resource, UnitsDemanded):
        name = resource + "C-Rate"
        value = len(self.users)
        #Price = BasePrice * (LocalDemand + DemandFactor * UnitsDemanded) / (LocalSupply + SupplyFactor * UnitsSupplied)
        rn = resource + "C"
        LS = self.nations["Nazarick"][rn]
        rnn = rn + "-Sold"
        rnc = rn + "-Amount"
        DemandFactor = self.settings[rnn]
        SupplyFactor = self.settings[rnc]
        Price1 = 10 + int(self.settings[name]) * ((value + (DemandFactor * 0)) / (1 + (LS + SupplyFactor * 1)))
        Price2 = 10 + int(self.settings[name]) * ((value + (DemandFactor * 0)) / (1 + (LS - 1 + SupplyFactor * 1)))
        Price = int((Price1 + Price2) / 2) * UnitsDemanded
        return Price
    
    def display_time(self, seconds, granularity=2): # What would I ever do without stackoverflow?
        intervals = (                               # Source: http://stackoverflow.com/a/24542445
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),    # 60 * 60 * 24
            ('hours', 3600),    # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
            )

        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])
    
    @commands.group(no_pm=True, pass_context=True)
    @checks.is_owner()
    @checks.overlord_server()
    async def setwar(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            
    @setwar.command(pass_context=True, no_pm=True) 
    async def test(self, ctx):
        channel = ctx.message.channel
        file = "data/pictures/nations.psd"
        psd = PSDImage.load(file)
        nations = psd.layers[2].layers[4].as_PIL()
       
        nations.save('data/pictures/nations.png')
        file = "data/pictures/nations.png"
        await self.bot.send_file(destination=channel, fp=file)
        
        
    
    @setwar.command(pass_context=True, no_pm=True) 
    async def leader(self, ctx, user: discord.Member=None):
        if user.id not in self.users:
            await self.bot.say("The user you specified does not have a Nation Wars account yet.")
            return
        self.users[user.id]["Role"] = "Leader"
        dataIO.save_json("data/war/users.json", self.users)
        nation = self.users[user.id]["Nation"]
        await self.bot.say("{} has been made a leader of the {}.".format(user.mention, nation))
    
    @setwar.command(pass_context=True, no_pm=True) 
    async def citizen(self, ctx, user: discord.Member=None):
        if user.id not in self.users:
            await self.bot.say("The user you specified does not have a Nation Wars account yet.")
            return
        self.users[user.id]["Role"] = "Citizen"
        dataIO.save_json("data/war/users.json", self.users)
        nation = self.users[user.id]["Nation"]
        await self.bot.say("{} has been made a citizen of the {}.".format(user.mention, nation))
    
    @setwar.command(pass_context=True, no_pm=True) 
    async def reseta(self, ctx):
        self.users = {}
        defaultSettings = {
            "EmpireC-Amount" : 5,
            "EmpireC-Rate" : 500,
            "EmpireC-Sold" : 5,
            "EmpireC-Name" : "Rubite Ore",
            "KingdomC-Amount" : 5,
            "KingdomC-Rate" : 500,
            "KingdomC-Sold" : 5,
            "KingdomC-Name" : "Ematite Ore",
            "Mine-Amount" : 10,
            "Mine-GoldAmount" : 10,
            "Mine-Time" : 900,
            "TheocracyC-Amount" : 5,
            "TheocracyC-Rate" : 500,
            "TheocracyC-Sold" : 5,
            "TheocracyC-Name" : "Sardite Ore",
            "NazarickC-Name" : "Gold",
            "NazarickID" : 346301265581703169,
        }
        self.settings = defaultSettings
        Nazarick = {
                "NazarickC" : 100000,
                "KingdomC" : 10,
                "EmpireC" : 10,
                "TheocracyC" : 10,
                "DataCrystals" : 0
            }
        Kingdom = {
                "NazarickC" : 1000,
                "KingdomC" : 100,
                "EmpireC" : 100,
                "TheocracyC" : 100,
                "DataCrystals" : 0
            }
        Empire = {
                "NazarickC" : 1000,
                "KingdomC" : 100,
                "EmpireC" : 100,
                "TheocracyC" : 100,
                "DataCrystals" : 0
            }
        Theocracy = {
                "NazarickC" : 1000,
                "KingdomC" : 100,
                "EmpireC" : 100,
                "TheocracyC" : 100,
                "DataCrystals" : 0
            }    
        DefaultNations = {
            "Nazarick" : Nazarick,
            "Kingdom" : Kingdom,
            "Empire" : Empire,
            "Theocracy" : Theocracy
        }
        self.nations = DefaultNations
        dataIO.save_json("data/war/nations.json", self.nations)
        dataIO.save_json("data/war/settings.json", self.settings)
        dataIO.save_json("data/war/users.json", self.users)
        await self.bot.say("Big boom boom, everything has been reset!")        
            
    @setwar.command(pass_context=True, no_pm=True) 
    async def resetu(self, ctx):
        self.users = {}
        dataIO.save_json("data/war/users.json", self.users)
        await self.bot.say("All users reset")
        
    @setwar.command(pass_context=True, no_pm=True) 
    async def resets(self, ctx):
        defaultSettings = {
            "EmpireC-Amount" : 5,
            "EmpireC-Rate" : 500,
            "EmpireC-Sold" : 5,
            "EmpireC-Name" : "Rubite Ore",
            "KingdomC-Amount" : 5,
            "KingdomC-Rate" : 500,
            "KingdomC-Sold" : 5,
            "KingdomC-Name" : "Ematite Ore",
            "Mine-Amount" : 3,
            "Mine-GoldAmount" : 10,
            "Mine-Time" : 900,
            "TheocracyC-Amount" : 5,
            "TheocracyC-Rate" : 500,
            "TheocracyC-Sold" : 5,
            "TheocracyC-Name" : "Sardite Ore",
            "NazarickC-Name" : "Gold",
            "NazarickID" : 346301265581703169,
        }
        self.settings = defaultSettings
        dataIO.save_json("data/war/settings.json", self.settings)
        await self.bot.say("All settings reset")    
     
    @setwar.command(pass_context=True, no_pm=True) 
    async def resetn(self, ctx):
        Nazarick = {
                "NazarickC" : 100000,
                "KingdomC" : 100,
                "EmpireC" : 100,
                "TheocracyC" : 100,
                "DataCrystals" : 0
            }
        Kingdom = {
                "NazarickC" : 1000,
                "KingdomC" : 100,
                "EmpireC" : 100,
                "TheocracyC" : 100,
                "DataCrystals" : 0
            }
        Empire = {
                "NazarickC" : 1000,
                "KingdomC" : 100,
                "EmpireC" : 100,
                "TheocracyC" : 100,
                "DataCrystals" : 0
            }
        Theocracy = {
                "NazarickC" : 1000,
                "KingdomC" : 100,
                "EmpireC" : 100,
                "TheocracyC" : 100,
                "DataCrystals" : 0
            }    
        DefaultNations = {
            "Nazarick" : Nazarick,
            "Kingdom" : Kingdom,
            "Empire" : Empire,
            "Theocracy" : Theocracy
        }
        self.nations = DefaultNations
        dataIO.save_json("data/war/nations.json", self.nations)
        await self.bot.say("All Nations reset")
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def register(self, ctx):
        """Register as part of your nation."""
        user = ctx.message.author
        server = ctx.message.server
        if user.id in self.users:
            await self.bot.say("You already have an account.")
            return
        if user.id not in self.users:
            roles = user.roles
            king = discord.utils.get(server.roles, name="Kingdom")
            emp = discord.utils.get(server.roles, name="Empire")
            theo = discord.utils.get(server.roles, name="Theocracy")
            if king in roles:
                nation = "Re-Estize Kingdom"
                nation_name = "Kingdom"
            elif emp in roles:
                nation = "Baharuth Empire"
                nation_name = "Empire"
            elif theo in roles:
                nation = "Slane Theocracy"
                nation_name = "Theocracy"
            else:
                await self.bot.say("You are not in a nation, please join one before trying to register.")
                return
            seconds = abs(int(time.perf_counter()) - self.settings["Mine-Time"])
            newUser = {
                "Nation" : nation,
                "Name" : nation_name,
                "Role" : "Citizen",
                "Rank" : 10,
                "Level" : 1,
                "Health" : 100,
                "MaxHealth" : 100,
                "XP" : 0,
                "Location" : nation_name,
                "TimesMined" : 0,
                "TotalMined" : 0,
                "NazarickC" : 100,
                "KingdomC" : 0,
                "EmpireC" : 0,
                "TheocracyC" : 0,
                "DataCrystals" : 0,
                "BattlesWon" : 0,
                "time" : seconds,
                "Loot" : 0,
                "locateX" : 0,
                "locateY" : 0,
                "Floor" : 0,
                }
            self.users[user.id] = newUser
        dataIO.save_json("data/war/users.json", self.users)
        await self.bot.say("Thank you for registering, have fun!")
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server() 
    async def potion(self, ctx):
        """Restore Health to full."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        if self.users[user.id]["MaxHealth"] == self.users[user.id]["Health"]:
            await self.bot.say("{} You already have max health.".format(user.mention))
            return
        if self.canSpend(user, "NazarickC", 10):
            self.removeResource(user, "NazarickC", 10)
            self.users[user.id]["Health"] = self.users[user.id]["MaxHealth"]
            await self.bot.say("{} You need to use the register command first.".format(user.mention))
            return
        else:
            await self.bot.say("{} You need 10 Gold to use this command. Current Balance: {} Gold".format(user.mention, self.users[user.id]["NazarickC"]))
            return
        
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def mine(self, ctx):
        """Mine Resources from your nation."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        seconds = abs(self.users[user.id]["time"] - int(time.perf_counter()))
        if seconds >= self.settings["Mine-Time"]:
            timer = self.roleLevel(user)
            word = self.users[user.id]["Name"] + "C"
            today = randint(10, 1000)
            amount = int(timer * today)
            earnings = int(self.priceS(self.users[user.id]["Name"], amount) / 100)
            if earnings > 1000:
                taxrate = 0.5
            elif earnings > 500:
                taxrate = 0.25
            else:
                taxrate = 0.10
            tax = int(earnings * taxrate)
            earningsAfter = 25 + (earnings - tax)
            self.users[user.id]["NazarickC"] += earningsAfter
            self.users[user.id]["time"] = int(time.perf_counter())
            self.users[user.id]["TimesMined"] += 1
            self.addXP(user, 1)
            self.users[user.id]["TotalMined"] += amount
            dataIO.save_json("data/war/users.json", self.users)
            wordamount = self.users[user.id]["Name"] + "C-Amount" 
            self.settings[wordamount] += amount
            dataIO.save_json("data/war/settings.json", self.settings)
            nation_name = self.users[user.id]["Name"]
            self.nations[nation_name][word] += int((amount / 100) * 20)
            self.nations["Nazarick"][word] += int((amount / 100) * 80)
            dataIO.save_json("data/war/nations.json", self.nations)
            embed = discord.Embed(colour=0xD8661A) 
            ore = self.users[user.id]["Name"] + "C-Name"
            embed.title = user.name + " - Mining Report: " + self.settings[ore]
            embed.add_field(name="Report Number", value="#" + str(self.users[user.id]["TimesMined"]))
            embed.add_field(name="Salary", value="25 Gold (Not taxed)")
            embed.add_field(name="Total Mined", value=amount)
            embed.add_field(name="Earnings before Tax", value=str(earnings) + " Gold")
            embed.add_field(name="Tax", value=str(tax) + " Gold")
            embed.add_field(name="Earnings after Tax", value=str(earningsAfter) + " Gold")
            await self.bot.say(embed=embed) 
        else:
            await self.bot.say("{} To mine again you'll have to wait at least {}.".format(user.mention, self.display_time(self.settings["Mine-Time"] - seconds)))
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()    
    async def wallet(self, ctx):
        """Player wallet."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        embed = discord.Embed(colour=0xD8661A) 
        embed.title = user.name + " - " + self.users[user.id]["Role"] + " of the " + self.users[user.id]["Nation"]
        embed.add_field(name="Gold", value= self.users[user.id]["NazarickC"])
        embed.add_field(name="Kingdom: " + self.settings["KingdomC-Name"], value= self.users[user.id]["KingdomC"])
        embed.add_field(name="Empire: " + self.settings["EmpireC-Name"], value= self.users[user.id]["EmpireC"])
        embed.add_field(name="Theocracy: " + self.settings["TheocracyC-Name"], value= self.users[user.id]["TheocracyC"])
        embed.add_field(name="Data Crystals", value= self.users[user.id]["DataCrystals"])
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server() 
    async def status(self, ctx):
        """Player status."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        embed = discord.Embed(colour=0xD8661A)
        embed.title = user.name + " status"
        embed.add_field(name="Title", value=self.users[user.id]["Role"] + " of the " + self.users[user.id]["Nation"])
        Location = self.users[user.id]["Location"]
        if ctx.message.server.id == "346301265581703169":
            Location = "Nazarick - Floor: " + str(self.users[user.id]["Floor"])
            embed.add_field(name="Loot", value=str(self.users[user.id]["Loot"]), inline=False)
        embed.add_field(name="Location", value=Location, inline=False)
        embed.add_field(name="Level", value= self.users[user.id]["Level"])
        embed.add_field(name="Health", value= self.users[user.id]["Health"])
        embed.add_field(name="XP", value= self.users[user.id]["XP"])
        embed.add_field(name="Balance", value= self.users[user.id]["NazarickC"])
        embed.add_field(name="Data Crystals", value= self.users[user.id]["DataCrystals"])
        embed.add_field(name="Battles won", value= self.users[user.id]["BattlesWon"])
        await self.bot.say(embed=embed)       
        
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()    
    async def vault(self, ctx):
        """National wallet."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        nation_name = self.users[user.id]["Nation"]
        nation = self.users[user.id]["Name"]
        embed = discord.Embed(colour=0xD8661A) 
        embed.title = nation_name + " Vault"
        embed.add_field(name="Gold", value= self.nations[nation]["NazarickC"])
        embed.add_field(name="Kingdom: " + self.settings["KingdomC-Name"], value= self.nations[nation]["KingdomC"])
        embed.add_field(name="Empire: " + self.settings["EmpireC-Name"], value= self.nations[nation]["EmpireC"])
        embed.add_field(name="Theocracy: " + self.settings["TheocracyC-Name"], value= self.nations[nation]["TheocracyC"])
        embed.add_field(name="Data Crystals", value= self.nations[nation]["DataCrystals"])
        await self.bot.say(embed=embed)   

    @commands.command(pass_context=True, no_pm=True)  
    @checks.overlord_server()
    async def stock(self, ctx):
        """Nazarick current stock"""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        embed = discord.Embed(colour=0xD8661A) 
        embed.title = "Nazarick Stock"
        embed.add_field(name="Gold", value= self.nations["Nazarick"]["NazarickC"])
        embed.add_field(name="Kingdom: " + self.settings["KingdomC-Name"], value= self.nations["Nazarick"]["KingdomC"])
        embed.add_field(name="Empire: " + self.settings["EmpireC-Name"], value= self.nations["Nazarick"]["EmpireC"])
        embed.add_field(name="Theocracy: " + self.settings["TheocracyC-Name"], value= self.nations["Nazarick"]["TheocracyC"])
        embed.add_field(name="Data Crystals", value= self.nations["Nazarick"]["DataCrystals"])
        await self.bot.say(embed=embed)  

    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def prices(self, ctx):
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        embed = discord.Embed(colour=0xD8661A) 
        embed.title = "Nazarick Trade Prices"
        embed.add_field(name="Kingdom - Buying", value= self.priceS("Kingdom", 1), inline=True)
        embed.add_field(name="Kingdom - Selling", value= self.priceB("Kingdom", 1), inline=False)
        embed.add_field(name="Empire - Buying", value= self.priceS("Empire", 1), inline=True)
        embed.add_field(name="Empire - Selling", value= self.priceB("Empire", 1), inline=False)
        embed.add_field(name="Theocracy - Buying", value= self.priceS("Theocracy", 1), inline=True)
        embed.add_field(name="Theocracy - Selling", value= self.priceB("Theocracy", 1), inline=False)
        await self.bot.say(embed=embed)      
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def buy(self, ctx, nation, amount : int):
        """Buy Resources from Nazarick."""
        user = ctx.message.author
        TheNations = ["Kingdom", "Empire", "Theocracy"]
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        nation = nation.capitalize()
        if nation == "nazarick":
            await self.bot.say("You can't buy gold.")
            return
        if amount < 1:
            await self.bot.say("You must input more than 1.")
            return
        if nation not in TheNations:
            await self.bot.say("You have entered an incorrect nation." + " Output was: " + repr(nation))
            return
        name = nation + "C"
        ore = name + "-Name"
        if amount > self.nations["Nazarick"][name]:
            await self.bot.say("Nazarick does not have enough {} at the moment. Current stock: {}".format(self.settings[ore], self.nations["Nazarick"][name]))
            return
        price = self.priceB(nation, amount)
        await self.bot.say("To buy {} {} from this nation it will cost you {} gold, do you wish to continue? y/n".format(amount, self.settings[ore], price))
        while True:
            msg = await self.bot.wait_for_message(timeout=90, channel=ctx.message.channel, author=user)
            if msg is not None:
                if msg.content == "y" or msg.content == "Y" or msg.content == "Yes" or msg.content == "yes":
                    if self.users[user.id]["NazarickC"] >= price:
                        self.users[user.id][name] += amount
                        self.users[user.id]["NazarickC"] -= price
                        dataIO.save_json("data/war/users.json", self.users)
                        self.nations["Nazarick"][name] -= amount
                        self.nations["Nazarick"]["NazarickC"] += price
                        dataIO.save_json("data/war/nations.json", self.nations)
                        rcn = name + "-Sold"
                        self.settings[rcn] += amount
                        dataIO.save_json("data/war/settings.json", self.settings)
                        await self.bot.say(user.mention + " You bought {} units of {}.".format(amount, self.settings[ore]))
                        return
                    else:
                        await self.bot.say("You lack the required funds for this transaction.")
                        return
                else:
                    await self.bot.say("Trade Cancelled.")
                    return
            else:
                await self.bot.say("Trade Cancelled.")
                return
                
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def sell(self, ctx, nation, amount : int):
        """Sell Resources to Nazarick."""
        user = ctx.message.author
        TheNations = ["Kingdom", "Empire", "Theocracy"]
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        nation = nation.capitalize()
        if nation == "nazarick":
            await self.bot.say("You can't sell gold.")
            return
        if amount < 1:
            await self.bot.say("You must input more than 1.")
            return
        if nation not in TheNations:
            await self.bot.say("You have entered an incorrect nation." + " Output was: " + repr(nation))
            return
        name = nation + "C"
        ore = name + "-Name"
        if amount > self.users[user.id][name]:
            await self.bot.say("You do not have enough {} at the moment. Current stock: {}".format(self.settings[ore], self.users[user.id][name]))
            return
        price = self.priceS(nation, amount)
        await self.bot.say("If you sell {} units of {} you will gain {} Gold, do you wish to continue? y/n".format(amount, self.settings[ore], price))
        while True:
            msg = await self.bot.wait_for_message(timeout=90, channel=ctx.message.channel, author=user)
            if msg is not None:
                if msg.content == "y" or msg.content == "Y" or msg.content == "Yes" or msg.content == "yes":
                    if self.nations["Nazarick"]["NazarickC"] >= price:
                        self.users[user.id][name] -= amount
                        self.users[user.id]["NazarickC"] += price
                        dataIO.save_json("data/war/users.json", self.users)
                        self.nations["Nazarick"][name] += amount
                        self.nations["Nazarick"]["NazarickC"] -= price
                        dataIO.save_json("data/war/nations.json", self.nations)
                        await self.bot.say(user.mention + " You sold {} units of {} for {} Gold.".format(amount, self.settings[ore], price))
                        return
                    else:
                        await self.bot.say("Nazarick lacks the required funds for this transaction.")
                        return
                else:
                    await self.bot.say("Trade Cancelled.")
                    return
            else:
                await self.bot.say("Trade Cancelled.")
                return
                
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()    
    async def give(self, ctx, nation, amount : int, user: discord.Member=None):
        """Give Resources to other users."""
        author = ctx.message.author
        TheNations = ["Kingdom", "Empire", "Theocracy", "Nazarick"]
        if author.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        if user.id not in self.users:
            await self.bot.say("The user you specified does not have a Nation Wars account yet.")
            return
        if amount < 1:
            await self.bot.say("You must input more than 1.")
            return
        if nation not in TheNations:
            await self.bot.say("You have entered an incorrect nation." + " Output was: " + repr(nation))
            return
        name = nation + "C" 
        ore = name + "-Name"    
        if amount > self.users[author.id][name]:
            await self.bot.say("You do not have enough {} at the moment. Current stock: {}".format(self.settings[ore], self.users[user.id][name]))
            return
        self.users[user.id][name] += amount    
        self.users[author.id][name] -= amount  
        dataIO.save_json("data/war/users.json", self.users)
        await self.bot.say("{} has given {} {} to {}.".format(author.mention, amount, self.settings[ore], user.mention))
        
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def donate(self, ctx, nation, amount : int):
        """Donate Resources to your nation."""
        user = ctx.message.author
        TheNations = ["Kingdom", "Empire", "Theocracy", "Nazarick"]
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        if amount < 1:
            await self.bot.say("You must input more than 1.")
            return
        if nation not in TheNations:
            await self.bot.say("You have entered an incorrect nation." + " Output was: " + repr(nation))
            return
        name = nation + "C"      
        ore = name + "-Name" 
        if amount > self.users[user.id][name]:
            await self.bot.say("You do not have enough {} at the moment. Current stock: {}".format(self.settings[ore], self.users[user.id][name]))
            return 
        self.users[user.id][name] -= amount    
        self.nations[nation][name] += amount  
        nation_name = self.users[user.id]["Nation"]
        dataIO.save_json("data/war/users.json", self.users)
        dataIO.save_json("data/war/nations.json", self.nations)
        await self.bot.say("{} has donated {} {} to the {}.".format(user.mention, amount, self.settings[ore], nation_name))    
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def data(self, ctx):
        """Create a Data Crystal."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        if self.users[user.id]["NazarickC"] < 5000:
            await self.bot.say("You need 5000 gold to use this command.")
            return
        if self.users[user.id]["KingdomC"] < 500:
            await self.bot.say("You need 500 Ematite Ore to use this command.")
            return
        if self.users[user.id]["EmpireC"] < 500:
            await self.bot.say("You need 500 Rubite Ore to use this command.")
            return
        if self.users[user.id]["TheocracyC"] < 500:
            await self.bot.say("You need 500 Sardite Ore to use this command.")
            return
        await self.bot.say(user.mention + "You are about to spend 5000 Gold, 500 Ematite, 500 Rubite and 500 Sardite to create a Data Crystal. Do you wish to continue? y/n")
        while True:
            msg = await self.bot.wait_for_message(timeout=90, channel=ctx.message.channel, author=user)
            if msg is None:
                await self.bot.say(user.mention + " The creation timed out.")
                return
            if msg.content == "y" or msg.content == "Y" or msg.content == "Yes" or msg.content == "yes":
                #do it
                self.users[user.id]["NazarickC"] -= 5000
                self.users[user.id]["KingdomC"] -= 500
                self.users[user.id]["EmpireC"] -= 500
                self.users[user.id]["TheocracyC"] -= 500
                self.users[user.id]["DataCrystals"] += 1
                dataIO.save_json("data/war/users.json", self.users)
                await self.bot.say(user.mention + " You have gained 1 Data Crystal!")
                return
            else:
                await self.bot.say(user.mention + " Process cancelled.")
                return
                
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def credit(self, ctx, nation, amount : int, user: discord.Member=None):
        """Give a member of your nation resources."""
        author = ctx.message.author
        TheNations = ["Kingdom", "Empire", "Theocracy", "Nazarick"]
        if author.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        if self.users[author.id]["Role"] is not "Leader":
            await self.bot.say("You need to be a leader to use this command.")
            return    
        if nation not in TheNations:
            await self.bot.say("You have entered an incorrect nation." + " Output was: " + repr(nation))
            return
        if amount < 1:
            await self.bot.say("You must input more than 1.")
            return    
        if user.id not in self.users:
            await self.bot.say("The user you specified does not have a Nation Wars account yet.")
            return    
        nation = self.users[author.id]["Name"]    
        if self.users[user.id]["Name"] is not nation:
            await self.bot.say("You can only give resources to members of your own nation.")
            return
        resource = nation + "C"
        if amount > self.nations[nation][resource]:
            await self.bot.say("You don't have enough resources to do this. Amount in Vault: ".format(self.nations[nation][resource]))
            return
        self.nations[nation][resource] -= amount
        self.users[user.id][resource] += amount
        dataIO.save_json("data/war/users.json", self.users)
        dataIO.save_json("data/war/nations.json", self.nations)
        nation_name = self.users[user.id]["Name"]
        ore = nation + "C-Name"
        await self.bot.say("The {} has credited {} with {} {}.".format(nation_name, user.mention, amount, self.settings[ore]))    
                
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()
    async def nationdata(self, ctx):
        """Create a Data Crystal for your Nation."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        nation = self.users[user.id]["Name"]
        if self.users[user.id]["Role"] is not "Leader":
            await self.bot.say("You need to be a leader to use this command.")
            return    
        if self.nations[nation]["NazarickC"] < 5000:
            await self.bot.say("You need 500 gold to use this command.")
            return
        if self.nations[nation]["KingdomC"] < 500:
            await self.bot.say("You need 500 Ematite Ore to use this command.")
            return
        if self.nations[nation]["EmpireC"] < 500:
            await self.bot.say("You need 500 Rubite Ore to use this command.")
            return
        if self.nations[nation]["TheocracyC"] < 500:
            await self.bot.say("You need 500 Sardite Ore to use this command.")
            return
        await self.bot.say(user.mention + "You are about to spend 5000 Gold, 500 Ematite, 500 Rubite and 500 Sardite to create a Data Crystal. Do you wish to continue? y/n")
        while True:
            msg = await self.bot.wait_for_message(timeout=90, channel=ctx.message.channel, author=user)
            if msg is not None:
                await self.bot.say(user.mention + " The creation timed out.")
                return
            if msg.content == "y" or msg.content == "Y" or msg.content == "Yes" or msg.content == "yes":
                #do it
                self.nations[nation]["NazarickC"] -= 5000
                self.nations[nation]["KingdomC"] -= 500
                self.nations[nation]["EmpireC"] -= 500
                self.nations[nation]["TheocracyC"] -= 500
                self.nations[nation]["DataCrystals"] += 1
                dataIO.save_json("data/war/nations.json", self.nations)
                await self.bot.say(user.mention + "Your nation has gained 1 Data Crystal!")
                return
            else:
                await self.bot.say(user.mention + " Process cancelled.")
                return
                
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()    
    async def warp(self, ctx):
        """Create a warp spell to Nazarick."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        if self.users[user.id]["DataCrystals"] < 1:
            await self.bot.say("You need a Data Crystal to use this command.")
            return
        await self.bot.say(user.mention + "You are about to use a Data Crystal to send yourself to the Great Tomb of Nazarick. Do you wish to continue? y/n")
        while True:
            msg = await self.bot.wait_for_message(timeout=90, channel=ctx.message.channel, author=user)
            if msg is None:
                await self.bot.say(user.mention + " The spell creation timed out.")
                return
            if msg.content == "y" or msg.content == "Y" or msg.content == "Yes" or msg.content == "yes":
                server = self.bot.get_server("346301265581703169")
                place = server.get_channel("346301265581703173")
                self.users[user.id]["DataCrystals"] -= 1
                dataIO.save_json("data/war/users.json", self.users)
                invite = await self.bot.create_invite(place, max_age=1800, max_uses=1)
                await self.bot.send_message(user, invite)
                return
            else:
                await self.bot.say(user.mention + " Process cancelled.")
                return
                
    @commands.command(pass_context=True, no_pm=True)
    @checks.overlord_server()    
    async def nationwarp(self, ctx, number : int):
        """Create a warp spell to Nazarick."""
        user = ctx.message.author
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return
        nation = self.users[user.id]["Name"]
        if self.users[user.id]["Role"] is not "Leader":
            await self.bot.say("You need to be a leader to use this command.")
            return 
        if number < 1:
            await self.bot.say("You must input 1 or more.")
            return    
        if self.users[user.id]["DataCrystals"] < 1:
            await self.bot.say("You need a Data Crystal to use this command.")
            return
        amount = 100 * number
        if self.nations[nation]["NazarickC"] < amount:
            await self.bot.say("You need more gold to send that many people.")
            return
        await self.bot.say(user.mention + "You are about to use a Data Crystal to send yourself and others to the Great Tomb of Nazarick. Do you wish to continue? y/n")
        while True:
            msg = await self.bot.wait_for_message(timeout=90, channel=ctx.message.channel, author=user)
            if msg is None:
                await self.bot.say(user.mention + " The spell creation timed out.")
                return
            if msg.content == "y" or msg.content == "Y" or msg.content == "Yes" or msg.content == "yes":
                server = self.bot.get_server("346301265581703169")
                place = server.get_channel("346301265581703173")
                self.users[user.id]["DataCrystals"] -= 1
                dataIO.save_json("data/war/users.json", self.users)
                invite = self.bot.create_invite(place, max_age=1800, max_uses=number)
                await self.bot.send_message(user, invite)
                return
            else:
                await self.bot.say(user.mention + " Process cancelled.")
                return
     
    def search(self, values, searchFor):
        TheList = []
        for k in values:
            if values[k]["Name"] == searchFor:
                TheList.append(k)
        return TheList
     
    @commands.command(pass_context=True)
    @checks.overlord_server()  
    async def mineboard(self, ctx, top : int=10):
        """Check the Mining Leaderboard for you nation."""
        user = ctx.message.author
        if top < 1:
            top = 10
        if user.id not in self.users:
            await self.bot.say("You need to use the register command first.")
            return  
        nation = self.users[user.id]["Name"]
        copyList = deepcopy(self.users)
        nationList = self.search(copyList, nation)
        bank_sorted = sorted(nationList, key=lambda x: copyList[x]["TotalMined"], reverse=True) 
        if len(bank_sorted) < top:
            top = len(bank_sorted)
        topten = bank_sorted[:top]
        #highscore = ""
        embed = discord.Embed(colour=0xD8661A)
        embed.title = "National Mining Leaderboard"
        place = 1
        for acc in topten:
            member = await self.bot.get_user_info(acc)
            embed.add_field(name=str(place) + " - " + member.name, value="Total Mined: " + str(copyList[acc]["TotalMined"]), inline=False)
            place += 1
        await self.bot.say(embed=embed)
        
def check_folders():
    if not os.path.exists("data/war"):
        print("Creating data/war folder...")
        os.makedirs("data/war")  
        
def check_files():
  
    f = "data/war/settings.json"
    if not fileIO(f, "check"):
        print("Creating settings.json...")
        fileIO(f, "save", {})
  
    f = "data/war/users.json"
    if not fileIO(f, "check"):
        print("Creating users.json...")
        fileIO(f, "save", {})
        
    f = "data/war/nations.json"
    if not fileIO(f, "check"):
        print("Creating nations.json...")
        fileIO(f, "save", {})
        
def setup(bot):
    check_folders()
    check_files()
    n = War(bot)
    bot.add_cog(n)   