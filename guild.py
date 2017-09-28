import discord
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
from cogs.utils.dataIO import dataIO
from collections import namedtuple, defaultdict, deque
import platform, asyncio, string, operator, random, textwrap
import os, re, aiohttp
from cogs.utils.chat_formatting import pagify, box
from .utils.dataIO import fileIO
from cogs.utils import checks
from copy import deepcopy
from enum import Enum
import threading
from datetime import datetime
import time
from random import randint
import math

class EconomyError(Exception):
    pass


class OnCooldown(EconomyError):
    pass


class InvalidBid(EconomyError):
    pass


class BankError(Exception):
    pass


class AccountAlreadyExists(BankError):
    pass


class NoAccount(BankError):
    pass


class InsufficientBalance(BankError):
    pass


class NegativeValue(BankError):
    pass


class SameSenderAndReceiver(BankError):
    pass


prefix = fileIO("data/red/settings.json", "load")['PREFIXES']

VC = ["Warrior", "Knight", "Swordsman", "Magician", "Blacksmith", "Craftsman", "Swindler", "Merchant", "Cook", "Scout", "Paladin", "General"]
Combat = ["Warrior", "Knight", "Swordsman", "Magician", "Scout", "Paladin", "General"]
Merch = ["Swindler", "Merchant"]

class Guild:
    """A level up thing with image generation!"""

    def __init__(self, bot):
        self.threads = []
        self.bot = bot
        self.users = fileIO("data/guild/users.json", "load")
        self.settings = fileIO("data/guild/settings.json", "load")
        self.levels = fileIO("data/guild/levels.json", "load")
        
    def _addXP(self, server, user, amount):
        self.users[server.id][user.id]["XP"] += amount
        fileIO('data/guild/users.json', "save", self.users)

    def account_exists(self, user):
        try:
            self._get_account(user)
        except NoAccount:
            return False
        return True
        
    def has_place(self, user, place):
        server = user.server
        account = self._get_account(user)
        if self.users[server.id][user.id][place] == True:
            return True
        else:
            return False
            
    def has_craftsman(self, user):
        server = user.server
        account = self._get_account(user)
        UserList = list(self.users[server.id][user.id]["vocations"])
        if "Craftsman" in UserList:
            return True
        else:
            return False
    
    def has_blacksmith(self, user):
        server = user.server
        account = self._get_account(user)
        UserList = list(self.users[server.id][user.id]["vocations"])
        if "Blacksmith" in UserList:
            return True
        else:
            return False
    
    def has_cook(self, user):
        server = user.server
        account = self._get_account(user)
        UserList = list(self.users[server.id][user.id]["vocations"])
        if "Cook" in UserList:
            return True
        else:
            return False
            
    def add_guidance(self, user, task, target, amount, reward):  
        server = user.server
        account = self._get_account(user)
        if task not in self.users[server.id][user.id]["Guidance of Baraka"]:
            new_task = {
                "task" : task,
                "target" : target,
                "goal" : amount,
                "progress" : 0,
                "reward" : reward
            }
            self.users[server.id][user.id]["Guidance of Baraka"][task] = new_task
        self._save_bank()    
                 
    def add_item(self, user, item, amount, price):
        server = user.server
        account = self._get_account(user)
        if item in self.users[server.id][user.id]["Inventory"]:
            current = int(self.users[server.id][user.id]["Inventory"][item]["quantity"]) + amount
            self.users[server.id][user.id]["Inventory"][item]["quantity"] = current
        else:
            new_item = {
                "quantity" : amount,
                "price" : price
            }
            self.users[server.id][user.id]["Inventory"][item] = new_item
        self._save_bank()
        
    def remove_item(self, user, item, amount):
        server = user.server
        account = self._get_account(user)
        try:
            if item in self.users[server.id][user.id]["Inventory"]:
                if int(self.users[server.id][user.id]["Inventory"][item]["quantity"]) == 1 or amount == int(self.users[server.id][user.id]["Inventory"][item]["quantity"]):
                    self.users[server.id][user.id]["Inventory"].pop(item)
                else:
                    current = int(self.users[server.id][user.id]["Inventory"][item]["quantity"]) - amount
                    self.users[server.id][user.id]["Inventory"][item]["quantity"] = current
                self._save_bank() 
        except:
            pass
            
    def has_item(self, user, item):
        server = user.server
        account = self._get_account(user)
        if item in self.users[server.id][user.id]["Inventory"]:
            return True
        else:
            return False
            
    def get_price(self, user, item):
        server = user.server
        account = self._get_account(user)
        price = self.users[server.id][user.id]["Inventory"][item]["price"]
        return price
        
    def get_quantity(self, user, item):
        server = user.server
        account = self._get_account(user)
        quantity = self.users[server.id][user.id]["Inventory"][item]["quantity"]
        return quantity
            
    def bought_place(self, user, place):
        server = user.server
        self.users[server.id][user.id][place] = True
        self._save_bank()

    def withdraw_gold(self, user, amount):
        server = user.server

        if amount < 0:
            raise NegativeValue()

        account = self._get_account(user)
        if int(account["balance"]) >= amount:
            account["balance"] = int(account["balance"]) - amount
            self.users[server.id][user.id] = account
            self._save_bank()
        else:
            raise InsufficientBalance()
    
    def check_haggle(self, user):
        server = user.server
        account = self._get_account(user)
        UserList = list(self.users[server.id][user.id]["vocations"])
        if any(word in Merch for word in UserList): 
            return True
        else:
            return False
            
    def check_profit(self, user, price):
        server = user.server
        account = self._get_account(user)
        UserList = list(self.users[server.id][user.id]["vocations"])
        if "Swindler" in UserList:
            price = price * 2.2
        elif "Merchant" in UserList:
            price = price * 2
        else:
            pass
        return price
    
    def train_user(self, user):
        server = user.server
        account = self._get_account(user)
        amount = self.settings[server.id]["expamount"]
        UserList = list(self.users[server.id][user.id]["vocations"])
        if any(word in Combat for word in UserList):
            xp = math.ceil(amount * 0.2)
        else:
            xp = math.ceil(amount * 0.1)
        self._addXP(server, user, xp)
        return xp
        
    def deposit_gold(self, user, amount):
        server = user.server
        if amount < 0:
            raise NegativeValue()
        account = self._get_account(user)
        account["balance"] += amount
        self.users[server.id][user.id] = account
        self._save_bank()

    def getStat(self, user, stat):
        server = user.server
        account = self._get_account(user)
        account[stat] = amount
        return amount   
        
    def set_gold(self, user, amount):
        server = user.server
        if amount < 0:
            raise NegativeValue()
        account = self._get_account(user)
        account["balance"] = amount
        self.users[server.id][user.id] = account
        self._save_bank()
        
    def reset_health(self, user):
        server = user.server
        account = self._get_account(user)
        value = account["maxhealth"]
        account["health"] = value
        self.users[server.id][user.id] = account
        self._save_bank()

    def transfer_gold(self, sender, receiver, amount):
        server = sender.server
        if amount < 0:
            raise NegativeValue()
        if sender is receiver:
            raise SameSenderAndReceiver()
        if self.account_exists(sender) and self.account_exists(receiver):
            sender_acc = self._get_account(sender)
            if sender_acc["balance"] < amount:
                raise InsufficientBalance()
            self.withdraw_gold(sender, amount)
            self.deposit_gold(receiver, amount)
        else:
            raise NoAccount()

    def can_spend(self, user, amount):
        account = self._get_account(user)
        if int(account["balance"]) >= amount:
            return True
        else:
            return False    
            
    def health_full(self, user):
        account = self._get_account(user)
        if account["health"] == account["maxhealth"]:
            return True
        else:
            return False   
            
    def is_dead(self, user):
        account = self._get_account(user)
        if account["health"] <= 0:
            return True
        else:
            return False  

    def _save_bank(self):
        dataIO.save_json("data/guild/users.json", self.users)

    def _get_account(self, user):
        server = user.server
        try:
            return deepcopy(self.users[server.id][user.id])
        except KeyError:
            raise NoAccount()
    
    async def on_message(self, message): 
        t = threading.Thread(target = await self._handle_on_message(message))
        self.threads.append(t)
        t.start()
        
    async def _handle_on_message(self, message):
        try:
            text = message.content
            channel = message.channel
            server = message.author.server
            user = message.author
            curr_time = time.time()
            
            # creates user if doesn't exist, bots are not logged.
            await self._create_user(user, server)
            await self._create_settings(server)
            await self._add_channel(server, channel)
            await self._create_levels(server)
            
            if self.settings[server.id]["on"] == False:
                return
            if self.settings[server.id]["channels"][channel.id]["priority"] == True and self.settings[server.id]["channels"][channel.id]["on"] == True:
                return
            if user.bot:
                return

            if self.settings[server.id]["channels"][channel.id]["priority"] == True:
                SV = self.settings[server.id]["channels"][channel.id]["CD"]
                amount = self.settings[server.id]["channels"][channel.id]["expamount"]
            else:
                SV = self.settings[server.id]["CD"]
                amount = self.settings[server.id]["expamount"]
                
            if float(curr_time) - float(self.users[server.id][user.id]["chat"]) >= SV and not any(text.startswith(x) for x in prefix):
                self.users[server.id][user.id]["chat"] = time.time()
                self.users[server.id][user.id]["XP"] += amount
                await self._process_exp(message)
                await self._process_rank(message)
                fileIO('data/guild/users.json', "save", self.users)
        except:
            pass   
            
    async def _process_exp(self, message):
        channel = message.channel
        server = message.author.server
        user = message.author
        level = self.users[server.id][user.id]["level"]
        if self.users[server.id][user.id]["level"] == 100:
            return
        level = self.users[server.id][user.id]["level"]
        nextlevel = int(level) + 1
        XP_Need = self.levels[server.id][str(nextlevel)]["xp_needed"]
        if self.users[server.id][user.id]["XP"] >= XP_Need:
            
            health_increase = randint(0, 10)
            self.users[server.id][user.id]["maxhealth"] += health_increase
            self.users[server.id][user.id]["health"] = self.users[server.id][user.id]["maxhealth"]
            self.users[server.id][user.id]["level"] += 1
            
            msg = "Level UP! " + user.mention + "\n"
            msg += "```" + "Level = " + str(nextlevel) + "\n"
            
            roll = [randint(0, 100) for _ in range(6)]

            msg += "Health + " + str(health_increase) + "\n"
            if self.users[server.id][user.id]["str"] < 98:
                if roll[0] <= 50:
                    if roll[0] <= 5:
                        self.users[server.id][user.id]["str"] += 2
                        msg += "STR +2" + "\n"
                    else:
                        self.users[server.id][user.id]["str"] += 1
                        msg += "STR +1" + "\n"
                else:
                    msg += "STR +0" + "\n"
            if self.users[server.id][user.id]["mag"] < 98:        
                if roll[1] <= 50:
                    if roll[1] <= 5:
                        self.users[server.id][user.id]["mag"] += 2
                        msg += "MAG +2" + "\n"
                    else:
                        self.users[server.id][user.id]["mag"] += 1
                        msg += "MAG +1" + "\n"
                else:
                    msg += "MAG +0" + "\n"
            if self.users[server.id][user.id]["speed"] < 98:       
                if roll[3] <= 50:
                    if roll[3] <= 5:
                        self.users[server.id][user.id]["speed"] += 2
                        msg += "SPD +2" + "\n"
                    else:
                        self.users[server.id][user.id]["speed"] += 1
                        msg += "SPD +1" + "\n"
                else:
                    msg += "SPD +0" + "\n"
            if self.users[server.id][user.id]["luck"] < 98:        
                if roll[4] <= 50:
                    if roll[4] <= 5:
                        self.users[server.id][user.id]["luck"] += 2
                        msg += "LCK +2" + "\n"
                    else:
                        self.users[server.id][user.id]["luck"] += 1
                        msg += "LCK +1" + "\n"
                else:
                    msg += "LCK +0" + "\n"
            if self.users[server.id][user.id]["defence"] < 98:        
                if roll[5] <= 50:
                    if roll[5] <= 5:
                        self.users[server.id][user.id]["defence"] += 2
                        msg += "DEF +2" + "\n"
                    else:
                        self.users[server.id][user.id]["defence"] += 1
                        msg += "DEF +1" + "\n"
                else:
                    msg += "DEF +0" + "\n"
            if self.users[server.id][user.id]["res"] < 98:        
                if roll[6] <= 50:
                    if roll[6] <= 5:
                        self.users[server.id][user.id]["res"] += 2
                        msg += "M.DEF +2" + "\n" + "```"
                    else:
                        self.users[server.id][user.id]["res"] += 1
                        msg += "M.DEF +1" + "\n" + "```"
                else:
                    msg += "M.DEF +0" + "\n" + "```"
            if self.settings[server.id]["whisper"] == True:
                await self.bot.send_message(user, msg)
            else:
                await self.bot.send_message(channel, msg) 
        fileIO('data/guild/users.json', "save", self.users)

    async def _create_user(self, user, server):
        if server.id not in self.users:
            self.users[server.id] = {}
        if user.id not in self.users[server.id]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            number = randint(1,8)
            volist = [" "] * number
            i = 0
            while i < number:
                voc = random.choice(VC)
                if voc in volist:
                    pass
                else:
                    volist[i] = voc
                    i += 1
            new_account = {"name" : user.name,
                           "race" : "Human",
                           "vocations" : volist,
                           "level" : 0,
                           "health" : 100,
                           "maxhealth" : 100,
                           "XP": 0,
                           "balance" : 100,
                           "shop" : False,
                           "house" : False,
                           "Guidance of Baraka" : {},
                           "Inventory" : {},
                           "chat": 0.0,
                           "Strength" : 5,
                           "Magic" : 5,
                           "Speed" : 5,
                           "Luck" : 5,
                           "Defence" : 5,
                           "Magic Defence" : 5,
                           "created_at" : timestamp}
            self.users[server.id][user.id] = new_account
        fileIO('data/guild/users.json', "save", self.users)

    async def _create_levels(self, server):
        if server.id not in self.levels:
            self.levels[server.id] = {}
            fileIO('data/guild/levels.json', "save", self.levels)
            for i in range(1, 101):
                value = (800 * i) + ((2 - 1) * i * 700)
                new_level = {
                "xp_needed" : value
                }
                self.levels[server.id][i] = new_level   
                fileIO('data/guild/levels.json', "save", self.levels)
        fileIO('data/guild/levels.json', "save", self.levels)

    async def _create_settings(self, server):
        if server.id not in self.settings:  
            new_settings = {
                "CD": 60,
                "whisper": False,
                "expamount": 1,
                "on": True,
                "channels": {},
                "roles": {}
            }
            self.settings[server.id] = new_settings
            allRoles = server.roles
            for oneRole in allRoles:
                if oneRole.id not in self.settings[server.id]["roles"]:
                    role_setting = {
                        "Keep": True
                    }
                    self.settings[server.id]["roles"][oneRole.id] = role_setting
        fileIO('data/guild/settings.json', "save", self.settings)

    async def _add_channel(self, server, channel):
        if channel.id not in self.settings[server.id]["channels"]:
            default_c_settings = {
                "expamount": 1,
                "CD": 60,
                "on": True,
                "priority": False
                }
            self.settings[server.id]["channels"][channel.id] = default_c_settings
        fileIO('data/guild/settings.json', "save", self.settings)  
    
    @checks.admin_or_permissions(manage_server=True)
    @commands.group(pass_context=True)
    async def serverconfig(self, ctx):
        """Server Configuration Options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return
    
    @checks.admin_or_permissions(manage_server=True)
    @serverconfig.command(pass_context=True, no_pm=True)
    async def sc(self, ctx):
        """Show current server configuration"""
        server = ctx.message.server
        
        expamount = self.settings[server.id]["expamount"]
        smallcool = self.settings[server.id]["CD"]
        server = self.settings[server.id]["on"]
        
        await self.bot.say("```" + "Current Server Configuration" + "\n" +
            "-------------------------" + "\n" +
            "EXP per message: " + str(expamount) + "\n" +
            "EXP cooldown: " + str(smallcool) + " seconds." + "\n" +
            "Server Enabled: " + str(server) + "\n" + "```")
    
    @checks.admin_or_permissions(manage_server=True)
    @serverconfig.command(pass_context=True, no_pm=True)
    async def serverEXP(self, ctx, amount : int, all : str="false"):
        """Set the amount of EXP gained per message. 
        Enter True after the amount to apply this to all channel settings."""
        server = ctx.message.server
        if amount < 1:
            await self.bot.say("EXP gain cannot be set below 1")
            return
        elif amount > 1000:
            await self.bot.say("EXP gain cannot be set above 1000.")
            return
        else:
            try:
                all.lower().strip()
                if amount == "yes" or amount == "y" or amount == "true" or amount == "t" or amount == "a" or amount == "all":
                    all = True
                else:
                    all = False
                if all == True:
                    allChannels = server.get_all_channels()
                    for newChannel in allChannels:
                        await self._add_channel(server, newChannel)
                        self.settings[server.id]["channels"][newChannel.id]["expamount"] = amount
                    await self.bot.say("EXP gain has been set to " + str(amount) + " in all channel settings.")
                    fileIO('data/guild/settings.json', "save", self.settings)
                else:
                    pass
                self.settings[server.id]["expamount"] = amount
                await self.bot.say("EXP gain has been set to " + str(amount) + ".")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.")
    
    @checks.admin_or_permissions(manage_server=True)
    @serverconfig.command(pass_context=True, no_pm=True)
    async def serverCD(self, ctx, amount : int, all : str="false"):
        """Set the Cooldown per message, default to 60 seconds.
        Enter True after the amount to apply this to all channel settings."""
        server = ctx.message.server
        if server.id not in self.settings:
            await self._create_settings(server) 
        if amount < 5:
            await self.bot.say("EXP cooldown cannot be set below 5 seconds.")
            return
        else:
            try:
                all.lower().strip()
                if amount == "yes" or amount == "y" or amount == "true" or amount == "t" or amount == "a" or amount == "all":
                    all = True
                else:
                    all = False
                if all == True:
                    allChannels = server.get_all_channels()
                    for newChannel in allChannels:
                        await self._add_channel(server, newChannel)
                        self.settings[server.id]["channels"][newChannel.id]["smallcool"] = amount
                    await self.bot.say("EXP cooldown has been set to " + str(amount) + " in all channel settings.")
                    fileIO('data/guild/settings.json', "save", self.settings)
                else:
                    pass
                self.settings[server.id]["smallcool"] = amount
                await self.bot.say("EXP cooldown has been set to " + str(amount) + ".")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.")
    
    @checks.admin_or_permissions(manage_server=True)
    @serverconfig.command(pass_context=True, no_pm=True)
    async def toggle(self, ctx):
        """Toggle exp gain in the whole server (overrides channel settings)"""
        server = ctx.message.server
        if server.id not in self.settings:
            await self._create_settings(server) 
        if self.settings[server.id]["on"] == True:
            try:
                self.settings[server.id]["on"] = False
                await self.bot.say("EXP has been turned off for the server.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.") 
                return
        else:
            try:
                self.settings[server.id]["on"] = True
                await self.bot.say("EXP has been turned on for the server.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.") 
                return
         
    @checks.admin_or_permissions(manage_server=True)
    @serverconfig.command(pass_context=True, no_pm=True)
    async def whisper(self, ctx):
        """Toggle whether Level Up Message is sent in chat or private.)"""
        server = ctx.message.server
        if server.id not in self.settings:
            await self._create_settings(server)
        if "whisper" not in self.settings[server.id]:
            self.settings[server.id]["whisper"] = False
        if self.settings[server.id]["whisper"] == True:
            try:
                self.settings[server.id]["whisper"] = False
                await self.bot.say("Level UP Messages will now be sent publicly.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.") 
                return
        else:
            try:
                self.settings[server.id]["whisper"] = True
                await self.bot.say("Level UP Messages will now be sent privately.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.") 
                return

    
    
    @checks.admin_or_permissions(manage_server=True)
    @serverconfig.command(pass_context=True, no_pm=True)
    async def ranktoggle(self, ctx, value):
        """Edit rank gained at levels"""
        server = ctx.message.server
        if server.id not in self.settings:
            await self._create_settings(server) 
        SRoles = server.roles
        for SRole in SRoles:
            if value == SRole.name:
                self.settings[server.id]["roles"][SRole.id]["Keep"] = not self.settings[server.id]["roles"][SRole.id]["Keep"]
                fileIO('data/guild/levels.json', "save", self.levels)
                await self.bot.say("The role: " + str(value) + " has been set to " + str(self.settings[server.id]["roles"][SRole.id]["Keep"]))
                return
        await self.bot.say("This role does not exist.")
                
    @checks.admin_or_permissions(manage_server=True)
    @commands.group(pass_context=True)
    async def channelconfig(self, ctx):
        """Server Configuration Options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @checks.admin_or_permissions(manage_server=True)
    @channelconfig.command(pass_context=True, no_pm=True)
    async def cc(self, ctx):
        """Show current channel configuration"""
        server = ctx.message.server
        channel = ctx.message.channel
        
        expamount = self.settings[server.id]["channels"][channel.id]["expamount"]
        smallcool = self.settings[server.id]["channels"][channel.id]["CD"]
        channelEnabled = self.settings[server.id]["channels"][channel.id]["on"]
        
        await self.bot.say("```" + "Current Channel Configuration" + "\n" +
            "-------------------------" + "\n" +
            "EXP per message: " + str(expamount) + "\n" +
            "EXP cooldown: " + str(smallcool) + " seconds." + "\n" +
            "Channel Enabled: " + str(channelEnabled) + "\n" + "```")
            
    @checks.admin_or_permissions(manage_server=True)
    @channelconfig.command(pass_context=True, no_pm=True)
    async def channelEXP(self, ctx, amount : int):
        """Set the amount of EXP gained per message."""
        server = ctx.message.server
        channel = ctx.message.channel
        if server.id not in self.settings:
            await self._create_settings(server) 
        if channel.id not in self.settings[server.id]["channels"]:
            await self._add_channel(server, channel)
        if amount < 1:
            await self.bot.say("EXP gain cannot be set below 1")
            return
        elif amount > 1000:
            await self.bot.say("EXP gain cannot be set above 1000.")
            return
        else:
            try:
                self.settings[server.id]["channels"][channel.id]["expamount"] = amount
                await self.bot.say("EXP gain has been set to " + str(amount) + " in this channel.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.")
                
    @checks.admin_or_permissions(manage_server=True)
    @channelconfig.command(pass_context=True, no_pm=True)
    async def channelCD(self, ctx, amount : int):
        """Set the amount of EXP gained per message."""
        server = ctx.message.server
        channel = ctx.message.channel
        if server.id not in self.settings:
            await self._create_settings(server) 
        if channel.id not in self.settings[server.id]["channels"]:
            await self._add_channel(server, channel)
        if amount < 5:
            await self.bot.say("EXP cooldown cannot be set below 5.")
            return
        else:
            try:
                self.settings[server.id]["channels"][channel.id]["CD"] = amount
                await self.bot.say("EXP cooldown has been set to " + str(amount) + ".")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.")
    
    @checks.admin_or_permissions(manage_server=True)
    @channelconfig.command(pass_context=True, no_pm=True)
    async def cp(self, ctx, channel: discord.Channel=None):
        """Toggle exp gain for the set channel, defaults to the channel your in."""
        server = ctx.message.server
        if not channel:
            channel = ctx.message.channel
        if server.id not in self.settings:
            await self._create_settings(server) 
        if channel.id not in self.settings[server.id]["channels"]:
            await self._add_channel(server, channel)
        if self.settings[server.id]["channels"][channel.id]["priority"] == True:
            try:
                self.settings[server.id]["channels"][channel.id]["on"] = False
                await self.bot.say("Priority has been turned off for the channel.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.") 
                return
        else:
            try:
                self.settings[server.id]["channels"][channel.id]["priority"] = True
                await self.bot.say("Priority has been turned on for the channel.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.") 
                return  
    
    @checks.admin_or_permissions(manage_server=True)
    @channelconfig.command(pass_context=True, no_pm=True)
    async def togglechannel(self, ctx, channel: discord.Channel=None):
        """Toggle exp gain for the set channel, defaults to the channel your in."""
        server = ctx.message.server
        if not channel:
            channel = ctx.message.channel
        if server.id not in self.settings:
            await self._create_settings(server) 
        if channel.id not in self.settings[server.id]["channels"]:
            await self._add_channel(server, channel)
        if self.settings[server.id]["channels"][channel.id]["on"] == True:
            try:
                self.settings[server.id]["channels"][channel.id]["on"] = False
                await self.bot.say("EXP has been turned off for the channel.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.") 
                return
        else:
            try:
                self.settings[server.id]["channels"][channel.id]["on"] = True
                await self.bot.say("EXP has been turned on for the channel.")
                fileIO('data/guild/settings.json', "save", self.settings)
            except:
                await self.bot.say("Something went wrong, please contact the Bot Owner.") 
                return            

    @commands.group(pass_context=True)
    async def vocation(self, ctx):
        """Server Configuration Options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @vocation.command(pass_context=True)
    async def inventory(self, ctx):
        """Check your inventory"""
        user = ctx.message.author
        server = ctx.message.server
        noItems = len(self.users[server.id][user.id]["Inventory"].keys())
        if noItems == 0:
            await self.bot.say("Goshujinsama, you have nothing in your inventory.") 
            return
        embed = discord.Embed(colour=0xD8661A)
        embed.title = "Inventory"
        for item in self.users[server.id][user.id]["Inventory"]:
            values = "Quantity: " + str(self.users[server.id][user.id]["Inventory"][item]["quantity"]) + "\n"
            values += "Value: " + str(self.users[server.id][user.id]["Inventory"][item]["price"])
            embed.add_field(name=item, value=values)
        await self.bot.say(embed=embed)
     
    @vocation.command(pass_context=True)
    async def trade(self, ctx, user : discord.Member, sum : int):
        """Transfer El to other users"""
        author = ctx.message.author
        try:
            self.transfer_gold(author, user, sum)
            logger.info("{}({}) transferred {} El to {}({})".format(
                author.name, author.id, sum, user.name, user.id))
            await self.bot.say("{} El have been transferred to {}'s account.".format(sum, user.name))
        except NegativeValue:
            await self.bot.say("You need to transfer at least 1 El.")
        except SameSenderAndReceiver:
            await self.bot.say("You can't transfer El to yourself.")
        except InsufficientBalance:
            await self.bot.say("You don't have that sum in your bank account.")
        except NoAccount:
            await self.bot.say("That user has no bank account.")            
            
    @vocation.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def addXP(self, ctx, member : discord.Member, amount : int):
        """addXP <User> <Amount>"""
        server = ctx.message.server
        if amount > 0:
            self.users[server.id][member.id]["XP"] += amount
            xp = self.users[server.id][member.id]["XP"]
            await self.bot.say(member.name + " now has " + str(xp) + " XP.")
            fileIO('data/guild/users.json', "save", self.users)
        else:
            return 
                                    
    @vocation.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def removeXP(self, ctx, member : discord.Member, amount : int):
        """removeXP <User> <Amount>"""
        server = ctx.message.server
        await self._create_user(member, server)
        if amount > 0:
            self.users[server.id][member.id]["XP"] -= amount
            xp = self.users[server.id][member.id]["XP"]
            await self.bot.say(member.name + " now has " + str(xp) + " XP.")
            fileIO('data/guild/users.json', "save", self.users)
        else:
            return
            
    @vocation.command(pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def setXP(self, ctx, member : discord.Member, amount : int):
        """setXP <User> <Amount>"""
        server = ctx.message.server
        await self._create_user(member, server)
        if amount > 0:
            self.users[server.id][member.id]["XP"] = amount
            xp = self.users[server.id][member.id]["XP"]
            await self.bot.say(member.name + " now has " + str(xp) + " XP.")
            fileIO('data/guild/users.json', "save", self.users)
        else:
            return        
    
    @vocation.command(pass_context=True, no_pm=True)
    async def blessing(self, ctx):
        """Register your user with Diana"""
        user = ctx.message.author
        server = ctx.message.server
        if user.id in self.users[server.id]:
            await self.bot.say("You have already been blessed.")
            return
        try:
            self._create_user(user, server)
            balance = self.users[server.id][user.id]["balance"]
            await self.bot.say("{} You have been blessed and given {} El for your efforts.".format(user.mention, str(balance)))
        except:
            pass
    
    @vocation.command(pass_context=True, no_pm=True)
    async def board(self, ctx, user : discord.Member=None):
        """See your or another persons Vocation Board (defaults to you)"""
        server = ctx.message.server

        if not user:
            user = ctx.message.author
        else:
            pass

        await self._create_user(user, server)
        await self._create_user(user, server)
        
        vocations = ', '.join(self.users[server.id][user.id]["vocations"])
        
        stra = str(self.users[server.id][user.id]["Strength"])
        mag = str(self.users[server.id][user.id]["Magic"])
        speed = str(self.users[server.id][user.id]["Speed"])
        luck = str(self.users[server.id][user.id]["Luck"])
        defence = str(self.users[server.id][user.id]["Defence"])
        resis = str(self.users[server.id][user.id]["Magic Defence"])
        
        embed = discord.Embed(colour=0xD8661A)
        embed.title = self.users[server.id][user.id]["name"]
        embed.add_field(name="Race", value=self.users[server.id][user.id]["race"])
        embed.add_field(name="Balace", value=str(self.users[server.id][user.id]["balance"]))
        embed.add_field(name="Vocations", value=self.users[server.id][user.id]["vocations"])
        embed.add_field(name="Level", value=str(self.users[server.id][user.id]["level"]))
        embed.add_field(name="XP", value=str(self.users[server.id][user.id]["XP"]))
        embed.add_field(name="Health", value=str(self.users[server.id][user.id]["health"]))
        embed.add_field(name="STR", value=stra)
        embed.add_field(name="MAG", value=mag)
        embed.add_field(name="SPD", value=speed)
        embed.add_field(name="LCK", value=luck)
        embed.add_field(name="DEF", value=defence)
        embed.add_field(name="M.DEF", value=resis)
        embed.add_field(name="Guidance of Baraka", value="Coming Soon...")
        
        await self.bot.say(user.mention + " - **Vocation Board** ")
        await self.bot.say(embed=embed)

    @vocation.command(name="set", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def set(self, ctx, user : discord.Member, stat, value):
        """Sets stats of user's guild account

        Admin/owner restricted."""
        server = ctx.message.server
        await self._create_user(user, server)
        if stat not in self.users[server.id][user.id]:
            await self.bot.say("This stat does not exist.")
            return
        self.users[server.id][user.id][stat] = value
        await self.bot.say(user.mention + "'s " + stat + " has been set to " + str(value))
  
    @checks.admin_or_permissions(manage_server=True)
    @commands.group(pass_context=True)
    async def levelconfig(self, ctx):
        """Server Configuration Options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return
            
    @checks.admin_or_permissions(manage_server=True)
    @levelconfig.command(pass_context=True, no_pm=True)
    async def resetlevels(self, ctx):
        """Reset all Levels for the Server"""
        server = ctx.message.server
        message = ctx.message
        chn = ctx.message.channel
        await self._create_levels(server)
        await self.bot.say("Choose a level style.")
        await self.bot.say("1 - Fire Emblem Style (100xp per Level)" + "\n" +
        "2 - Runescape Style (Coming Soon)" + "\n" +
        "3 - Custom Style (Coming Soon)" + "\n" +
        "Type exit to quit")
        while True:
            msg = await self.bot.wait_for_message(author=message.author, channel=chn)
            if msg is not None:
                if msg.content == "exit":
                    return
                elif msg.content == "1":
                    for i in range(100):
                        j = i + 1
                        value = j * 100
                        self.levels[server.id][str(j)]["xp_needed"] = value  
                        fileIO('data/guild/levels.json', "save", self.levels)
                    await self.bot.say("Done.")
                    return
                elif msg.content == "2":
                    try:
                        for i in range(100):
                            j = i + 1
                            value = j + 300 * math.pow(2, float(j)/7)
                            #value = math.floor(j + 300 * (2 ** (j / 7.0)))
                            self.levels[server.id][str(j)]["xp_needed"] = value
                        fileIO('data/guild/levels.json', "save", self.levels)
                        await self.bot.say("Done.")
                        return
                    except:
                        await self.bot.say("Something went wrong.")
                        return
                elif msg.content == "3":
                    return
                else:
                    await self.bot.say("Invalid choice." + "\n" +
                    "Use: 1, 2, 3 or exit.")
            else: 
                return
               
    @checks.admin_or_permissions(manage_server=True)
    @levelconfig.command(pass_context=True, no_pm=True)
    async def xp(self, ctx, level : int, value : int):
        """Edit xp needed for level"""
        server = ctx.message.server
        await self._create_levels(server)
        if level < 0 or level > 101:
            await self.bot.say("Level must be between 1 and 100")
            return
        XPneed = str(value)
        Ln = str(level)
        nextLevel = level + 1
        prevlevel = level - 1
        if value < 1:
            await self.bot.say("XP cannot be less than 1")
            return   
        if level == 1:
            if value < self.levels[server.id][str(nextLevel)]['xp_needed']:
                self.levels[server.id][str(level)]['xp_needed'] = value
                fileIO('data/guild/levels.json', "save", self.levels)
                await self.bot.say("XP set to " + XPneed + " for level " + Ln)
            else:
                value = self.levels[server.id][str(nextLevel)]['xp_needed']
                await self.bot.say("XP Needed for this level must be more than " + str(value))
        else:
            if value >= self.levels[server.id][str(nextLevel)]['xp_needed']:
                await self.bot.say("XP Needed for this level must be less than " + str(self.levels[server.id][nextLevel]['xp_needed']))
                return
            elif value <= self.levels[server.id][str(prevlevel)]['xp_needed']:
                await self.bot.say("XP Needed for this level must be more than " + str(self.levels[server.id][prevlevel]['xp_needed']))
                return
            else:    
                self.levels[server.id][str(level)]['xp_needed'] = value
                fileIO('data/guild/levels.json', "save", self.levels)
                await self.bot.say("XP set to " + XPneed + " for level " + Ln)
   
    @checks.admin_or_permissions(manage_server=True)
    @levelconfig.command(pass_context=True, no_pm=True)
    async def getlevel(self, ctx, level : int):
        """Create Levels for the Server to use"""
        server = ctx.message.server
        await self._create_levels(server)
        if level < 0:
            await self.bot.say("Number cannot be negative.")
        elif level > 100:
            await self.bot.say("Number must be below 101.")
        else:
            XPneed = self.levels[server.id][str(level)]['xp_needed']
            
            await self.bot.say("```" + "Level Info" + "\n" +
            "-------------------------" + "\n" +
            "Level Number: " + str(level) + "\n" +
            "XP Needed: " + str(XPneed) + "\n" + "```")  
    
def check_folders():
    if not os.path.exists("data/guild"):
        print("Creating data/guild folder...")
        os.makedirs("data/guild")  

def check_files():
    f = "data/guild/users.json"
    if not fileIO(f, "check"):
        print("Creating users.json...")
        fileIO(f, "save", {})      
      
    f = "data/guild/settings.json"
    if not fileIO(f, "check"):
        print("Creating settings.json...")
        fileIO(f, "save", {})  
        
    f = "data/guild/levels.json"
    if not fileIO(f, "check"):
        print("Creating levels.json...")
        fileIO(f, "save", {})  
            
def setup(bot):
    check_folders()
    check_files()

    n = Guild(bot)
    bot.add_listener(n.on_message,"on_message")
    bot.add_cog(n)       