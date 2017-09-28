from discord.ext import commands
from cogs.utils import checks
from .utils.dataIO import dataIO
from __main__ import send_cmd_help, user_allowed
import os
import discord
import asyncio
import random


class Describe:
    def __init__(self, bot):
        self.bot = bot

        
    def randomEnemy(self):
        pep = {}
        pep['1'] = 'Gerudo'
        pep['2'] = 'Thief'
        pep['3'] = 'Criminal'
        pep['4'] = 'Wild Spirit'
        pep['5'] = 'Enemy Soldier'
        pep['6'] = 'Enemy Mage'
        pep['7'] = 'ReDead'
        pep['8'] = 'Gibdo'
        pep['9'] = 'Iron Knuckle'
        pep['10'] = 'Darknut'
        pep['11'] = 'Moblin'
        pep['12'] = 'Bokoblin'
        pep['13'] = 'Corrupted Bokoblin'
        pep['14'] = 'Wolfos'
        pep['15'] = 'Demon'
        pep['16'] = 'Goron'
        pep['17'] = 'Kokiri'
        pep['18'] = 'Stalfos'
        pep['20'] = 'Dead Hand'
        pepo = random.choice([pep[number] for number in pep])
        return pepo 
        
    def randomMethod(self):
        pep = {}
        pep['1'] = 'swinging your sword at it!'
        pep['2'] = 'swinging your sword at the weak spot on its back!'
        pep['3'] = 'swinging your sword at it legs!'
        pep['4'] = 'swinging your sword after it attacks!'
        pep['5'] = 'shooting it with your bow!'
        pep['6'] = 'throwing bombs into its mouth!'
        pep['7'] = 'hitting its arms with your slingshot!'
        pep['8'] = 'dodging its strikes and attacking back!'
        pep['9'] = 'using bombs!'
        pep['10'] = 'swinging your deku sticks!'
        pep['11'] = 'stunning it with Deku Nuts and attacking!'
        pep['12'] = 'cracking the weak spot on its back with your hammer!'
        pep['13'] = 'doing some cool shit!'
        pep['14'] = 'umm....I actually don\'t know....sorry!'
        pep['15'] = 'using the power of friendship!'
        pep['16'] = 'using the force!'
        pepo = random.choice([pep[number] for number in pep])
        return pepo    
        
        
    @commands.command(pass_context=True)
    async def describe(self, context, member : discord.Member=None):
        """Get Navi to describe someone!"""
        if member == None:
            member = context.message.author
        thing = self.randomEnemy()
        method = self.randomMethod()
        msg = "This " + thing + " is known as " + member.name + ".  Try beating it by " + method
        await self.bot.say(msg)
        

def setup(bot):
    n = Describe(bot)
    bot.add_cog(n)
