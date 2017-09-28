from discord.ext import commands
from .economy import NoAccount
from __main__ import send_cmd_help
from .utils import checks
from random import randint
import os
import time
import random
import asyncio
import discord

class Arena:
    """Allows up to 1 players to play Arena Games"""

    def __init__(self, bot):
        self.bot = bot

    def enough_points(self, uid, amount):
        bank = self.bot.get_cog('Economy').bank
        if bank.can_spend(uid, amount):
            return True
        else:
            return False
            
    def account_check(self, speaker):
        bank = self.bot.get_cog('Economy').bank
        if bank.account_exists(speaker):
            return True
        else:
            return False
            
    def roleCheck(self, user : discord.User):
        Roles = user.roles
        for Role in Roles[:]:
            if Role.id == "220712429636681728": #Copper
                return 2
            elif Role.id == "220712465866948610": #Iron
                return 3
            elif Role.id == "220712513484881921": #Silver
                return 4
            elif Role.id == "220712535861493760": #Gold
                return 5
            elif str(Role.id) == "220712555650351114": #Platinum
                return 6
            elif Role.id == "220712579587112960": #Mythril
                return 7
            elif Role.id == "220712606145576960": #Orichalcum
                return 8
            elif Role.id == "220712680728559616": #Adamantite
                return 9
            elif Role.id == "223488592486334465": #Hero
                return 10
            elif Role.id == "220756096086704129": #God
                return 100
            else:
                pass
        return 1 #unranked
        
    def roleNameCheck(self, Number):
        if Number == 1:
            return "Unranked"
        elif Number == 2:
            return "Copper"
        elif Number == 3:
            return "Iron"
        elif Number == 4:
            return "Silver"
        elif Number == 5:
            return "Gold"
        elif Number == 6:
            return "Platinum"
        elif Number == 7:
            return "Mythril"
        elif Number == 8: 
            return "Orichalcum"
        elif Number == 9:
            return "Adamantite"
        elif Number == 10:
            return "Hero"
        elif Number == 100:
            return "God"
        else:
            return "Unranked"
        
    def nationCheck(self, user : discord.User):
        Roles = user.roles
        for Role in Roles[:]:
            if Role.id == "220742745420070923": #TheKingdom
                return 2
            elif Role.id == "220742070246047745": #TheEmpire
                return 3
            elif Role.id == "220741512818982913": #TheTheocracy
                return 4
            else:
                pass
        return 1 #unranked
            
    def nationNameCheck(self, number):
        if number == 2: #TheKingdom
            return "The Kingdom"
        elif number == 3: #TheEmpire
            return "The Empire"
        elif number == 4: #TheTheocracy
            return "The Theocracy"
        else:
            return "The Sorcerer Kingdom"
    
    def randomStart(self, author):
        goodOutcome = {}
        goodOutcome['1'] = '{0} made the first move by dashing directly towards the opponent.'.format(author)
        goodOutcome['2'] = '{0} watched carefully and started approaching slowly.'.format(author)
        goodOutcome['3'] = '{0} tried to use random movement to throw off their opponent, heading towards them in a beeline.'.format(author)
        goodOutcome['4'] = '{0} growled in a fierce manner and charged.'.format(author)
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def randomStartResponse(self, author):
        goodOutcome = {}
        goodOutcome['1'] = '{0} held their weapon tight in preperation.'.format(author)
        goodOutcome['2'] = '{0} stepped backwards, anticipating the attack.'.format(author)
        goodOutcome['3'] = '{0} ran towards their opponent, trying to match their strategy.'.format(author)
        goodOutcome['4'] = '{0} started rocking side to side in an attempt to roll at the last moment.'.format(author)
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
    
    def randomPlace(self):
        goodOutcome = {}
        goodOutcome['1'] = 'high ground'
        goodOutcome['2'] = 'low ground'
        goodOutcome['3'] = 'side'
        goodOutcome['4'] = 'air'
        goodOutcome['5'] = 'ground'
        goodOutcome['6'] = 'wall'
        goodOutcome['7'] = 'dirt'
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def randomAttack(self):
        goodOutcome = {}
        goodOutcome['1'] = 'swing'
        goodOutcome['2'] = 'smash'
        goodOutcome['3'] = 'swipe'
        goodOutcome['4'] = 'poke'
        goodOutcome['5'] = 'stab'
        goodOutcome['6'] = 'slash'
        goodOutcome['7'] = 'jab'
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def randomDefend(self):
        goodOutcome = {}
        goodOutcome['1'] = 'block'
        goodOutcome['2'] = 'parry'
        goodOutcome['3'] = 'dodge'
        goodOutcome['4'] = 'counter'
        goodOutcome['5'] = 'deflect'
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def randomBody(self):
        goodOutcome = {}
        goodOutcome['1'] = 'head'
        goodOutcome['2'] = 'left arm'
        goodOutcome['3'] = 'right arm'
        goodOutcome['4'] = 'left leg'
        goodOutcome['5'] = 'right leg'
        goodOutcome['6'] = 'face'
        goodOutcome['7'] = 'body'
        goodOutcome['8'] = 'stomach'
        goodOutcome['9'] = 'torso'
        goodOutcome['10'] = 'back'
        goodOutcome['11'] = 'foot'
        goodOutcome['12'] = 'hand'
        goodOutcome['13'] = 'shoulder'
        goodOutcome['14'] = 'knee'
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
    
    def randomWeapon(self,):
        goodOutcome = {}
        goodOutcome['1'] = 'Sword'
        goodOutcome['2'] = 'Long Sword'
        goodOutcome['3'] = 'Knife'
        goodOutcome['4'] = 'Axe'
        goodOutcome['5'] = 'Hammer'
        goodOutcome['6'] = 'Scimitar'
        goodOutcome['7'] = 'Katana'
        goodOutcome['8'] = 'Great Sword'
        goodOutcome['9'] = 'Cleaver'
        goodOutcome['10'] = 'Brass Knuckles'
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def goodFight(self, authorOne, authorTwo, weaponOne, weaponTwo):
        place = self.randomPlace()
        attack = self.randomAttack()
        defend = self.randomDefend()
        body = self.randomBody()
        weapon = self.randomWeapon()
        outcome = {}
        outcome['1'] = authorOne + ' attacked with the ' + weaponOne + ' they carried. Trying to ' + attack + ' ' + authorTwo + ' and managing to score a hit on their ' + body + '.' 
        outcome['2'] = 'The ' + weaponOne + ' and ' + weaponTwo + ' clashed as sparks illuminated the fighters faces. But ' + authorOne + ' used the ' + place + ' to their advantage and hit ' + authorTwo + '.' 
        outcome['3'] = 'Picking up a random ' + weapon + ' off the ground, ' + authorOne + ' managed to hit ' + authorTwo + ' in the ' + body + '.' 
        outcome['4'] = authorTwo + ' got knocked back into a wall and was forced to retreat as ' + authorOne + ' used the flat part of their ' + weaponOne + ' to harm ' + authorTwo + ' in the ' + body + '.' 
        outcome['5'] = 'Using a great deal of force, ' + authorOne + ' managed to push ' + authorTwo + ' back and trip them up. Causing the ' + weaponTwo + ' they were carrying to injure them.'
        good = random.choice([outcome[i] for i in outcome])
        return good
        
    def midFight(self, authorOne, authorTwo, weaponOne, weaponTwo):
        place = self.randomPlace()
        attack = self.randomAttack()
        defend = self.randomDefend()
        body = self.randomBody()
        weapon = self.randomWeapon()
        outcome = {}
        outcome['1'] = authorOne + ' moved about carefully, considering if they could hurt ' + authorTwo + ' in the ' + body + '.' 
        outcome['2'] = 'The ' + place + ' would be a good place to fight from. At least that\'s what ' + authorOne + ' thought.'
        outcome['3'] = 'There was a ' + weapon + ' lying on the floor that ' + authorOne + ' thought of utilising.'
        outcome['4'] = authorOne + ' wondered if a ' + attack + ' hit ' + authorTwo + ' in the ' + body + ', whether it would do much damage or not.'
        outcome['5'] = 'A ' + defend + ' may be the best thing to do. ' + authorOne + ' prepared themselves in advance.'
        good = random.choice([outcome[i] for i in outcome])
        return good
        
    def badFight(self, authorOne, authorTwo, weaponOne, weaponTwo):
        place = self.randomPlace()
        attack = self.randomAttack()
        defend = self.randomDefend()
        body = self.randomBody()
        weapon = self.randomWeapon()
        outcome = {}
        outcome['1'] = 'Pushing their advantage too far, ' + authorOne + ' was shocked as the ' + weaponOne + ' they were using was easily stopped as ' + authorTwo + ' performed a ' + defend + ' and they were hurt instead.'
        outcome['2'] = 'Thinking that the ' + place + ' could have been used to hit ' + authorTwo + ', ' + authorOne + ' was suprised to find themselves hit in the ' + body + '.'  
        outcome['3'] = authorOne + ' tripped and hurt their ' + body + ', giving ' + authorTwo + ' the advantage.'  
        outcome['4'] = 'As ' + authorOne + ' and ' + authorTwo + ' clashed their weapons the ' + weaponTwo + ' that ' + authorTwo + ' was using hit ' + authorOne + ' in the ' + body + '.'  
        outcome['5'] = authorOne + ' fell backwards and hit their ' + body + ' as ' + authorTwo + ' used their ' + weaponTwo + ' to do extra damage, despite the way ' + authorOne + ' tried to ' + defend + '.' 
        out = random.choice([outcome[i] for i in outcome])
        return out
    
    @commands.cooldown(1, 300, commands.BucketType.user)  
    @commands.command(pass_context=True, no_pm=True)
    async def pvp(self, ctx, bet: int):
        """Arena PVP, requires 2 players"""
        author  = ctx.message.author
        server = ctx.message.server
        chn = ctx.message.channel
        ready = False
        if self.account_check(author):
            if bet >= 50 and bet <= 3000:
                if self.enough_points(author, bet):
                    pass
                else:
                    await self.bot.say("You do not have enough gold.")
                    return
            else:
                await self.bot.say("You need to bet more than 50 and less than 3,000 Gold.")
                return
        else:
            await self.bot.say("You cannot issue a challenge without an account first. Type '# bank register' to register with the Guild.")   
            return
        code = "pvp " + str(bet)
        await self.bot.say(author.name + " has issued a challenge with a bet of " + str(bet) + " Gold!" + "\n" +
        "To fight him enter '" + code + "' to accept the challenge!")
        endtime = time.time() + 60
        while time.time() < endtime:
            msg = await self.bot.wait_for_message(timeout=60, channel=chn)
            if msg is not None:
                if msg.content == code:
                    author2 = msg.author
                    if author != author2:
                        if self.account_check(author2):
                            if self.enough_points(author2, bet):
                                ready = True
                                break
                            else:
                                await self.bot.say("You do not have enough gold.")
                        else:
                            await self.bot.say("You cannot issue a challenge without an account first. Type '# bank register' to register with the Guild.")   
                    else:
                        await self.bot.say("You can't challenge yourself.")
                else:
                    pass
            else: 
                pass
        if ready == True:
            pass
        else:
            await self.bot.say("Apparently no one wants to challenge you " + author.mention + "!")  
            return
        bank = self.bot.get_cog('Economy').bank
        bank.withdraw_gold(author, bet)    
        bank.withdraw_gold(author2, bet)    
        await self.bot.say(author.mention + "! You have been challenged by " + author2.mention + " to a 1 on 1 battle!")
        await asyncio.sleep(3)
        await self.bot.say("The location is an arena inside The Empire!")  
        Fighter1Role = self.roleCheck(author)
        Fighter1Nation = self.nationCheck(author)
        Fighter1RoleName = self.roleNameCheck(Fighter1Role)
        Fighter1NationName = self.nationNameCheck(Fighter1Nation)
        Fighter2Role = self.roleCheck(author2)
        Fighter2Nation = self.nationCheck(author2)
        Fighter2RoleName = self.roleNameCheck(Fighter2Role)
        Fighter2NationName = self.nationNameCheck(Fighter2Nation)
        Fighter1Weapon = self.randomWeapon()
        while True:
            Fighter2Weapon = self.randomWeapon()
            if Fighter2Weapon == Fighter1Weapon:
                Fighter2Weapon = self.randomWeapon()
            else:
                break
        else:
            pass
        points1 = 0
        points2 = 0
        await asyncio.sleep(3)
        await self.bot.say("Our Champion in this battle is a " + Fighter1RoleName + " rank fighter from " + Fighter1NationName + "!")  
        await asyncio.sleep(4)
        await self.bot.say("The Challenger is a " + Fighter2RoleName + " rank fighter from " + Fighter2NationName + "!")
        await asyncio.sleep(3)
        await self.bot.say("Good luck to the both of you!")
        await asyncio.sleep(5)
        await self.bot.say(author.name + " walked in with their " + Fighter1Weapon + " looking confident.")
        await asyncio.sleep(3)
        await self.bot.say(author2.name + " came in holding their " + Fighter2Weapon + " looking equally confident.")   
        await asyncio.sleep(5)
        lst = ['...'] * 8   
        Roll1 = randint(0, 10)
        Roll2 = randint(0, 10)
        while True:
            Roll1 = randint(0, 300) + (Fighter1Role * 10)
            if Roll1 == Roll2:
                pass
            elif Roll1 > Roll2:
                #Add Player 1 start
                lst[0] = self.randomStart(author.name)
                lst[1] = self.randomStartResponse(author2.name)
                break
            elif Roll2 > Roll1:
                #Add PLayer 2 start
                lst[0] = self.randomStart(author2.name)
                lst[1] = self.randomStartResponse(author.name)
                break
            else:
                pass
        else:
            pass
        Fighter1Bonus = Fighter1Role * 100
        Fighter2Bonus = Fighter2Role * 100
        Fighter1Hit = 100 + (Fighter1Bonus / 2) - (Fighter2Bonus / 10)
        Fighter2Hit = 100 + (Fighter2Bonus / 2) - (Fighter1Bonus / 10)
        for i in range(5):
            Roll1 = randint(0, 1001)
            Roll2 = randint(0, 1001)
            if Roll1 > 0 and Roll1 < Fighter1Hit:
                #Player 1 lands a hit and Player 2 suffers.
                msg = self.goodFight(author.name, author2.name, Fighter1Weapon, Fighter2Weapon)
                points1 = points1 + 1
            elif Roll1 > Fighter1Hit and Roll1 < Fighter1Bonus:
                msg = self.midFight(author.name, author2.name, Fighter1Weapon, Fighter2Weapon)
            else:
                #bad message
                msg = self.badFight(author.name, author2.name, Fighter1Weapon, Fighter2Weapon)
                points2 = points2 + 1
            lst[i + 2] = msg
            #Next Player
            if Roll1 > 0 and Roll1 < Fighter2Hit:
                #Player 1 lands a hit and Player 2 suffers.
                msg2 = self.goodFight(author2.name, author.name, Fighter2Weapon, Fighter1Weapon)
                points2 = points2 + 1
            elif Roll1 > Fighter2Hit and Roll1 < Fighter2Bonus:
                msg2 = self.midFight(author2.name, author.name, Fighter2Weapon, Fighter1Weapon)
            else:
                #bad message
                msg2 = self.badFight(author2.name, author.name, Fighter2Weapon, Fighter1Weapon)
                points1 = points1 + 1
            lst[i + 3] = msg2
        for i in range(8):    
            await self.bot.say(lst[i])  
            await asyncio.sleep(4)
        #Tally result
        prize = bet * 2
        while True:
            if points1 > points2:
                if abs(points1-points2):
                    await self.bot.say("As the battle drew near " + author2.name + " took their final breath and collapsed.")
                    await self.bot.say("It seems like they died.")
                    if author.id == '159043902383456257':
                        await self.bot.say("As expected of Ainz-Sama!")
                        await asyncio.sleep(3)
                    elif author2.id == '159043902383456257':
                        await self.bot.say("I find it hard to understand why Ainz-Sama let you win! He even took lot's of damage right now.")
                        await asyncio.sleep(3)
                        await self.bot.say("No there must be a reason behind it....Ahh it was a lesson for you after all!")
                        await asyncio.sleep(3)
                        await self.bot.say("As expected of Ainz-Sama!")
                        await asyncio.sleep(3)    
                    elif Fighter1Role == 100:
                        await self.bot.say("As expected from a servant of Ainz-Sama!")
                        await asyncio.sleep(3)
                    elif Fighter2Role == 100:
                        await self.bot.say("It's utterly disgraceful that a servant of Ainz-Sama could fail like this!")
                        await asyncio.sleep(3)
                        await self.bot.say("I'll have to question whether you should be allowed to stay within Nazarick or not.")
                        await asyncio.sleep(3)
                    else:
                        pass
                    await self.bot.say(author2.name + " is fortunate that Ainz-Sama used revival magic on them.")
                    await asyncio.sleep(3)
                    bank.deposit_gold(author, prize)
                    if author.id == '159043902383456257':
                        await self.bot.say("The winner is " + author.mention + "-Sama! Here is " + str(prize) + " Gold!")
                    else:
                        await self.bot.say("The winner is " + author.mention + "! They won " + str(prize) + " Gold!")
                    return
                else:
                    await self.bot.say("The battle drew to a close and " + author2.name + "fainted.")
                    await asyncio.sleep(3)
                    await self.bot.say("They lost to the opponent.")
                    await asyncio.sleep(3)
                    if author.id == '159043902383456257':
                        await self.bot.say("As expected of Ainz-Sama!")
                        await asyncio.sleep(3)
                    elif author2.id == '159043902383456257':
                        await self.bot.say("I find it hard to understand why Ainz-Sama let you win! He even took lot's of damage right now.")
                        await asyncio.sleep(3)
                        await self.bot.say("No there must be a reason behind it....Ahh it was a lesson for you after all!")
                        await asyncio.sleep(3)
                        await self.bot.say("As expected of Ainz-Sama!")
                        await asyncio.sleep(3)    
                    elif Fighter1Role == 100:
                        await self.bot.say("As expected from a servant of Ainz-Sama!")
                        await asyncio.sleep(3)
                    elif Fighter2Role == 100:
                        await self.bot.say("It's utterly disgraceful that a servant of Ainz-Sama could fail like this!")
                        await asyncio.sleep(3)
                        await self.bot.say("I'll have to question whether you should be allowed to stay within Nazarick or not.")
                        await asyncio.sleep(3)
                    else:
                        pass
                    bank.deposit_gold(author, prize)
                    if author.id == '159043902383456257':
                        await self.bot.say("The winner is " + author.mention + "-Sama! Here is " + str(prize) + " Gold!")
                    else:
                        await self.bot.say("The winner is " + author.mention + "! They won " + str(prize) + " Gold!")
                    return
            elif points2 > points1:
                if abs(points1-points2):
                    await self.bot.say("As the battle drew near " + author.name + " took their final breath and collapsed.")
                    await asyncio.sleep(3)
                    await self.bot.say("It seems like they died.")
                    await asyncio.sleep(3)
                    if author2.id == '159043902383456257':
                        await self.bot.say("As expected of Ainz-Sama!")
                        await asyncio.sleep(3)
                    elif author.id == '159043902383456257':
                        await self.bot.say("I find it hard to understand why Ainz-Sama let you win! He even took lot's of damage right now.")
                        await asyncio.sleep(3)
                        await self.bot.say("No there must be a reason behind it....Ahh it was a lesson for you after all!")
                        await asyncio.sleep(3)
                        await self.bot.say("As expected of Ainz-Sama!")
                        await asyncio.sleep(3)    
                    elif Fighter2Role == 100:
                        await self.bot.say("As expected from a servant of Ainz-Sama!")
                        await asyncio.sleep(3)
                    elif Fighter1Role == 100:
                        await self.bot.say("It's utterly disgraceful that a servant of Ainz-Sama could fail like this!")
                        await asyncio.sleep(3)
                        await self.bot.say("I'll have to question whether you should be allowed to stay within Nazarick or not.")
                        await asyncio.sleep(3)
                    else:
                        pass
                    bank.deposit_gold(author2, prize)
                    await self.bot.say("The winner is " + author2.mention + "! They won " + str(prize) + " Gold!")
                    return
                else:
                    await self.bot.say("The battle drew to a close and " + author.name + "fainted.")
                    await asyncio.sleep(3)
                    await self.bot.say("They lost to the opponent.")
                    await asyncio.sleep(3)
                    if author2.id == '159043902383456257':
                        await self.bot.say("As expected of Ainz-Sama!")
                        await asyncio.sleep(3)
                    elif author.id == '159043902383456257':
                        await self.bot.say("I find it hard to understand why Ainz-Sama let you win! He even took lot's of damage right now.")
                        await asyncio.sleep(3)
                        await self.bot.say("No there must be a reason behind it....Ahh it was a lesson for you after all!")
                        await asyncio.sleep(3)
                        await self.bot.say("As expected of Ainz-Sama!")
                        await asyncio.sleep(3)    
                    elif Fighter2Role == 100:
                        await self.bot.say("As expected from a servant of Ainz-Sama!")
                        await asyncio.sleep(3)
                    elif Fighter1Role == 100:
                        await self.bot.say("It's utterly disgraceful that a servant of Ainz-Sama could fail like this!")
                        await asyncio.sleep(3)
                        await self.bot.say("I'll have to question whether you should be allowed to stay within Nazarick or not.")
                        await asyncio.sleep(3)
                    else:
                        pass
                    bank.deposit_gold(author2, prize)
                    await self.bot.say("The winner is " + author2.mention + "! They won " + str(prize) + " Gold!")
                    return
            else:
                final = randint(1,2)
                if final == 1:
                    points1 = points1 + 1
                else:
                    points2 = points2 + 1
        
        
        
    @pvp.error
    async def pvp_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            await self.bot.say(error)   
    
def setup(bot):
    n = Arena(bot)
    bot.add_cog(n)        