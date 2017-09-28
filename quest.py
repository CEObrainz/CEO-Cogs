from discord.ext import commands
from .economy import NoAccount
from __main__ import send_cmd_help
from .utils import checks
from .utils.dataIO import fileIO
from random import randint
import os
import math
import random
import asyncio
import discord

class Quest:
    def __init__(self, bot):
        self.bot = bot
        self.users = fileIO("data/guild/users.json", "load")
        
    @commands.group(name="quest", pass_context=True)
    async def quest(self, ctx):
        """Quest operations"""
        
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            
            
    def game_checks():        
        def predicate(ctx):
            score = 0;
            bank = self.bot.get_cog('Economy').bank
            if bank.account_exists(ctx.message.author) == True:
                score = score + 1
            if bank.can_spend(ctx.message.author.id, 50) == True:
                score = score + 1
            if bid >= 10 and bid <= 50:
                score = score + 1
            return score == 3
        return commands.check(predicate)
        
    def game_checks_test(ctx):
        return bank.account_exists(ctx.message.author) == True
            
     
    def roleCheck(self, user : discord.User):
        Roles = user.roles
        for Role in Roles[:]:
            if Role.id == "220712429636681728":
                return 2
            elif Role.id == "220712465866948610":
                return 3
            elif Role.id == "220712513484881921":
                return 4
            elif Role.id == "220712535861493760":
                return 5
            elif str(Role.id) == "220712555650351114":
                return 6
            elif Role.id == "220712579587112960":
                return 7
            elif Role.id == "220712606145576960":
                return 8
            elif Role.id == "220712680728559616": 
                return 9
            elif Role.id == "223488592486334465":
                return 10
            elif Role.id == "220756096086704129":
                return 100
            else:
                pass
        return 1
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
    
    def account_check(self, speaker):
        bank = self.bot.get_cog('Economy').bank
        if bank.account_exists(speaker):
            return True
        else:
            return False
            
    def getDifficulty(self, result3):
        if result3 == 1: #Clementine
            return 1200
        elif result3 == 2: #undead
            return 1000
        elif result3 == 3: #demon
            return 2000
        elif result3 == 4: #Phantom Ainz
            return 5010
        elif result3 == 5:
            return 2
        elif result3 == 6:
            return 2
        elif result3 == 7:
            return 2
        else:
            return 100
    
    def getThresh(self, result3):
        if result3 == 1: #Clementine
            return 5
        elif result3 == 2: #undead
            return 6
        elif result3 == 3: #demon
            return 4
        elif result3 == 4: #Phantom Ainz
            return 3
        elif result3 == 5:
            return 1
        elif result3 == 6:
            return 1
        elif result3 == 7:
            return 1
        else:
           return 1
        
    def getBonus(self, result3):
        if result3 == 1: #Clementine
            return 50
        elif result3 == 2: #undead
            return 60
        elif result3 == 3: #demon
            return 100
        elif result3 == 4: #Phantom Ainz
            return 200
        elif result3 == 5:
            return 1
        elif result3 == 6:
            return 1
        elif result3 == 7:
            return 1
        else:
           return 1
    
    def randomPerson(self):
        pep = {}
        pep['1'] = 'Knight'
        pep['2'] = 'Old Man'
        pep['3'] = 'Old Woman'
        pep['4'] = 'General'
        pep['5'] = 'Traveller'
        pep['6'] = 'Merchant'
        pep['7'] = 'Consort'
        pep['8'] = 'Mage'
        pep['9'] = 'Tribal Leader'
        pep['10'] = 'Trader'
        
        pepo = random.choice([pep[i] for i in pep])
        return pepo
        
    def randomEnemy(self, result):
        number = result * 2    
        pep = {}
        pep['1'] = 'Drunk'
        pep['2'] = 'Thieve'#
        pep['3'] = 'Criminal'
        pep['4'] = 'Killer'#
        pep['5'] = 'Enemy Soldier'
        pep['6'] = 'Enemy Mage'#
        pep['7'] = 'Undead'
        pep['8'] = 'Undead Knight'#
        pep['9'] = 'Orc'
        pep['10'] = 'Troll'#
        pep['11'] = 'Pigman'
        pep['12'] = 'Beastman'#
        pep['13'] = 'Corrupted Human'
        pep['14'] = 'Dire Wolf'#
        pep['15'] = 'Great Beast'
        pep['16'] = 'Ancient Beast'#
        pep['17'] = 'Devil Spawn'
        pep['18'] = 'Lesser Devil'#
        pepo = random.choice([pep[number] for number in pep])
        return pepo
            
    def randomItem(self, result):
        number = result * 2    
        items = {}
        items['1'] = 'Apple' 
        items['2'] = 'Old Bone'
        items['3'] = 'Herb'
        items['4'] = 'Goldengale Flower'
        items['5'] = 'Magic Stone'
        items['6'] = 'Enchanted Wood'
        items['7'] = 'Historical Weapon'
        items['8'] = 'Artefact'
        items['9'] = 'Jewel'
        items['10'] = 'Golden Plate'
        items['11'] = 'Lizardman Skin'
        items['12'] = 'Beastman Tool'
        items['13'] = 'Mysterious Sigil'
        items['14'] = 'Ancient Weapon'
        items['15'] = 'Undead Gem'
        items['16'] = 'Elder Lich Bone'
        items['17'] = 'Demonic Book'
        items['18'] = 'Dragon Rune'
        item = random.choice([items[number] for number in items])
        return item
    
    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
            
    def randomBadOutcomeFetch(self, author, itemToCollect):
        badOutcome = {}
        badOutcome['1'] = '{0} had some trouble when a theif stole one of the {1}s that they found.'.format(author, itemToCollect)
        badOutcome['2'] = '{0} used too much force and broke a {1}'.format(author, itemToCollect)
        badOutcome['3'] = '{0} tripped and broke the {1} that they were carrying.'.format(author, itemToCollect)
        badOutcome['4'] = '{0} was attacked by an undead and accidentally stepped on the {1}, breaking it.'.format(author, itemToCollect)
        badOutcome['5'] = '{0} couldn\'t find any {1}s and considered giving up.'.format(author, itemToCollect)
        badOutcome['6'] = '{0} threw a {1} in frustration and broke it.'.format(author, itemToCollect)
        badOutcome['7'] = '{0} saw one of the {1}s in a hard to reach location. They gave up trying to get it.'.format(author, itemToCollect)
        badOutcome['8'] = '{0} found some {1}s......but it broke apart in their hands.'.format(author, itemToCollect)
        bad = random.choice([badOutcome[i] for i in badOutcome])
        return bad
        
    def randomBadOutcomeD(self, author, itemToCollect):
        badOutcome = {}
        badOutcome['1'] = '{0} ran into some bandits and wasted time defeating them.'.format(author)
        badOutcome['2'] = '{0} took the wrong turn and ended up having to retrace theur path.'.format(author)
        badOutcome['3'] = '{0} didn\'t realise they dropped the {1} and had to go back to get it.'.format(author, itemToCollect)
        badOutcome['4'] = '{0} was robbed by a theif and wasted time getting the {1} back.'.format(author, itemToCollect)
        badOutcome['5'] = '{0} fell into a trap and had to spend time healing themselves with a potion.'.format(author)
        badOutcome['6'] = '{0} used expensive random teleport magic....but ended up further away from the target location.'.format(author)
        badOutcome['7'] = '{0} took a risky path that led to a dungeon, {0} marked it down in their personal notes but it was still a waste of time.'.format(author)
        badOutcome['8'] = '{0} helped save a novice adventurer from a monster. Though they did a good deed the lengthy shouts of gratitude afterwards was a considerable time waste.'.format(author)
        bad = random.choice([badOutcome[i] for i in badOutcome])
        return bad
        
    def randomBadOutcomeK(self, author, enemy):
        badOutcome = {}
        badOutcome['1'] = '{0} was hit by a {1} in the shoulder.'.format(author, enemy)
        badOutcome['2'] = '{0} fought hard and killed several {1}s but sustained injuries in the back.'.format(author, enemy)
        badOutcome['3'] = '{0} almost lost their weapon to a {1} and had to pick it up.'.format(author, enemy)
        badOutcome['4'] = '{0} was blinded by trap magic and almost didn\'t see the {1} strike.'.format(author, enemy)
        badOutcome['5'] = '{0} fought with a broken weapon for a while.'.format(author)
        badOutcome['6'] = '{0} was tripped and hurt their knee.'.format(author)
        badOutcome['7'] = '{0} killed a {1} as another one rammed into them.'.format(author, enemy)
        badOutcome['8'] = '{0} lost part of their sight as blood trickled into their eyes.'.format(author)
        badOutcome['9'] = 'During the fight {0} was pushed by an unseen force and lost their footing.'.format(author)
        badOutcome['10'] = 'A flurry of attacks coming from a nearby {1} was enough to push {0} backwards.'.format(author, enemy)
        bad = random.choice([badOutcome[i] for i in badOutcome])
        return bad
        
    def randomBadOutcomeE(self, author, result3):
        if result3 == 1: #Clementine
            ways_to_kill = {}
            ways_to_kill['1'] = '{0} stood up to Clementine, sword in hand and determined to do well. However little did they expect the former Black Scripture member to incite [Ability Boost] so quickly and dash towards them, disabling an arm instantly.'.format(author)
            ways_to_kill['2'] = 'Clementine threw one of her Stilettos at {0}, the blade piercing their left eye.'.format(author)
            ways_to_kill['3'] = '{0} took a fire axe and swung at Clementine, unfortunately the fighter used [Ability Boost] and [Greater Ability Boost] to dodge those attack with ease and counter.'.format(author)
            ways_to_kill['4'] = '{0} barely noticed as his back was stabbed, slowly bleeding as Clementine laughed.'.format(author)
            ways_to_kill['5'] = '{0} tripped over and barely dodged a fatal attack.'.format(author)
            ways_to_kill['6'] = '{0} tried to hit Clementine but the fighter dodged with ease.'.format(author)
            ways_to_kill['7'] = '{0} was stabbed in the knee, forcing them to try and use healing magic.'.format(author)
            ways_to_kill['8'] = '{0} watched as one of their comrades died before their eyes.'.format(author)
            ways_to_kill['9'] = '{0} cringed as Clementine taunted them, a feeling of dread slowly sinking in.'.format(author)
            ways_to_kill['10'] = '{0} squared up to the blond killer but saw something in her eyes that was worrysome.'.format(author)
            WTK = random.choice([ways_to_kill[i] for i in ways_to_kill])
        elif result3 == 2: #undead                
            ways_to_kill = {}
            ways_to_kill['1'] = '{0} was pushed back as the undead slashed with it\'s arm.'.format(author)
            ways_to_kill['2'] = '{0} stuck his sword through the undead\'s body but forgot that swords are one of the least effective methods against undead.'.format(author)
            ways_to_kill['3'] = '{0} tried to use a blunt weapon but it broke rather quickly.'.format(author)
            ways_to_kill['4'] = '{0} tripped over and barely dodged a fatal attack.'.format(author)
            ways_to_kill['5'] = '{0} was slashed in the arm, forcing them to reposition themselves.'.format(author)
            ways_to_kill['6'] = '{0} watched as one of their comrades died before their eyes.'.format(author)
            ways_to_kill['7'] = '{0} was stabbed in the knee, forcing them to try and use healing magic.'.format(author)
            ways_to_kill['8'] = '{0} witnessed a local die due to the undead powers the foe had.'.format(author)
            ways_to_kill['9'] = '{0} felt cold as a curse tried to attack them.'.format(author)
            ways_to_kill['10'] = '{0} attacked with a stone, but the undead caught it....made a weird sound like a laugh and threw it back, injuring your hand..'.format(author)
            WTK = random.choice([ways_to_kill[i] for i in ways_to_kill])
        elif result3 == 3: #demon
            ways_to_kill = {}
            ways_to_kill['1'] = '{0} was hit by a fire attack, burning part of their armour.'.format(author)
            ways_to_kill['2'] = '{0} clashed with the demons weapons yet couldn\'t bypass its defences.'.format(author)
            ways_to_kill['3'] = '{0} was thrown back, injuring themselves greatly'.format(author)
            ways_to_kill['4'] = '{0} tripped over and barely dodged a fatal attack.'.format(author)
            ways_to_kill['5'] = '{0} was caught up fighting the underlings the demon spawned.'.format(author)
            ways_to_kill['6'] = '{0} was trapped by a wall of fire for a moment.'.format(author)
            ways_to_kill['7'] = '{0} was stabbed in the knee, forcing them to try and use healing magic.'.format(author)
            ways_to_kill['8'] = '{0} watched as one of their comrades died before their eyes.'.format(author)
            ways_to_kill['9'] = '{0} was offput by the arrogant like nature of the masked demon.'.format(author)
            ways_to_kill['10'] = '{0} was stunned by the speed the demon had.'.format(author)
            WTK = random.choice([ways_to_kill[i] for i in ways_to_kill])
        elif result3 == 4: #Ainz
            ways_to_kill = {}
            ways_to_kill['1'] = '{0} couldn\'t even land a single hit as time seemingly slowed down.'.format(author)
            ways_to_kill['2'] = '{0} felt terrified for unknown reasons, their resolve to fight shakened.'.format(author)
            ways_to_kill['3'] = '{0} witnessed a glimpse of the carnage that Ainz-Sama was capable of, they threw up slighty.'.format(author)
            ways_to_kill['4'] = '{0} tripped over and barely dodged a fatal attack.'.format(author)
            ways_to_kill['5'] = '{0} watched the Phantom Overlord with fear.'.format(author)
            ways_to_kill['6'] = '{0} couldn\'t see their foe for a while, frightening them.'.format(author)
            ways_to_kill['7'] = '{0} was confused as their vision blurred.'.format(author)
            ways_to_kill['8'] = '{0} failed to land any meaningful hits, the strength of the foe exponentially stronger than them.'.format(author)
            ways_to_kill['9'] = '{0} watched as one of their comrades died before their eyes.'.format(author)
            ways_to_kill['10'] = '{0} was slashed in the back.'.format(author)
            WTK = random.choice([ways_to_kill[i] for i in ways_to_kill])
        else:
            ways_to_kill = {}
            ways_to_kill['1'] = '{0} tripped over and barely dodged a fatal attack.'.format(author)
            WTK = random.choice([ways_to_kill[i] for i in ways_to_kill])
        return WTK

    def randomGoodOutcomeFetch(self, author, itemToCollect):
        goodOutcome = {}
        goodOutcome['1'] = '{0} found some {1}s buried in the dirt.'.format(author, itemToCollect)
        goodOutcome['2'] = '{0} helped an old man on his journey and was given some {1}s as a reward.'.format(author, itemToCollect)
        goodOutcome['3'] = '{0} killed an undead that was carrying a {1}.'.format(author, itemToCollect)
        goodOutcome['4'] = '{0} found a rare {1} inside a treasure chest.'.format(author, itemToCollect)
        goodOutcome['5'] = '{0} found some {1}s in a bag in the middle of the grass.'.format(author, itemToCollect)
        goodOutcome['6'] = '{0} found some {1}s from a fellow Adventurer that died.'.format(author, itemToCollect)
        goodOutcome['7'] = '{0} saw one of the {1}s in a hard to reach location. They got it using magic.'.format(author, itemToCollect)
        goodOutcome['8'] = '{0} found a {1}......a very rare and special kind too.'.format(author, itemToCollect)
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def randomGoodOutcomeD(self, author, itemToCollect):
        goodOutcome = {}
        goodOutcome['1'] = '{0} found a shortcut that allowed them to save some time.'.format(author)
        goodOutcome['2'] = '{0} helped an old man on his journey and was shown a secret path to their destination.'.format(author)
        goodOutcome['3'] = '{0} killed an undead that was in their path.'.format(author)
        goodOutcome['4'] = '{0} found some transportation that sped up their journey.'.format(author)
        goodOutcome['5'] = '{0} drank a stamina potion allowing them to run faster than usual.'.format(author)
        goodOutcome['6'] = '{0} used expensive random teleport magic and managed to get closer to the target.'.format(author)
        goodOutcome['7'] = '{0} took a risky path but saved some time.'.format(author)
        goodOutcome['8'] = '{0} saved time by packing a lighter load than usual.'.format(author)
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def randomGoodOutcomeK(self, author, enemy):
        goodOutcome = {}
        goodOutcome['1'] = '{0} killed a {1} with precision and was fast enough to face the next.'.format(author, enemy)
        goodOutcome['2'] = '{0} saved a local from a {1} and defeated the instigator too, looking heroic.'.format(author, enemy)
        goodOutcome['3'] = '{0} found one of the {1} dead before they could get to it.'.format(author, enemy)
        goodOutcome['4'] = '{0} used healing magic to get rid of any sustained injuries.'.format(author)
        goodOutcome['5'] = '{0} drank a stamina potion which allowed them to overpower a {1}.'.format(author, enemy)
        goodOutcome['6'] = '{0} fought off 3 {1}s with a farming tool, lowering the moral of the enemy.'.format(author, enemy)
        goodOutcome['7'] = '{0} was saved by an ally in the nick of time, killing the {1} before they died themselves.'.format(author, enemy)
        goodOutcome['8'] = '{0} brought well fitting armour that protected them from numerous stikes to the legs.'.format(author)
        goodOutcome['9'] = '{0} was fast enough to dodge an attack from a {1}.'.format(author, enemy)
        goodOutcome['10'] = '{0} saved a local making them look heroic.'.format(author)
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def randomGoodOutcomeE(self, author):
        goodOutcome = {}
        goodOutcome['1'] = '{0} was fast enough to dodge an attack.'.format(author)
        goodOutcome['2'] = '{0} saved a local from a large area attack making them look heroic.'.format(author)
        goodOutcome['3'] = '{0} found one a rare potion lying on the ground and drank it.'.format(author)
        goodOutcome['4'] = '{0} used healing magic to get rid of any sustained injuries.'.format(author)
        goodOutcome['5'] = '{0} drank a stamina potion which allowed them to keep up with their foe.'.format(author)
        goodOutcome['6'] = '{0} fought the enemy with a glowing weapon, intruiging the foe somewhat.'.format(author)
        goodOutcome['7'] = '{0} was saved by an ally in the nick of time, allowing them to reposition themselves.'.format(author)
        goodOutcome['8'] = '{0} brought well fitting armour that protected them from numerous stikes to the legs.'.format(author)
        goodOutcome['9'] = '{0} was pumped full of excitement as the battle raged on.'.format(author)
        goodOutcome['10'] = '{0} drank a strength potion allowing them to fend off more attacks.'.format(author)
        good = random.choice([goodOutcome[i] for i in goodOutcome])
        return good
        
    def is_legal(self, s):
        test = int(s)
        if test == 1:
            return True
        elif test == 2:
            return True
        elif test == 3:
            return True
        elif test == 4:
            return True
        elif test == 5:
            return True
        elif test == 6:
            return True
        elif test == 7:
            return True
        elif test == 8:
            return True
        elif test == 9:
            return True
        else:
            return False
    
    @commands.cooldown(1, 900, commands.BucketType.user)  
    @quest.command(name="start", pass_context=True)  
    async def _Start(self, ctx):
        """Do a Guild Quest"""
        message = ctx.message
        author = message.author.mention
        user = ctx.message.author
        server = ctx.message.server
        AN = ctx.message.author.name
        chn = ctx.message.channel
        bank = self.bot.get_cog('Economy').bank
        guild = self.bot.get_cog('Guild')
        score = self.roleCheck(ctx.message.author)
        if self.account_check(ctx.message.author):
            pass
        else:
            await self.bot.say("You cannot go on a quest without an account. Type '# bank register' first.")   
            return
        await self.bot.say("Choose a rank! Current Rank: " + str(score))
        await self.bot.say("1 - Copper" + "\n" +
        "2 - Iron" + "\n" +
        "3 - Silver" + "\n" +
        "4 - Gold" + "\n" +
        "5 - Platinum" + "\n" +
        "6 - Mythril" + "\n" +
        "7 - Orichalcum" + "\n" +
        "8 - Adamantite" + "\n" +
        "Type exit to quit")
        
        
        while True:
            msg = await self.bot.wait_for_message(timeout =30, author=message.author, channel=chn)
            if msg is not None:
                if msg.content == "exit":
                    return
                elif self.is_number(msg.content) and self.is_legal(msg.content):
                    result = int(msg.content)
                    if result <= score:
                        break
                    else:
                        await self.bot.say("You are not a high enough rank for this kind of quest!") 
                else:
                    await self.bot.say("Invalid Number!") 
                    await self.bot.say("Select the rank of quest you wish to do!")
            else: 
                return
        await self.bot.say("Very well what type of quest would you like to do!")
        await self.bot.say("1 - Fetch Quest" + "\n" +
        "2 - Delivery Quest" + "\n" +
        "3 - Kill Quest" + "\n" +
        "4 - Emergency Quest" + "\n" +   
        "Type exit to quit")
        while True:        
            msg = await self.bot.wait_for_message(timeout =30, author=message.author, channel=chn)
            if msg is not None:
                if msg.content == "exit":
                    return
                elif self.is_number(msg.content) and int(msg.content) > 0 and int(msg.content) < 5:   
                    result2 = int(msg.content)
                    break    
                else:
                    await self.bot.say("Invalid Number!")   
                    await self.bot.say("Select a type of Quest!")    
            else: 
                return
                
        score2 = self.nationCheck(ctx.message.author)
        if result2 == 1:
            noToCollect = randint(20,100)
            itemToCollect = self.randomItem(result)
            await self.bot.say("You chose a Fetch Quest!")
            await asyncio.sleep(2)
            area = self.Quest_areas(result, score2)
            await self.bot.say("We have a mission for you in " + area + "!") 
            await asyncio.sleep(2)
            await self.bot.say("You have a been asked to collect " + str(noToCollect) + " " + itemToCollect + "s in "  + area + ".") 
            await asyncio.sleep(2)
            await self.bot.say("Good Luck!")
            await asyncio.sleep(2)
            TrialDiff = result * 100
            Handicap = score * 50
            kek = 0
            cool = 0
            if Handicap >= TrialDiff:
                #might as well win
                LVL = 10
                Check = 3
            else:
                LVL = TrialDiff - Handicap  
                Check = LVL * 0.45
            lst = ['...'] * 5
            for i in range(5):
                output = randint(1,LVL)
                if output < Check:
                    #Something bad happens
                    msgg = self.randomBadOutcomeFetch(AN, itemToCollect)
                    formatted = msgg.format(msgg) + '  -  Minus 5 ' + itemToCollect
                    if formatted not in lst:
                        lst[i] = formatted
                    #await self.bot.say('**{0}**'.format(msgg) + '  -  Minus 5 ' + itemToCollect)
                    #await asyncio.sleep(3)
                    kek = kek + 1
                    
                elif output > Check:
                    #Something good.
                    #await self.bot.say("You found some more " + itemToCollect + "!")
                    msgg = self.randomGoodOutcomeFetch(AN, itemToCollect)
                    formatted = msgg.format(msgg) + '  -  Plus 2 ' + itemToCollect
                    if formatted not in lst:
                        lst[i] = formatted
                    #await self.bot.say('**{0}**'.format(msgg) + '  -  Plus 2 ' + itemToCollect)
                    #await asyncio.sleep(3)
                    cool = cool + 1
                else:
                    pass
            for lst[i] in lst[:]:
                await self.bot.say(lst[i])
                await asyncio.sleep(3)
            if kek > 2:
                await self.bot.say(author + "I'm sorry, you took too long and the mission was completed by someone else. Better luck next time!")
            elif kek <= 3:                    
                #Player win
                collected = noToCollect + (cool * 2) - (kek * 5)
                await self.bot.say("Congratulations " + author + " on completing the mission!")
                await asyncio.sleep(2)
                await self.bot.say("You collected: " + str(collected) + " " + itemToCollect + "s!")
                await asyncio.sleep(2)
                await self.bot.say("Please wait while we calculate your reward...")
                await asyncio.sleep(4)
                money = (result * 4) + (cool / 10) - (kek * result)
                if score > result:
                    money = money * 0.9
                else:
                    money = money * 1.1
                money = int(round(money))
                await self.bot.say(author + "You have been rewarded: " + str(money) + " Gold!")
                amount = math.ceil(money / 2) + 1
                guild._addXP(server, user, amount)
                await self.bot.say(author + "You got " + str(amount) + " XP!")
                bank.deposit_gold(ctx.message.author, money)
            else:
                await self.bot.say("Something went wrong!")    
        elif result2 == 2:
            await self.bot.say("You chose a Delivery Quest!") 
            await asyncio.sleep(2)
            area = self.Quest_areas(result, score2)
            itemToCollect = self.randomItem(result)
            person = self.randomPerson()
            await self.bot.say("We have a mission for you in " + area + "!") 
            await asyncio.sleep(2)
            await self.bot.say("You have been asked to deliver a " + itemToCollect + " to a " + person + " in " + area + "!")
            await asyncio.sleep(2)
            await self.bot.say("Good Luck!")
            await asyncio.sleep(2)
            TrialDiff = result * 125
            Handicap = score * 50
            kek = 0
            cool = 0
            if Handicap >= TrialDiff:
                #might as well win
                LVL = 10
                Check = 7
                BadCheck = 3
            else:
                LVL = TrialDiff - Handicap  
                Check = LVL * 0.60
                BadCheck = LVL * 0.40
            lst = ['...'] * 7    
            for i in range(7):
                output = randint(1,LVL)
                if output < BadCheck:
                    #Something bad happens
                    msgg = self.randomBadOutcomeD(AN, itemToCollect)
                    formatted = msgg.format(msgg)
                    if formatted not in lst:
                        lst[i] = formatted
                    #await self.bot.say('**{0}**'.format(msgg))
                    #await asyncio.sleep(3)
                    kek = kek + 1
                    
                elif output > Check:
                    #Something good.
                    #await self.bot.say("You found some more " + itemToCollect + "!")
                    msgg = self.randomGoodOutcomeD(AN, itemToCollect)
                    formatted = msgg.format(msgg)
                    if formatted not in lst:
                        lst[i] = formatted
                    #await self.bot.say('**{0}**'.format(msgg))
                    #await asyncio.sleep(3)
                    cool = cool + 1
                else:
                    pass
            for lst[i] in lst[:]:
                await self.bot.say(lst[i])
                await asyncio.sleep(3)
            if kek > 4:
                await self.bot.say(author + "I'm sorry, the person waiting for the item was not at the location. He may have died or was supplied by someone else taking the job. Better luck next time!")
            elif kek <= 4:                    
                #Player win
                await self.bot.say("Congratulations " + author + " on completing the mission!")
                await asyncio.sleep(2)
                await self.bot.say("You delivered: " + itemToCollect + " to the client!")
                await asyncio.sleep(2)
                await self.bot.say("Please wait while we calculate your reward...")
                await asyncio.sleep(4)
                money = (result * 5) + (cool / 5) - (kek * result)
                if score > result:
                    money = money * 0.95
                else:
                    money = money * 1.15
                money = int(round(money))
                await self.bot.say(author + "You have been rewarded: " + str(money) + " Gold!")
                amount = math.ceil(money / 2) + 1
                guild._addXP(server, user, amount)
                await self.bot.say(author + "You got " + str(amount) + " XP!")
                bank.deposit_gold(ctx.message.author, money)
            else:
                await self.bot.say("Something went wrong!")        
        elif result2 == 3:
            await self.bot.say("You chose a Kill Quest!") 
            await asyncio.sleep(2)
            area = self.Quest_areas(result, score2)
            await self.bot.say("We have a mission for you in " + area + "!") 
            await asyncio.sleep(2)
            await self.bot.say("There has been reports of dangerous activity around " + area + ". We need you to investigate and kill whatever is causing the commotion.")
            await asyncio.sleep(3)
            await self.bot.say(author + " packs their equipment and leaves immediately, reaching " + area + " within a few hours due to specialised magic.")
            await asyncio.sleep(3)
            numberToKill = randint(2,30)
            enemy = self.randomEnemy(result)
            await self.bot.say("Finding one of the locals nearby it's quickly disclosed that " + str(numberToKill) + " " + enemy + "s have been causing harm to the locals.")
            await asyncio.sleep(2)
            await self.bot.say("Good Luck!")
            await asyncio.sleep(2)
            TrialDiff = result * 150
            Handicap = score * 50
            kek = 0
            cool = 0
            if Handicap >= TrialDiff:
                #might as well win
                LVL = 10
                Check = 5
                BadCheck = 4
            else:
                LVL = TrialDiff - Handicap  
                Check = LVL * 0.65
                BadCheck = LVL * 0.35
            lst = ['...'] * 10   
            for i in range(10):
                output = randint(1,LVL)
                if output < BadCheck:
                    #Something bad happens
                    msgg = self.randomBadOutcomeK(AN, enemy)
                    formatted = msgg.format(msgg)
                    if formatted not in lst:
                        lst[i] = formatted
                    #await self.bot.say('**{0}**'.format(msgg))
                    #await asyncio.sleep(3)
                    kek = kek + 1
                    
                elif output > Check:
                    #Something good.
                    msgg = self.randomGoodOutcomeK(AN, enemy)
                    formatted = msgg.format(msgg)
                    if formatted not in lst:
                        lst[i] = formatted
                    #await self.bot.say('**{0}**'.format(msgg))
                    #await asyncio.sleep(3)
                    cool = cool + 1
                else:
                    pass
            for lst[i] in lst[:]:
                await self.bot.say(lst[i])
                await asyncio.sleep(3)
            if kek > 5:
                await self.bot.say(author + "I'm sorry, but you sustained too many injuries and the Guild was forced to send someone to rescue you. Perhaps try an easier quest next time!")
            elif kek <= 6:                    
                #Player win
                await self.bot.say("Congratulations " + author + " on completing the mission!")
                await asyncio.sleep(2)
                await self.bot.say("You managed to kill all the " + enemy + "s in the area!")
                await asyncio.sleep(2)
                await self.bot.say("Please wait while we calculate your reward...")
                await asyncio.sleep(4)
                
                money = (result * 10) + (cool / 2.5) - (kek * result) + (numberToKill / 10)
                if score > result:
                    money = money
                else:
                    money = money * 1.2
                money = int(round(money))
                await self.bot.say(author + "You have been rewarded: " + str(money) + " Gold!")
                amount = math.ceil(money / 2) + 1
                guild._addXP(server, user, amount)
                await self.bot.say(author + "You got " + str(amount) + " XP!")
                bank.deposit_gold(ctx.message.author, money)
            else:
                await self.bot.say("Something went wrong!")
        elif result2 == 4:
            await self.bot.say("You chose an Emergency Quest!") 
            await asyncio.sleep(2)
            await self.bot.say("The quests here are extremely dangerous and are only recommended to those that have prior experience with fighting to the death.") 
            await asyncio.sleep(2)
            await self.bot.say("The following Quests are available!") 
            await self.bot.say("1 - Unknown Fighter from the Slain Theocracy" + "\n" +
            "2 - Powerful Undead" + "\n" +
            "3 - Powerful Demon" + "\n" +
            "4 - Mysterious Phantom Spellcaster" + "\n" +
            "Type exit to quit")
            while True:        
                msg = await self.bot.wait_for_message(timeout =30, author=message.author, channel=chn)
                if msg is not None:
                    if msg.content == "exit":
                        return
                    elif self.is_number(msg.content) and int(msg.content) > 0 and int(msg.content) < 5:   
                        result3 = int(msg.content)
                        break    
                    else:
                        await self.bot.say("Invalid Number!")   
                        await self.bot.say("Select mission number!")    
                else:
                    return
            foe = ""
            if result3 == 1:
                foe = "Clementine"
            elif result3 == 2:
                foe = "an undead"
            elif result3 == 3:
                foe = "a Masked Demon"
            elif result3 == 4:
                foe = "Phantom Ainz"
            else:
                await self.bot.say("Something went really wrong!")   
            area = self.Quest_areas(result, score2)
            await self.bot.say("It seems that "+ foe + " has been seen in " + area + "!") 
            await asyncio.sleep(2)
            await self.bot.say("You will depart immediately!")
            await asyncio.sleep(5)
            await self.bot.say(author + " packs their equipment and leaves immediately, reaching " + area + " within a few hours due to specialised magic.")
            await asyncio.sleep(3)
            await self.bot.say("Upon reaching " + area + " " + AN + " can feel a powerful presence!")
            await asyncio.sleep(2)
            await self.bot.say("Good Luck!")
            await asyncio.sleep(5)
            TrialDiff = self.getDifficulty(result3)
            Handicap = score * 50
            kek = 0
            cool = 0
            if Handicap >= TrialDiff:
                #might as well win
                LVL = 10
                Check = 5
                BadCheck = 4
            else:
                LVL = TrialDiff - Handicap  
                Check = LVL * 0.8
                BadCheck = LVL * 0.4
            lst = ['...'] * 10   
            for i in range(10):
                output = randint(1,LVL)
                if output < BadCheck:
                    #Something bad happens
                    msgg = self.randomBadOutcomeE(AN, result3)
                    formatted = msgg.format(msgg)
                    if formatted not in lst:
                        lst[i] = formatted
                    #await self.bot.say('**{0}**'.format(msgg))
                    #await asyncio.sleep(3)
                    kek = kek + 1
                    
                elif output > Check:
                    #Something good.
                    msgg = self.randomGoodOutcomeE(AN)
                    formatted = msgg.format(msgg)
                    if formatted not in lst:
                        lst[i] = formatted
                    #await self.bot.say('**{0}**'.format(msgg))
                    #await asyncio.sleep(3)
                    cool = cool + 1
                else:
                    pass
            for lst[i] in lst[:]:
                await self.bot.say(lst[i])
                await asyncio.sleep(3)
            thresh = self.getThresh(result3)    
            if kek > 8: #dead
                await self.bot.say(author + "......hello. You have just been revived. Unfortunately you died. This means we can't give you a reward. Perhaps try an easier mission or quest next time!")
            elif kek >= thresh:
                await self.bot.say(author + "I'm sorry, but you sustained too many injuries and the Guild was forced to send someone to rescue you. Perhaps try an easier mission or quest next time!")
            elif kek < thresh and kek > 1:                    
                #Player win
                await self.bot.say("Thank you for the hard work " + author + ". Although you didn't kill the foe we collected valuable information about them!")
                await asyncio.sleep(2)
                await self.bot.say("Please wait while we calculate your reward...")
                await asyncio.sleep(4)
                money = (result * 15) + (cool / 2) - (kek * result)
                if score > result:
                    money = money
                else:
                    money = money * 1.5
                money = int(round(money))
                await self.bot.say(author + "You have been rewarded: " + str(money) + " Gold!")
                amount = math.ceil(money / 2) + 1
                guild._addXP(server, user, amount)
                await self.bot.say(author + "You got " + str(amount) + " XP!")
                bank.deposit_gold(ctx.message.author, money)
            elif kek <= 1:                    
                #Player win
                await self.bot.say("Congratulations " + author + ". You managed to do it....you managed to beat " + foe + "!")
                await asyncio.sleep(2)
                await self.bot.say("Please wait while we calculate your reward...")
                await asyncio.sleep(4)
                bonus = self.getBonus(result3)
                money = (result * 20) + (cool / 2) - (kek * result) + bonus
                if score > result:
                    money = money
                else:
                    money = money * 1.5
                money = int(round(money))
                await self.bot.say(author + "You have been rewarded: " + str(money) + " Gold!")
                amount = math.ceil(money / 2) + 1
                guild._addXP(server, user, amount)
                await self.bot.say(author + "You got " + str(amount) + " XP!")
                bank.deposit_gold(ctx.message.author, money)
            else:
                await self.bot.say("Something went wrong!")
        else:
            await self.bot.say("Something went really wrong!") 
        
        
    def Quest_areas(self, result, score2):
        if score2 == 2 and result == 2 or result == 1:
            #E-Rantel
            areas = {}
            areas['1'] = 'E-Rantel' 
            areas['2'] = 'E-Rantel outskirts'
            areas['3'] = 'E-Rantel Plains'
            choice = random.choice([areas[i] for i in areas])
        elif score2 == 3 and result == 2 or result == 1:
            #The Empire
            areas = {}
            areas['1'] = 'the Empire' #
            areas['2'] = 'the Empire outskirts'
            areas['3'] = 'the Empire plains'
            choice = random.choice([areas[i] for i in areas])
        elif score2 == 4 and result == 2 or result == 1:
            #The Empire
            areas = {}
            areas['1'] = 'the Slane Theocracy' 
            areas['2'] = 'the Slane Theocracy outskirts'
            areas['3'] = 'the Slane Theocracy plains'
            choice = random.choice([areas[i] for i in areas])
        elif result == 3:
            #Iron
            areas = {}
            areas['1'] = 'Katze Plains' 
            areas['2'] = 'Tob Forests'
            areas['3'] = 'the Great Lake'
            choice = random.choice([areas[i] for i in areas])
        elif result == 4:
            #Silver
            areas = {}
            areas['1'] = 'the Dwarf kingdom'
            areas['2'] = 'the Cryptic Woods'
            areas['3'] = 'Katze Plains'
            areas['4'] = 'Tob Forests'
            areas['5'] = 'the Great Lake'
            choice = random.choice([areas[i] for i in areas])
        elif result == 5:
            #Gold
            areas = {}
            areas['1'] = 'the Holy Kingdom' #Copper
            areas['2'] = 'the Draconic kingdom'
            areas['3'] = 'the Deep Woods'
            choice = random.choice([areas[i] for i in areas])
        elif result == 6:
            #Platinum
            areas = {}
            areas['1'] = 'the Republic' #Copper
            areas['2'] = 'the Beastmen Kingdom'
            choice = random.choice([areas[i] for i in areas])
        elif result == 7:
            #Mythril
            areas = {}
            areas['1'] = 'a Orc settlement' #Copper
            areas['2'] = 'the Elf kingdom'
            choice = random.choice([areas[i] for i in areas])
        elif result == 8:
            #Orichalcum
            areas = {}
            areas['1'] = 'the Dark Elf forest' #Copper
            areas['2'] = 'the Dark dwarf country'
            choice = random.choice([areas[i] for i in areas])
        elif result == 9:
            #Adamantite
            areas = {}
            areas['1'] = 'the Flying city' #Copper
            areas['2'] = 'the Land of Dragon Riders'
            choice = random.choice([areas[i] for i in areas])
        else:
            #Hero/Other#Nazarick
            areas = {}
            areas['1'] = 'Nazarick' #Copper
            choice = random.choice([areas[i] for i in areas])  
        return choice   
     
    
    @_Start.error
    async def _Start_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            await self.bot.say(error)      
            
    def subtract_bet(self, userid, bet, server):
        bank = self.bot.get_cog('Economy').bank
        mobj = server.get_member(userid)
        if self.account_check(mobj):
            bank.withdraw_gold(mobj, bet)
   
    def add_total(self, winner, total, server):
        bank = self.bot.get_cog('Economy').bank
        i = -1
        for winner in winners:
            i = i + 1
            userid = winner.replace(',', '')
            mobj = server.get_member(userid)
            bank.deposit_gold(mobj, totals[i])
            
            
def setup(bot):
    n = Quest(bot)
    bot.add_cog(n)
