import discord
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
from cogs.utils import checks
import os, re, aiohttp
from .utils.dataIO import fileIO
from cogs.utils.dataIO import dataIO
from datetime import datetime
import time, asyncio
from bittrex.bittrex import Bittrex, API_V2_0, API_V1_1

#Stoch RSI is 0.20 or less for oversold goods
#Stoch RSI is 0.80 or more for overbought goods

KEY1 = ""
KEY2 = ""

BTCFormats = ["XBT", "BTC", "BITCOIN", "BIT", "SATOSHI"]
USDFormats = ["USD", "DOLLARS", "US DOLLARS", "USDT"]

class Cryptocoin:
    """Displays info related to crpyto from bitrex."""
    
    def __init__(self, bot):
        self.bot = bot
        self.my_bittrex = Bittrex("e8488011676540198d8dccdf16c2b5c2", "2493a0961e1c41dd9da01e1212e8ea99", api_version=API_V2_0)
        self.settings = fileIO("data/cryptocoin/settings.json", "load")
        self.data15min = fileIO("data/cryptocoin/data15min.json", "load")
        self.data30min = fileIO("data/cryptocoin/data30min.json", "load")
        self.data1hour = fileIO("data/cryptocoin/data1hour.json", "load")
        self.data4hour = fileIO("data/cryptocoin/data4hour.json", "load")
        self.data12hour = fileIO("data/cryptocoin/data12hour.json", "load")
        self.data1day = fileIO("data/cryptocoin/data1day.json", "load")
    
    async def storingData(self):
        while True:
            self.data15min["updated"] -= 900
            self.data30min["updated"] -= 900
            self.data1hour["updated"] -= 900
            self.data4hour["updated"] -= 900
            self.data12hour["updated"] -= 900
            self.data1day["updated"] -= 900
            self.my_bittrex.get_markets()
            value = self.my_bittrex.get_market_summaries()
            if self.data15min["updated"] <= 0:
                tTime = datetime.now().strftime ("%Y%m%d%H%M")
                await self.storeData(value, self.data15min, tTime)
                self.data15min["updated"] += 900 
                fileIO('data/cryptocoin/data15min.json', "save", self.data15min)
            if self.data30min["updated"] <= 0:
                tTime = datetime.now().strftime ("%Y%m%d%H%M")
                await self.storeData(value, self.data30min, tTime)
                self.data30min["updated"] += 1800 
                fileIO('data/cryptocoin/data30min.json', "save", self.data30min)
            if self.data1hour["updated"] <= 0:
                tTime = datetime.now().strftime ("%Y%m%d%H")
                await self.storeData(value, self.data1hour, tTime)
                self.data1hour["updated"] += 3600 
                fileIO('data/cryptocoin/data1hour.json', "save", self.data1hour)
            if self.data4hour["updated"] <= 0:
                tTime = datetime.now().strftime ("%Y%m%d%H")
                await self.storeData(value, self.data4hour, tTime)
                self.data4hour["updated"] += 14400 
                fileIO('data/cryptocoin/data4hour.json', "save", self.data4hour)
            if self.data12hour["updated"] <= 0:
                tTime = datetime.now().strftime ("%Y%m%d%H")
                await self.storeData(value, self.data12hour, tTime)
                self.data12hour["updated"] += 43200 
                fileIO('data/cryptocoin/data12hour.json', "save", self.data12hour)
            if self.data1day["updated"] <= 0:
                tTime = datetime.now().strftime ("%Y%m%d")
                await self.storeData(value, self.data1day, tTime)
                self.data1day["updated"] += 86400 
                fileIO('data/cryptocoin/data1day.json', "save", self.data1day)
            await asyncio.sleep(900)  
    
    async def storeData(self, value, file, unit):
        """Stores data collected from bittrex into a json file."""
        data = file
        coins = value["result"]
        unixtime = unit
        for coin in coins:
            name = coin["Summary"]["MarketName"]
            if name not in data:
                name = coin["Summary"]["MarketName"]
                data[name] = {}
            if unixtime not in data[name]:
                new_data = {
                    "High": float(coin["Summary"]["High"]),
                    "Low": float(coin["Summary"]["Low"]),
                    "Volume": coin["Summary"]["Volume"],
                    "BaseVolume": coin["Summary"]["BaseVolume"],
                    "Last": float(coin["Summary"]["Last"]),
                }
                data[name][unixtime] = new_data
            if len(data[name]) > 200:
                templist = data[name]
                templist = sorted(templist, key=int)
                templist = templist[:-1]
                data[name] = templist
            periods = self.settings[server.id]["Base-RSI"]    
            if len(data[name]) > periods:
                AverageGain = 
     
    def rsi_one(self, input):
        """Calculate the StochRSI of all crypto currencies for 1hr, 4hr, 12hr and 1 day."""
        value = self.data[input]
        periods = self.settings[server.id]["Base-RSI"]
        data = self.data1hour.pop("updated")
        for coins in data:
            if len(coins) < periods:
                tempPeriods = len(coins)
            else:
                tempPeriods = periods
            templist = coins
            templist = sorted(templist, key=int)
            templist = templist[:tempPeriods]
            #Average Gain 
                
        #RS = Average gain of up periods during the specified time frame
        #LLRSI = Lowest point in time frame
        LLRSI = float(value["result"]["Low"])
        HHRSI = float(value["result"]["High"])
        #RS = float(LLRSI + HHRSI) / 2)
        average = (LLRSI + HHRSI) / 2
        averageGain = (HHRSI - average) / average
        averageLoss = (average - LLRSI) / average
        RS = averageGain / averageLoss
        RSI = 100 - (100 / (1 + RS))
        #HHRSI = Highest point in time frame
        StochRSI = (RSI - LLRSI) / (HHRSI - LLRSI)
        return StochRSI
        
    @commands.command(pass_context=True, no_pm=True)
    async def resetCrypto(self, ctx, value): 
        """Resets all settings to default.
        RSI: 14
        Currency: BTC
        Oversold: 20
        Overbought: 80
        """
        sever = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
        self.settings[server.id]["Base-RSI"] = 14
        self.settings[server.id]["Base-Currency"] = "BTC"
        self.settings[server.id]["Base-Oversold"] = 20
        self.settings[server.id]["Base-Overbought"] = 80
        fileIO('data/cryptocoin/settings.json', "save", self.settings)
        await self.bot.say("All Crypto Bitrex related values set to default.")
    
    @commands.command(pass_context=True, no_pm=True)
    async def setRSI(self, ctx, value): 
        """Set the number of days that StochRSI uses for its calculations.
        Default: 14 Days
        """
        sever = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
        if value <= 1:
            await self.bot.say("Value must be more than 1.")
        elif value >= 100:
            await self.bot.say("Value must be less than 100.")
        else:
            self.settings[server.id]["Base-RSI"] = value
            await self.bot.say("RSI value set to {}.".format(value))
        fileIO('data/cryptocoin/settings.json', "save", self.settings)
    
    @commands.command(pass_context=True, no_pm=True)
    async def setCurrency(self, ctx, value): 
        """Set the base currency used in all Cryptocoin related functions.
        BTC Formats: "XBT", "BTC", "BITCOIN", "BIT", "SATOSHI"
        USD Formats: "USD", "DOLLARS", "US DOLLARS", "USDT"
        """
        sever = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
        if value.upper() in BTCFormats:
            self.settings[server.id]["Base-Currency"] = "BTC"
            await self.bot.say("Base unit set to Bitcoin.")
        elif value.upper() in USDFormats:
            self.settings[server.id]["Base-Currency"] = "USDT"
            await self.bot.say("Base unit set to US Dollars.")
        else:
            await self.bot.say("Invalid value.")
        fileIO('data/cryptocoin/settings.json', "save", self.settings)
        
    @commands.command(pass_context=True, no_pm=True)
    async def setOversold(self, ctx, value:int): 
        """Set the unit used to check when a currency is oversold.
        Must be inbetween 1 and 100.
        Example (20): Notifies user when oversold is below 20
        Default is 20.
        """
        sever = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
        if value <= 1:
            await self.bot.say("Value must be more than 1.")
        elif value >= 100:
            await self.bot.say("Value must be less than 100.")
        else:
            self.settings[server.id]["Base-Oversold"] = value
            await self.bot.say("Oversold value set to {}.".format(value))
        fileIO('data/cryptocoin/settings.json', "save", self.settings)
        
    @commands.command(pass_context=True, no_pm=True)
    async def setOverbought(self, ctx, value:int): 
        """Set the unit used to check when a currency is overbought.
        Must be inbetween 1 and 100.
        Example (80): Notifies user when overbought is above 80
        Default is 80.
        """
        sever = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
        if value <= 1:
            await self.bot.say("Value must be more than 1.")
        elif value >= 100:
            await self.bot.say("Value must be less than 100.")
        else:
            self.settings[server.id]["Base-Overbought"] = value
            await self.bot.say("Overbought value set to {}.".format(value))
        fileIO('data/cryptocoin/settings.json', "save", self.settings)
    
    @commands.command(pass_context=True, no_pm=True)
    async def testcrypt(self, ctx): 
        self.my_bittrex.get_markets()
        #currency = "BTC-" + input.upper()
        value = self.my_bittrex.get_market_summaries()
        self.temp = value
        fileIO('data/cryptocoin/temp.json', "save", self.temp)
        await self.bot.say("Done")
    
    @commands.command(pass_context=True, no_pm=True)
    async def value(self, ctx, input): 
        """Check the StochRSI for a given currency in the last 24 hours."""
        self.my_bittrex.get_markets()
        currency = "USDT-" + input.upper()
        value = self.rsi(currency)
        await self.bot.say("The current StochRSI for {} in the last 24 Hours is: {}".format(currency, value))

def check_folders():
    if not os.path.exists("data/cryptocoin"):
        print("Creating data/cryptocoin folder...")
        os.makedirs("data/cryptocoin")

def check_files():
    f = "data/cryptocoin/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default cryptocoin's settings.json...")
        dataIO.save_json(f, {})
        
    f = "data/cryptocoin/data15min.json"
    if not dataIO.is_valid_json(f):
        print("Creating default cryptocoin's data15min.json...")
        dataIO.save_json(f, {"updated": 0})
        
    f = "data/cryptocoin/data30min.json"
    if not dataIO.is_valid_json(f):
        print("Creating default cryptocoin's data30min.json...")
        dataIO.save_json(f, {"updated": 0})
        
    f = "data/cryptocoin/data1hour.json"
    if not dataIO.is_valid_json(f):
        print("Creating default cryptocoin's data1hour.json...")
        dataIO.save_json(f, {"updated": 0})
        
    f = "data/cryptocoin/data4hour.json"
    if not dataIO.is_valid_json(f):
        print("Creating default cryptocoin's data4hour.json...")
        dataIO.save_json(f, {"updated": 0}) 
        
    f = "data/cryptocoin/data12hour.json"
    if not dataIO.is_valid_json(f):
        print("Creating default cryptocoin's data12hour.json...")
        dataIO.save_json(f, {"updated": 0})
        
    f = "data/cryptocoin/data1day.json"
    if not dataIO.is_valid_json(f):
        print("Creating default cryptocoin's data1day.json...")
        dataIO.save_json(f, {"updated": 0})  
        
def setup(bot):
    check_folders()
    check_files()
    n = Cryptocoin(bot)
    bot.add_cog(n)
    bot.loop.create_task(n.storingData())