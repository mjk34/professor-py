import discord, block, random, os
import commands.user as user
import commands.humble as humble

from discord.utils import get
from dotenv import load_dotenv

from commands.activity import getLevel, getLevelXP, level_xp
from commands.helper import today, dailyLuck, dailyFortune, getName, fetchContentList, getIcon
from commands.manager import pushBlock, pushWish
from commands.stats import getStat, stats, getStar, getDarkStar, getReforger
from commands.user import getServerBonus
from commands.wish import getStarPity ,guarenteed

filler = ['<', '>', '!', '@', '&']
status_check = [
        '*Congrats, you are cursed*.',
        '*A honest sum, nothing more*.'
]

load_dotenv()
HUMBLE = int(os.getenv('HUMBLE_ID'))
HBOT = 904417820899700756

"""Allow users to randomly generate free uwu once a day"""
async def daily (ctx, client, BLOCKCHAIN):
    """1. Users can generate uwuCreds based on rng
       2. Usage is checked to function once per day
       3. rng will scale based on server_bonus level
       4. Blockchain will be validated, new block will be added to end of Blockchain
       5. Users will be given 2 WISHes
       6. Humble Love will be checked"""
       
    id, name = ctx.author.id, ctx.author.name
    """Check if the user has already done their daily"""
    if user.hasDaily(id, BLOCKCHAIN) == False:
        embed = discord.Embed(
            title = f'Daily',
            description = f'You next **/uwu** is tomorrow.',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
        
    bonus = int(user.getDailyCount(id, BLOCKCHAIN) / 7)
    server_bonus = getServerBonus(BLOCKCHAIN)
    fortune, status = dailyLuck(server_bonus)

    vitality = getStat(id, stats[0], BLOCKCHAIN)
    multiplier = int(25 + 15*vitality)
    stat_bonus = int((fortune)*(0.10*vitality - pow(vitality, 0.008*vitality) + 1))

    """Generate new Block"""
    daily_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Daily',
        data = fortune + bonus*multiplier + stat_bonus
    )

    fortune_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Luck',
        data = fortune
    )
    
    """Update Blockchain"""
    pushBlock(daily_block, BLOCKCHAIN)
    pushBlock(fortune_block, BLOCKCHAIN)         

    orb_url = 'https://assets.dicebreaker.com/pondering-my-orb-header-art.png/BROK/resize/844%3E/format/jpg/quality/80/pondering-my-orb-header-art.png'
    if random.random() < 0.50:
        PONDER_LIST = fetchContentList('ponder.txt')
        index = random.randint(0, len(PONDER_LIST)-1)
        orb_url = PONDER_LIST[index]

    read = ''
    read += dailyFortune()

    """Generate Description"""
    desc = f'{status} **+{fortune}** creds were added to your *Wallet*!\n'

    desc += f'From **Vitality {vitality}** and **{bonus}** *Bonus Stack(s)*, you get an additional **+{bonus*multiplier + stat_bonus}** creds!\n'

    desc += f'\nNet total: {fortune + bonus*multiplier + stat_bonus}'
    
    """Return Message"""
    embed = discord.Embed(
        title = 'Daily',
        description = desc,
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    embed.add_field(
        name = f'Fortune\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000-',
        value = read
    )
    embed.set_image(url=orb_url)
    await ctx.send(embed=embed)

    """Give Wishes """
    stamina, total_wish = getStat(id, stats[1], BLOCKCHAIN), 2
    if stamina == 1 or stamina == 2: total_wish = 3
    if stamina == 3 or stamina == 4: total_wish = 4
    if stamina == 5 or stamina == 6: total_wish = 5
    if stamina == 7 or stamina == 8: total_wish = 6
    if stamina == 9 or stamina == 10: total_wish = 7
    
    for i in range(total_wish):
        pushWish(id, name, BLOCKCHAIN) 

    """Check Humble Love"""
    if status not in status_check: 
        await humble.chaos(ctx, client, BLOCKCHAIN)

"""Allow users to check out much uwuCreds they have accumulated"""
async def wallet (ctx, BLOCKCHAIN, ACTIVCHAIN):
    """1. Users can view the total amount of CREDs they have
       2. Users can view the total amount of TICKETs they have
       3. Users can view DAILY counters for /uwu, SUBMITs and TOKENs
       4. Users can view Activity Level and next level XP
       5. Users can view WISH count, Pity and if they are Guarenteed
       6. Users can view counters for STARs, DARK STARs, and REFORGERs"""
     
    """Read Blockchain and return user total"""  
    id = ctx.author.id
    user_creds = user.totalCreds(id, BLOCKCHAIN)
    user_tickets = user.totalTickets(id, BLOCKCHAIN) + user.totalStitchedTickets(id, BLOCKCHAIN)

    user_level = getLevel(id, ACTIVCHAIN)
    user_xp = getLevelXP(id, ACTIVCHAIN)
    level_up_xp = level_xp[user_level+1]

    user_tokens = user.totalTokens(id, BLOCKCHAIN)
    user_torn = user.totalTornTickets(id, BLOCKCHAIN)
    user_stars = getStar(id, BLOCKCHAIN)
    user_dstars = getDarkStar(id, BLOCKCHAIN)
    user_reforger = getReforger(id, BLOCKCHAIN)

    user_wish = user.wishCount(id, BLOCKCHAIN)
    user_pity = getStarPity(id, BLOCKCHAIN)
    user_guarenteed = guarenteed(id, BLOCKCHAIN)

    user_subs = user.totalSubsWeek(id, BLOCKCHAIN)
    user_claim = user.claimedCount(id, BLOCKCHAIN)
    user_shield = user.getShieldCount(id, BLOCKCHAIN)
    
    stamina = getStat(id, stats[1], BLOCKCHAIN)

    daily = {True:'Available', False:'Not Available'}[user.hasDaily(id, BLOCKCHAIN)]
    claim = {True:'Available', False:'Not Available'}[user_claim == 0]
    desc = ''

    desc += f'**LEVEL {user_level}**\nNext Level:\u2000{user_xp}/{level_up_xp} XP\n\n'
    
    if stamina == 0:
        desc += f'Daily UwU:\u3000\u3000**{daily}**\nClaim Bonus: \u3000**{claim}**\nSubmissions: \u3000**{(2) - user_subs}/{2}**\n\n'
    else:
        desc += f'Daily UwU:\u3000\u3000**{daily}**\nClaim Bonus: \u3000**{claim}**\nSubmissions: \u3000**{(2 + int(stamina/2)) - user_subs}/{2 + int(stamina/2)}** \n\n'

    desc += f'Wishes:\u2000**{user_wish}**\u3000Pity:\u2000**{user_pity}**\u3000'
    if user_guarenteed:
        desc += 'Guarenteed:\u2000**Yes**\n\n'
    else: 
        desc += 'Guarenteed:\u2000**No**\n\n'

    desc += f'Tokens:\u2000**{user_tokens}**\u3000Shields:\u2000**{user_shield}**\u3000Torn Tickets:\u2000**{user_torn}**\n'
    desc += f'Stars:\u2000**{user_stars}**\u3000 Dark Stars:\u2000**{user_dstars}**\u3000Reforgers:\u2000**{user_reforger}**\n\n'

    desc += f'Total Creds:\u3000 **{user_creds}**\u3000 Total Tickets: \u2000**{user_tickets}**\n'

    """Return Message"""
    embed = discord.Embed(
        title = f'Wallet',
        description = desc,
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
   
"""Allow users to deploy a shield that insures against humble and steals"""
async def deploy_shield(ctx, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user tokens is checked
       2. Blockchain will be validated, new blocks will be added to the end of Blockchain"""
    
    id, name = ctx.author.id, ctx.author.name

    """Check if user has at least one TOKEN to deploy"""
    if user.totalTokens(id, BLOCKCHAIN) < 1:
        embed = discord.Embed(
            title = f'Deploy Shield',
            description = f'You need at least one Token to Deploy a Shield!',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    """Generate new Block"""
    shield_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Shield',
        data = 0
    )

    token_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = '-Token',
        data = 0
    ) 

    pushBlock(shield_block, BLOCKCHAIN)
    pushBlock(token_block, BLOCKCHAIN)

    """Return Message"""
    embed = discord.Embed(
        title = f'Deploy Shield',
        description = f'Token Accepted, Shield is Active. \n\nNOTE: *Shields will last until Monday. 1 Shield will automatically protect against 1 Humble Love or Player Steal*',
        color = 2352682    
    ).set_image(url='https://pa1.narvii.com/7085/63929295629e463986e22d6976b74ba1c350d073r1-500-281_hq.gif')
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)

"""Allow users to deploy an attack that steals another players creds"""
async def deploy_attack(ctx, target, client, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name
    server_bonus = user.getServerBonus(BLOCKCHAIN)

    """Parse the Target id from <@id>"""
    target_id = target
    for ch in filler: target_id = target_id.replace(ch, '')
    target_id = int(target_id)

    target_name = await getName(target_id, client)

    """Check if user has at least one TOKEN to deploy"""
    if user.totalTokens(id, BLOCKCHAIN) < 1:
        embed = discord.Embed(
            title = f'Deploy Attack',
            description = f'You need at least one Token to Deploy an Attack!',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
    
    """Calculate attack power"""
    attack = 275 * (int(server_bonus/3) + 1)
    
    """Check if the Giver has sufficient uwuCreds"""
    target_creds = user.totalCreds(target_id, BLOCKCHAIN)
    if target_creds < attack:
        embed = discord.Embed(
            title = f'Deploy Attack',
            description = f'<@{target_id}> does not have enough creds, don\'t bully the poor!',
            color = 6053215    
        ).set_image(url='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjQzcnU0b2NyNWgyOXUyajBnbG85d2U4Z254OHViOG9kbWZpeXF6MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eiqxzscsYDET6/giphy.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    """Check if target has a shield"""
    shield = 0
    if user.getShieldCount(target_id, BLOCKCHAIN) > 0:
        server_bonus = user.getServerBonus(BLOCKCHAIN)
        shield = 200 * (int(server_bonus/3) + 1)

        """Consume One Shield"""
        shield_block = block.Block(
            user = target_id,
            name = target_name,
            timestamp = today(),
            description = f'-Shield',
            data = 0
        )

        pushBlock(shield_block, BLOCKCHAIN)

    """Generate new Blocks"""
    data1 = 0
    if attack - shield <= 0: data1 = 0
    else: data1 = attack - shield

    attack_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = f'Attack',
        data = data1
    )

    data2 = 0
    if shield - attack >= 0: data2 = 0
    else: data2 = shield - attack

    target_block = block.Block(
        user = target_id,
        name = target_name,
        timestamp = today(),
        description = f'Attack by {name}',
        data = data2
    )

    token_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = '-Token',
        data = 0
    )

    """Update Blockchain"""
    pushBlock(attack_block, BLOCKCHAIN)
    pushBlock(target_block, BLOCKCHAIN)
    pushBlock(token_block, BLOCKCHAIN)

    """Return Message"""
    embed = discord.Embed(
        title = f'Deploy Attack',
        description = f'Token Accepted, You hired an attack against <@{target_id}>. \n\nYour goons siphoned {data1} Creds!',
        color = 2352682    
    ).set_image(url='https://c.tenor.com/LeKYlO4APnwAAAAC/tenor.gif')
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(f'<@{target_id}>', embed=embed)

    if shield > 0:
        embed2 = discord.Embed(
            title = f'Shield Cracked',
            description = f'<@{target_id}>\'s Shield safeguarded {shield} Creds from Humble.',
            color = 16711680   
        ).set_image(url='https://31.media.tumblr.com/85b421f4184e976268a22e64ca90481b/tumblr_inline_noz3mbubgC1rh9lcd_500.gif')
        embed2.set_footer(text='@~ powered by UwUntu')
        await ctx.send(f'<@{target_id}>', embed=embed2)

"""Allow users to give their uwuCreds to another user""" 
async def give(ctx, reciever, client, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user total is checked
       2. Blockchain will be validated, new blocks will be added to the end of Blockchain"""

    """Parses Reciever id from <@id>"""
    giver_id, reciever_id = ctx.author.id, reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

    """Check if the Giver is the reciever"""
    if giver_id == reciever_id:
        embed = discord.Embed(
            title = f'Donate',
            description = f'You cannot donate to yourself!',
            color = 6053215    
        ).set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
    
    """Check if the Giver has sufficient uwuCreds"""
    giver_creds = user.totalCreds(giver_id, BLOCKCHAIN)
    if giver_creds < 500:
        embed = discord.Embed(
            title = f'Donate',
            description = f'Insufficient funds, you currently have **+{giver_creds}** uwuCreds!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
    
    reciever_name = await getName(reciever_id, client)
    if user.hasDonated(giver_id, reciever_name, BLOCKCHAIN):
        embed = discord.Embed(
            title = f'Donate',
            description = f'You have already donated to <@{reciever_id}>!',
            color = 6053215    
        ).set_thumbnail(url='https://media.tenor.com/images/90ea198565528e21b8ec47cdae286395/tenor.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    """Generate new Blocks"""
    giving_block = block.Block(
        user = giver_id,
        name = ctx.author.name,
        timestamp = today(),
        description = f'Donate${reciever_name}',
        data = -500
    )

    recieving_block = block.Block(
        user = reciever_id,
        name = reciever_name,
        timestamp = today(),
        description = f'Recieved from {ctx.author.name}',
        data = 500
    )
    
    """Update Blockchain"""
    pushBlock(giving_block, BLOCKCHAIN)
    pushBlock(recieving_block, BLOCKCHAIN)          
    
    """Return Message"""
    embed = discord.Embed(
        title = f'Give',
        description = f'A donation of **{500}** was generously given to <@{reciever_id}>!',
        color = 16700447    
    ).set_image(url='https://2.bp.blogspot.com/-UMkbGppX02A/UwoAVpunIMI/AAAAAAAAGxo/W9a0M4njhOQ/s1600/4363+-+animated_gif+k-on+k-on!+k-on!!+moe+nakano_azusa.gif')
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(f'<@{reciever_id}>', embed=embed)

    """Give One Wish"""
    pushWish(id, ctx.author.name, BLOCKCHAIN) 
    
"""Allow moderators to generate specified amount of uwuCreds to another user"""
async def handout(ctx, reciever, amount, client, BLOCKCHAIN):
    """1. User will be checked for Moderator status
       2. Blockchain will be validated, new blocks will be added to the end of Blockchain"""
    
    # if amount > 10000:
    #     text = f'Oi! This is not a charity, did you really try to give {amount} uwuCreds'
    #     await ctx.send(f'```CSS\n[{text}]\n```')
    #     return
    
    """Parses Reciever id from <@id>"""
    reciever_id = reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

    if reciever_id == HBOT: reciever_id = HUMBLE

    """Check if the Giver is a moderator"""
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        
        """Generate new Block"""
        recieving_block = block.Block(
            user = reciever_id,
            name = await getName(reciever_id, client),
            timestamp = today(),
            description = f'Handout from {ctx.author.name}',
            data = amount
        )
        
        """Update Blockchain"""
        pushBlock(recieving_block, BLOCKCHAIN)      
        
        """Return Message"""
        embed = discord.Embed(
            title = f'Handout',
            description = f'**{amount}** uwuCreds was handout to <@{reciever_id}>!',
            color = 16749300    
        ).set_image(url='https://i.imgur.com/zVdLFbp.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(f'<@{reciever_id}>', embed=embed)
    else: 
        embed = discord.Embed(
            title = f'Handout',
            description = f'Insufficient power, you are not a moderator!',
            color = 6053215    
        ).set_thumbnail(url='https://media1.tenor.com/images/80662c4e35cf12354f65f1d6f7beada8/tenor.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        
"""Allow moderators to reduce a specified amount of uwuCreds from another user"""
async def take(ctx, reciever, amount, client, BLOCKCHAIN):
    """1. User will be checked for Moderator status
       2. Blockchain will be validated, new blocks will be added to the end of Blockchain"""
    
    if amount > 10000:
        text = f'Oi! This is a bit much, did you really try to take {amount} uwuCreds'
        await ctx.send(f'```CSS\n[{text}]\n```')
        return
    
    """Parses Reciever id from <@id>"""
    reciever_id = reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

    if reciever_id == HBOT: reciever_id = HUMBLE

    """Check if the Giver is a moderator"""
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        
        """Generate new Block"""
        recieving_block = block.Block(
            user = reciever_id,
            name = await getName(reciever_id, client),
            timestamp = today(),
            description = f'Taken by {ctx.author.name}',
            data = -amount
        )
        
        """Update Blockchain"""
        pushBlock(recieving_block, BLOCKCHAIN)           
        
        """Return Message"""
        embed = discord.Embed(
            title = f'Take',
            description = f'**{amount}** uwuCreds was taken from <@{reciever_id}>!',
            color = 16749300    
        ).set_image(url='https://i.gifer.com/7Z7b.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(f'<@{reciever_id}>', embed=embed)
    else: 
        embed = discord.Embed(
            title = f'Take',
            description = f'Insufficient power, you are not a moderator!',
            color = 6053215    
        ).set_thumbnail(url='https://media1.tenor.com/images/80662c4e35cf12354f65f1d6f7beada8/tenor.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)

"Allow users to view vaguely where another user's creds are at"
async def snoop (ctx, target, client, BLOCKCHAIN):

    """Parses Reciever id from <@id>"""
    target_id = target
    for ch in filler: target_id = target_id.replace(ch, '')
    target_id = int(target_id)

    user_creds = user.totalCreds(target_id, BLOCKCHAIN)
    while True:
        left = random.random()
        right = random.random()
        
        if left < 0.15 and right < 0.15 and left != right:
            break

    upper = int((1 + left)*user_creds)
    lower = int((1 - right)*user_creds)

    desc = f'*hmmm*, I suspect <@{target_id}>-chan is around **{lower}**-**{upper}**!'
    target_icon = await getIcon(target_id, client)

    """Return Message"""
    embed = discord.Embed(
        title = f'Snoop',
        description = desc,
        color = 6943230    
    ).set_thumbnail(url=target_icon)
    embed.set_footer(text='@~ powered by UwUntu')
    embed.set_image(url='https://c.tenor.com/LBkGAkraDxQAAAAC/vtuber-hololive.gif')
    await ctx.send(f'<@{target_id}>', embed=embed)