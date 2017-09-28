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

default_settings = {"PAYDAY_TIME": 86164, "SLOT_MIN": 5, "SLOT_MAX": 100, "SLOT_TIME": 0, "REGISTER_CREDITS": 0}

Japan_Items = ["5-Ingredients-0", "3-Yarns-200", "3-Bundle of Papers-1000", "5-Gloves-50", "10-Bamboo Copter-1", "5-Hair Spray-50", "3-Porcelain Plate Set-500", "5-Pen and Ink set-100", "2-Sake-500", "5-Materials-0"]
Food = ["Wild Boar Steak-100", "Guillaume skewers-100", "Paella-150", "Deep-fried Hunter-Style Witchetty with sauce-500", "Unagi Don-400", "Miso Soup-150", "Curry Udon-200"]
Weapon = ["Great Sword-1500", "Claymore-1500", "Bastard Sword-1500", "Short Sword-1000", "Knife-1000", "Long Sword-1200"]

Forest = ["Wild Boar", "Undead", "Orc"]
Plains = ["12-legged Tarantula", "Troll", "Beastman", "Wolf"]
Ruins = ["Armoured Guardian Knight", "Anient Beast"]


class Quest1:
    """A level up thing with image generation!"""

    def __init__(self, bot):
        global default_settings
        self.bot = bot
        self.file_path = "data/guild1/settings.json"
        #self.file_path2 = "data/guild1/enemy.json"
        #self.enemy = dataIO.load_json(self.file_path2)
        self.settings = dataIO.load_json(self.file_path)
        self.settings = defaultdict(lambda: default_settings, self.settings)
        if "PAYDAY_TIME" in self.settings:  # old format
            default_settings = self.settings
            self.settings = {}
        self.payday_register = defaultdict(dict)
        
    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False    
    
    def randomSinglePurchase(self):
        reply = {}
        reply['1'] = "I’ll take one"
        reply['2'] = "Hmm…I guess I’ll buy one to try."
        reply['3'] = "I’ll get one for my wife then."
        return random.choice([reply[i] for i in reply])
        
    def randomAllPurchase(self, value):
        reply = {}
        reply['1'] = "Seriously!? I’ll buy them all. "
        reply['2'] = "{}!? Would it be alright selling them so cheap? I'll take all you have!".format(value)
        reply['3'] = "You’re not cheating me, aren’t you?! You’re selling them for that price?! I’ll get them all."
        return random.choice([reply[i] for i in reply])

    def randomHagglePurchase(self):
        reply = {}
        reply['1'] = "That’s quite pricey, isn’t it? Can’t you lower it?"
        reply['2'] = "It's quite high...Can't you give me a discount?"
        reply['3'] = "I really want it…but the price…."
        return random.choice([reply[i] for i in reply])
        
    def randomNoPurchase(self):
        reply = {}
        reply['1'] = "Nah, think I’ll pass."
        reply['2'] = "What a rip-off!"
        reply['3'] = "Sorry, changed my mind."
        reply['4'] = "I’ll pass then."
        return random.choice([reply[i] for i in reply])    
    
    def display_time(self, seconds, granularity=2):
        intervals = (  # Source: http://stackoverflow.com/a/24542445
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
    
    @commands.command(pass_context=True, no_pm=True)
    async def payday(self, ctx):  # TODO
        """Get some free El"""
        author = ctx.message.author
        server = author.server
        id = author.id
        guild = self.bot.get_cog("Guild")
        if guild.account_exists(author):
            roll1 = 1
            roll2 = randint(2, 10)
            amount = (roll1 * 100) + (roll2 * 10)
            if id in self.payday_register[server.id]:
                seconds = abs(self.payday_register[server.id][
                              id] - int(time.perf_counter()))
                if seconds >= self.settings[server.id]["PAYDAY_TIME"]:
                    guild.deposit_gold(author, amount)
                    self.payday_register[server.id][
                        id] = int(time.perf_counter())
                    msg = author.mention + " As expected of Goshujinsama, you found {} Silver Coin and {} White Copper coins for a total of {} El".format(str(roll1), str(roll2), str(amount))
                    await self.bot.say(msg)
                else:
                    dtime = self.display_time(
                        self.settings[server.id]["PAYDAY_TIME"] - seconds)
                    await self.bot.say(
                        "{} Too soon. For your next payday you have to"
                        " wait {}.".format(author.mention, dtime))
            else:
                self.payday_register[server.id][id] = int(time.perf_counter())
                guild.deposit_gold(author, amount)
                msg = author.mention + " As expected of Goshujinsama, you found {} Silver Coin and {} White Copper coins for a total of {} El".format(str(roll1), str(roll2), str(amount))
                await self.bot.say(msg)
        else:
            await self.bot.say("You have not been blessed yet Goshujinsama, therefore you need to do ``Diana vocation blessing`` first.")

    @commands.command(pass_context=True)
    async def inn(self, ctx):
        """Heal at an Inn, costs 200 El"""
        server = ctx.message.server
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        if guild.account_exists(user) == False:
            await self.bot.say("You have not been blessed yet Goshujinsama, therefore you need to do ``Diana vocation blessing`` first.")
            return
        if guild.can_spend(user, 200):
            if not guild.health_full(user):
                guild.withdraw_gold(user, 200)
                guild.reset_health(user)
                # check for house / 24 hour cooldown
                await self.bot.say(user.mention + ' - You have Full Health!')
            else:
                await self.bot.say('Goshujinsama, you can only use an Inn when you have full health....unless you plan on doing....*that*.....I guess Goshujinsama is really like that after all.')
        else:
            await self.bot.say('Goshujinsama, you don\'t have enough El to do that....hohoho!')
    
    @commands.command(pass_context=True)
    async def cook(self, ctx):
        """Cook Food!"""
        server = ctx.message.server
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        if guild.has_item(user, "Ingredients"):
            quantity = guild.get_quantity(user, "Ingredients")
            if quantity >= 2:
                guild.remove_item(user, "Ingredients", 2)
                FoodItem = random.choice(Food)
                name = FoodItem.rsplit('-', 1)[0]
                price = FoodItem.rsplit('-', 1)[1] 
                if guild.has_cook(user):
                    msg = "As expected of Goshujinsama, you have made a fine " + name + "."
                    guild.add_item(user, name, 1, int(price))
                    await self.bot.say(msg)
                    if "27" in self.users[server.id][author.id]["Guidance of Baraka"]:
                        self.users[server.id][author.id]["Guidance of Baraka"]["27"]["complete"] = True
                    else:
                        new_guidance = {
                            "text" : "Cook any food successfully",
                            "complete" : True
                            }
                        self.users[server.id][author.id]["Guidance of Baraka"]["27"] = new_guidance
                        fileIO('data/guild/users.json', "save", self.users)
                    return
                elif randint(0,100) < 60:
                    msg = "Oh you did it Goshujinsama! That " + name + " looks really tasty...."
                    guild.add_item(user, name, 1, int(price))
                    await self.bot.say(msg)
                    if "27" in self.users[server.id][author.id]["Guidance of Baraka"]:
                        self.users[server.id][author.id]["Guidance of Baraka"]["27"]["complete"] = True
                    else:
                        new_guidance = {
                            "text" : "Cook any food successfully",
                            "complete" : True
                            }
                        self.users[server.id][author.id]["Guidance of Baraka"]["27"] = new_guidance
                        fileIO('data/guild/users.json', "save", self.users)
                    return
                else:
                    msg = "Oh.....um, at least you tried. I'm not sure how you failed to make " + name + " but try harder next time."
                    await self.bot.say(msg)
                    return
            else:
                await self.bot.say("Goshujinsama, you need at least 2 ingredients to cook.")
                return
        await self.bot.say("Goshujinsama, you cannot cook with no ingredients.")
        return
        
    @commands.command(pass_context=True)
    async def forge(self, ctx):
        """Forge Weapons!
        
        Warning: Upon failure in creating a weapon, the user will not receive the materials back!"""
        server = ctx.message.server
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        if guild.has_item(user, "Materials"):
            quantity = guild.get_quantity(user, "Materials")
            if quantity >= 5:
                guild.remove_item(user, "Materials", 5)
                WeaponsItem = random.choice(Weapon)
                name = WeaponsItem.rsplit('-', 1)[0]
                price = WeaponsItem.rsplit('-', 1)[1] 
                if guild.has_blacksmith(user):
                    msg = "As expected of Goshujinsama, you have made a fine " + name + "."
                    guild.add_item(user, name, 1, int(price))
                    await self.bot.say(msg)
                    return
                elif randint(0,100) < 40:
                    msg = "Oh you did it Goshujinsama! That " + name + " looks really powerful...."
                    guild.add_item(user, name, 1, int(price))
                    await self.bot.say(msg)
                    return
                else:
                    msg = "Oh.....um, at least you tried. I'm not sure how you failed to make that " + name + " but try harder next time."
                    await self.bot.say(msg)
                    return
            else:
                await self.bot.say("Goshujinsama, you need at least 5 materials to forge.")
                return
        await self.bot.say("Goshujinsama, you cannot forge weapons with no materials.")
        return
        
    @commands.command(pass_context=True)
    async def craft(self, ctx, recipe:int=None):
        """Recipes:
        
        1  -  3 x Black Crystals
        2  -  1 x Magic Stone
        3  -  1 x Amethyst Stone
        4  -  1 x Garnet Stone
        5  -  1 x Sapphire Stone

        Warning: : Upon failure in creating the item, user will not receive the materials back!"""
        server = ctx.message.server
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        if recipe == 1:
            if guild.has_item(user, "Black Crystals"):
                quantity = guild.get_quantity(user, "Black Crystals")
                if quantity >= 3:
                    guild.remove_item(user, "Black Crystals", 3)
                    if guild.has_craftsman(user) == False:
                        chance = randint(0,100)
                        if chance < 60:
                            await self.bot.say("Goshujinsama, I'm afraid you failed to make anything useful.")
                            return
                    item = {}
                    item['1'] = 'Gold Ring-2000'
                    item['2'] = 'Gold Necklace-2500'
                    item['3'] = 'Silver Ring-1000'
                    item['4'] = 'Silver Necklace-1500'
                    theItem = random.choice([item[i] for i in item])
                    name = WeaponsItem.rsplit('-', 1)[0]
                    price = WeaponsItem.rsplit('-', 1)[1] 
                    guild.add_item(user, name, 1, int(price))
                    msg = "As expected of Goshujinsama, you have crafted a fine " + name + "."
                    await self.bot.say(msg)
                    return
                else:
                    await self.bot.say("Goshujinsama, you don't have enough Black Crystals, you need at least 3 of them.")
                    return
            await self.bot.say("Goshujinsama, you don't have any Black Crystals, you do realise you need actual materials to make something?")
            return
        elif recipe == 2:
            if guild.has_item(user, "Magic Stone"):
                quantity = guild.get_quantity(user, "Magic Stone")
                if quantity >= 1:
                    guild.remove_item(user, "Magic Stone", 1)
                    if guild.has_craftsman(user) == False:
                        chance = randint(0,100)
                        if chance < 60:
                            await self.bot.say("Goshujinsama, I'm afraid you failed to make anything useful.")
                            return
                    item = {}
                    item['1'] = 'Magic Ring-30000'
                    item['2'] = 'Magic Necklace-35000'
                    theItem = random.choice([item[i] for i in item])
                    name = WeaponsItem.rsplit('-', 1)[0]
                    price = WeaponsItem.rsplit('-', 1)[1] 
                    guild.add_item(user, name, 1, int(price))
                    msg = "As expected of Goshujinsama, you have crafted a fine " + name + "."
                    await self.bot.say(msg)
                    return
                else:
                    await self.bot.say("Goshujinsama, you don't have enough Magic Stones, you need at least 1 of them.")
                    return
            await self.bot.say("Goshujinsama, you don't have any Magic Stones, you do realise you need actual materials to make something?")
            return
        elif recipe == 3:
            if guild.has_item(user, "Amethyst Stone"):
                quantity = guild.get_quantity(user, "Amethyst Stone")
                if quantity >= 1:
                    guild.remove_item(user, "Amethyst Stone", 1)
                    if guild.has_craftsman(user) == False:
                        chance = randint(0,100)
                        if chance < 60:
                            await self.bot.say("Goshujinsama, I'm afraid you failed to make anything useful.")
                            return
                    item = {}
                    item['1'] = 'Amethyst Ring-30000'
                    item['2'] = 'Amethyst Necklace-35000'
                    theItem = random.choice([item[i] for i in item])
                    name = WeaponsItem.rsplit('-', 1)[0]
                    price = WeaponsItem.rsplit('-', 1)[1] 
                    guild.add_item(user, name, 1, int(price))
                    msg = "As expected of Goshujinsama, you have crafted a fine " + name + "."
                    await self.bot.say(msg)
                    return
                else:
                    await self.bot.say("Goshujinsama, you don't have enough Amethyst Stones, you need at least 1 of them.")
                    return
            await self.bot.say("Goshujinsama, you don't have any Amethyst Stones, you do realise you need actual materials to make something?")
            return
        elif recipe == 4:
            if guild.has_item(user, "Garnet Stone"):
                quantity = guild.get_quantity(user, "Garnet Stone")
                if quantity >= 1:
                    guild.remove_item(user, "Garnet Stone", 1)
                    if guild.has_craftsman(user) == False:
                        chance = randint(0,100)
                        if chance < 60:
                            await self.bot.say("Goshujinsama, I'm afraid you failed to make anything useful.")
                            return
                    item = {}
                    item['1'] = 'Garnet Ring-50000'
                    item['2'] = 'Garnet Necklace-55000'
                    theItem = random.choice([item[i] for i in item])
                    name = WeaponsItem.rsplit('-', 1)[0]
                    price = WeaponsItem.rsplit('-', 1)[1]  
                    guild.add_item(user, name, 1, int(price))
                    msg = "As expected of Goshujinsama, you have crafted a fine " + name + "."
                    await self.bot.say(msg)
                    return
                else:
                    await self.bot.say("Goshujinsama, you don't have enough Garnet Stones, you need at least 1 of them.")
                    return
            await self.bot.say("Goshujinsama, you don't have any Garnet Stones, you do realise you need actual materials to make something?")
            return
        elif recipe == 5:
            if guild.has_item(user, "Sapphire Stone"):
                quantity = guild.get_quantity(user, "Sapphire Stone")
                if quantity >= 1:
                    guild.remove_item(user, "Sapphire Stone", 1)
                    if guild.has_craftsman(user) == False:
                        chance = randint(0,100)
                        if chance < 60:
                            await self.bot.say("Goshujinsama, I'm afraid you failed to make anything useful.")
                            return
                    item = {}
                    item['1'] = 'Sapphire Ring-80000'
                    item['2'] = 'Sapphire Necklace-85000'
                    theItem = random.choice([item[i] for i in item])
                    name = WeaponsItem.rsplit('-', 1)[0]
                    price = WeaponsItem.rsplit('-', 1)[1] 
                    guild.add_item(user, name, 1, int(price))
                    msg = "As expected of Goshujinsama, you have crafted a fine " + name + "."
                    await self.bot.say(msg)
                    return
                else:
                    await self.bot.say("Goshujinsama, you don't have enough Sapphire Stones, you need at least 1 of them.")
                    return
            await self.bot.say("Goshujinsama, you don't have any Sapphire Stones, you do realise you need actual materials to make something?")
            return
        else:
            await self.bot.say("Goshujinsama, I don't think you can select that recipie. Choose a number between 1 and 5.")
            return
        
    @commands.cooldown(1, 86400, commands.BucketType.user)  
    @commands.command(pass_context=True)
    async def train(self, ctx):
        """Get XP by training"""
        server = ctx.message.server
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        if guild.account_exists(user) == False:
            await self.bot.say("You have not been blessed yet Goshujinsama, therefore you need to do ``Diana vocation blessing`` first.")
            return
        number = guild.train_user(user)
        if randint(1,100) <= 10:
            msg = "Hmm...It seems that you've improved quite a lot today."
            number = 5
            guild._addXP(server, user, 5)
        else:
            msg = "After many agonzing hours of Shello-san's training, you felt that you've grown slightly stronger. Hopefully you have enough energy to make it to bed tonight. \n"
        msg += "+ " + str(number) + " XP"
        await self.bot.say(msg)
        
    @commands.group(pass_context=True)
    async def buy(self, ctx):
        """Buy things"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return
            
    @buy.command(pass_context=True)
    async def shop(self, ctx):
        """Buy a Shop"""
        server = ctx.message.server
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        if guild.account_exists(user) == False:
            await self.bot.say("You have not been blessed yet Goshujinsama, therefore you need to do ``Diana vocation blessing`` first.")
            return
        if guild.can_spend(user, 500000):
            if guild.has_place(user, "shop"):
                await self.bot.say("You already own a shop Goshujinsama, you cannot buy another one at this moment in time.")
                return
            else:
                guild.bought_place(user, "shop")
                guild.withdraw_gold(user, 500000)
                await self.bot.say("Brilliant purchase Goshujinsama, I hope business goes well for you.")
                if "30" in self.users[server.id][author.id]["Guidance of Baraka"]:
                    self.users[server.id][author.id]["Guidance of Baraka"]["30"]["complete"] = True
                else:
                    new_guidance = {
                        "text" : "Own a Shop",
                        "complete" : True
                        }
                    self.users[server.id][author.id]["Guidance of Baraka"]["30"] = new_guidance
                    fileIO('data/guild/users.json', "save", self.users)
        else:
            await self.bot.say("You cannot afford a shop right now Goshujinsama. You may need at least 500,000 El.")
            
    @buy.command(pass_context=True)
    async def house(self, ctx):
        """Buy a home"""
        server = ctx.message.server
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        if guild.account_exists(user) == False:
            await self.bot.say("You have not been blessed yet Goshujinsama, therefore you need to do ``Diana vocation blessing`` first.")
            return
        if guild.can_spend(user, 1000000):
            if guild.has_place(user, "house"):
                await self.bot.say("You already own a home Goshujinsama, you cannot buy another one at this moment in time.")
                return
            else:
                guild.bought_place(user, "house")
                guild.withdraw_gold(user, 1000000)
                await self.bot.say("Congratulations on your purchase Goshujinsama, you've bought a wonderful new home.")
                if "29" in self.users[server.id][author.id]["Guidance of Baraka"]:
                    self.users[server.id][author.id]["Guidance of Baraka"]["29"]["complete"] = True
                else:
                    new_guidance = {
                        "text" : "Own a House",
                        "complete" : True
                        }
                    self.users[server.id][author.id]["Guidance of Baraka"]["29"] = new_guidance
                    fileIO('data/guild/users.json', "save", self.users)
        else:
            await self.bot.say("Goshujinsama cannot afford a house right now.....hohoho! Come back when you have 1,000,000 El.")
    
    @commands.cooldown(1, 86400, commands.BucketType.user)  
    @commands.command(pass_context=True)
    async def mirror(self, ctx):
        """Travel home to Japan"""
        server = ctx.message.server
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        if guild.account_exists(user) == False:
            await self.bot.say("Goshujinsama has not been blessed yet. You can still go home but nothing will come of it, therefore you need to do ``Diana vocation blessing`` first.")
            return
        if guild.can_spend(user, 500) == False:
            await self.bot.say("Goshujinsama, you do not have enough El to travel home....how pitiful. You'll need around 500 El if you wish to travel back to Japan.")
            return
        guild.withdraw_gold(user, 500)    
        msg = "Goshujinsama, welcome back from Japan! I see you have brought: \n"
        for i in range(3):
            item = random.choice(Japan_Items)
            name = item.rsplit('-', 2)[1]
            number = item.rsplit('-', 2)[0]
            price = item.rsplit('-', 2)[2] 
            msg += "-" + number + " " + name + "\n"
            guild.add_item(user, name, int(number), int(price))
        await self.bot.say(msg)
      
    @commands.command(pass_context=True)    
    async def sell(self, ctx, *, item):
        """Sell something and make a profit!"""
        user = ctx.message.author
        guild = self.bot.get_cog("Guild")
        server = ctx.message.server
        if guild.has_item(user, item) == False:
            await self.bot.say("Goshujinsama, you cannot sell something you do not have.")
            return
        BasePrice = guild.get_price(user, item)    
        if BasePrice == 0:
            await self.bot.say("Goshujinsama, you cannot sell that item.")
            return
        change = randint(0,100)
        if guild.check_haggle(user):
            if change < 80:
                HagglePrice = BasePrice * 1.5
            else:
                HagglePrice = BasePrice * 0.8
        else:
            if change < 50:
                HagglePrice = BasePrice * 1.3
            else:
                HagglePrice = BasePrice * 0.8

        await self.bot.say("Goshujinsama, the customer is asking how much the " + item + " costs. What shall I tell them?")
        msg = "1 - Sell at Base Price for: " + str(BasePrice) + "\n"
        msg += "2 - Haggle for: " + str(HagglePrice) + "\n"
        msg += "3 - exit \n"
        await self.bot.say(msg)
        while True:
            msg = await self.bot.wait_for_message(channel=ctx.message.channel, author=user)
            if msg.content == "1" and randint(0,100) < 80:
                currentPrice = BasePrice
                while True:
                    haggle = randint(0,100)
                    cs = currentPrice / BasePrice
                    if haggle * cs > 90:
                        #No Sale
                        await self.bot.say("Goshujinsama, the customer replied: " + self.randomNoPurchase())
                        await self.bot.say("They left.")
                        return
                    elif haggle * cs < 60:
                        #customer buy
                        await self.bot.say("Goshujinsama, the customer replied: " + self.randomSinglePurchase())
                        guild.remove_item(user, item, 1)
                        profit = int(guild.check_profit(user, BasePrice))
                        guild.deposit_gold(user, profit)
                        await self.bot.say("Goshujinsama, you made " + str(profit) + " El in this sale.")
                        return
                    else:
                        #customer haggle
                        msg = "Goshujinsama, the customer replied: " + self.randomHagglePurchase() + "\n" + "Please enter a new price (type ``exit`` to quit.):"
                        await self.bot.say(msg)
                        while True:
                            msg = await self.bot.wait_for_message(channel=ctx.message.channel, author=user)
                            if msg.content.lower() == "exit":
                                await self.bot.say("Goshujinsama, the customer has now left.")
                                return
                            elif self.is_number(msg.content):
                                changePrice = int(msg.content)
                                cs = changePrice / currentPrice * 100
                                currentPrice = changePrice
                                break  
                            else:
                                await self.bot.say("Goshujinsama, I require a numerical response between 1 and 3.")       
            elif msg.content == "2":
                currentPrice = HagglePrice
                if HagglePrice < BasePrice:
                    #garunteed sell all
                    await self.bot.say("Goshujinsama, the customer replied: " + self.randomAllPurchase(currentPrice))
                    quantity = guild.get_quantity(user, item)
                    guild.remove_item(user, item, quantity)
                    price = HagglePrice * quantity
                    profit = int(guild.check_profit(user, price))
                    guild.deposit_gold(user, profit)
                    await self.bot.say("Goshujinsama, you made " + str(profit) + " El in this sale.")
                    return
                else:
                    while True:
                        haggle = randint(0,100)
                        cs = currentPrice / BasePrice
                        if haggle * cs > 90:
                            #No Sale
                            await self.bot.say("Goshujinsama, the customer replied: " + self.randomNoPurchase())
                            await self.bot.say("They left.")
                            return
                        elif haggle * cs < 55:
                            #customer buy
                            await self.bot.say("Goshujinsama, the customer replied: " + self.randomSinglePurchase())
                            guild.remove_item(user, item, 1)
                            profit = int(guild.check_profit(user, currentPrice))
                            guild.deposit_gold(user, profit)
                            await self.bot.say("Goshujinsama, you made " + str(profit) + " El in this sale.")
                            return
                        else:
                            #customer haggle
                            msg = "Goshujinsama, the customer replied: " + self.randomHagglePurchase() + "\n" + "Please enter a new price (type ``exit`` to quit.):"
                            await self.bot.say(msg)
                            while True:
                                msg = await self.bot.wait_for_message(channel=ctx.message.channel, author=user)
                                if msg.content.lower() == "exit":
                                    await self.bot.say("Goshujinsama, the customer has now left.")
                                    return
                                elif self.is_number(msg.content):
                                    changePrice = int(msg.content)
                                    cs = changePrice / currentPrice * 100
                                    currentPrice = changePrice
                                    break  
                                else:
                                    await self.bot.say("Goshujinsama, I require a numerical response between 1 and 3.")
            elif msg.content == "3":
                await self.bot.say("Goshujinsama, the customer left.")
                return
            else:
                await self.bot.say("Goshujinsama, I require a numerical response between 1 and 3.")
                    
    @mirror.error
    async def mirror_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            await self.bot.say(error)   

    @train.error
    async def train_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            await self.bot.say(error)   
        
 
def check_folders():
    if not os.path.exists("data/guild1"):
        print("Creating data/guild1 folder...")
        os.makedirs("data/guild1")


def check_files():

    f = "data/guild1/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default guild1's settings.json...")
        dataIO.save_json(f, {})

      
def setup(bot):
    check_folders()
    check_files()
    n = Quest1(bot)
    bot.add_cog(n)