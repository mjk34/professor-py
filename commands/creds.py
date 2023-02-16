import discord, block, blockchain, random, os
import commands.user as user
import commands.humble as humble

from discord.utils import get
from dotenv import load_dotenv
from commands.helper import today, dailyLuck, dailyFortune, getName, fetchContentList, getIcon
from commands.stats import getVitality, getStamina, getFortune

filler = ['<', '>', '!', '@', '&']

load_dotenv()
HUMBLE = int(os.getenv('HUMBLE_ID'))
HBOT = 904417820899700756

"""Allow users to randomly generate free uwu once a day"""
async def daily (ctx, client, BLOCKCHAIN):
    """1. Users can generate uwuCreds based on rng
       2. Usage is checked to function once per day
       3. Blockchain will be validated, new block will be added to end of Blockchain"""
       
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
    
    fortune, status = dailyLuck()
    bonus = int(user.getDailyCount(id, BLOCKCHAIN) / 7) + int(getFortune(id, BLOCKCHAIN))
    
    vitality = getVitality(id, BLOCKCHAIN)
    stat_bonus = int((fortune + bonus*100)*(0.10*vitality))

    """Generate new Block"""
    new_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Daily',
        data = fortune + bonus*100 + stat_bonus
    )
    
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(new_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()           

    orb_url = 'https://assets.dicebreaker.com/pondering-my-orb-header-art.png/BROK/resize/844%3E/format/jpg/quality/80/pondering-my-orb-header-art.png'
    if random.random() < 0.50:
        PONDER_LIST = fetchContentList('ponder.txt')
        index = random.randint(0, len(PONDER_LIST)-1)
        orb_url = PONDER_LIST[index]

    read = ''
    read += dailyFortune()
    
    desc = f'{status} **+{fortune}** creds were added to your *Wallet*!\n'
    if bonus > 0:
        desc += f'From **+{bonus}** *Bonus*, you get an additional **+{bonus*100}** creds!\n'
    if vitality > 0:
        desc += f'\nFrom **Vitality {vitality}**, you get an additional **+{stat_bonus}** creds!' 

    desc += f' Net total: {fortune + bonus*100 + stat_bonus}'
    
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

    if fortune >= 400:
        await humble.chaos(ctx, client, bonus, BLOCKCHAIN)
    
"""Allow users to check out much uwuCreds they have accumulated"""
async def wallet (ctx, BLOCKCHAIN):
    """1. Users can view the total amount of uwuCreds they have
       2. Users can view the total amount of tickets they have
       3. Users can view daily counters for /uwu and submissions"""
     
    """Read Blockchain and return user total"""  
    id = ctx.author.id
    user_creds = user.totalCreds(id, BLOCKCHAIN)
    user_tickets = user.totalTickets(id, BLOCKCHAIN)

    user_subs = user.totalSubsWeek(id, BLOCKCHAIN)
    user_claim = user.hasClaim(id, BLOCKCHAIN)
    user_wish = user.hasWish(id, BLOCKCHAIN)

    stamina = getStamina(id, BLOCKCHAIN)
    fortune = getFortune(id, BLOCKCHAIN)

    total_wish = 2 + int(fortune/2)
    total_claim = 1 + int(stamina/2)

    daily = {True:'Available', False:'Not Available'}[user.hasDaily(id, BLOCKCHAIN)]
    desc = f'Daily UwU:\u3000\u3000**{daily}**\nDaily Wish:\u3000\u3000**{total_wish - user_wish}/{total_wish}**\nClaim Bonus: \u3000**{total_claim - user_claim}/{total_claim}**\nSubmissions: \u3000**{(5 + stamina) - user_subs}/{5 + stamina}** \n\n'
    desc += f'Total Creds:\u3000**{user_creds}**\u3000 Total Tickets: \u3000**{user_tickets}**'

    BLOCKCHAIN.printChain()

    """Return Message"""
    embed = discord.Embed(
        title = f'Wallet',
        description = desc,
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
   
"""Allow users to give their uwuCreds to another user""" 
async def give (ctx, reciever, client, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user total is checked
       2. Blockchain will be validated, new blocks will be added to the end of Blockchain"""

    """Parses Reciever id from <@id>"""
    giver_id, reciever_id = ctx.author.id, reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)
    
    """Check if the Giver has sufficient uwuCreds"""
    giver_creds = user.totalCreds(giver_id, BLOCKCHAIN)
    if giver_creds < 200:
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
    new_block1 = block.Block(
        user = giver_id,
        name = ctx.author.name,
        timestamp = today(),
        description = f'Donate${reciever_name}',
        data = -200
    )

    new_block2 = block.Block(
        user = reciever_id,
        name = reciever_name,
        timestamp = today(),
        description = f'Recieved from {ctx.author.name}',
        data = 200
    )
    
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(new_block1)
    BLOCKCHAIN.addBlock(new_block2)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()           
    
    """Return Message"""
    embed = discord.Embed(
        title = f'Give',
        description = f'A donation of **{200}** was generously given to <@{reciever_id}>!',
        color = 16700447    
    ).set_image(url='https://2.bp.blogspot.com/-UMkbGppX02A/UwoAVpunIMI/AAAAAAAAGxo/W9a0M4njhOQ/s1600/4363+-+animated_gif+k-on+k-on!+k-on!!+moe+nakano_azusa.gif')
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
    
"""Allow moderators to generate specified amount of uwuCreds to another user"""
async def handout(ctx, reciever, amount, client, BLOCKCHAIN):
    """1. User will be checked for Moderator status
       2. Blockchain will be validated, new blocks will be added to the end of Blockchain"""
    
    if amount > 5000:
        text = f'Oi! This is not a charity, did you really try to give {amount} uwuCreds'
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
        new_block = block.Block(
            user = reciever_id,
            name = await getName(reciever_id, client),
            timestamp = today(),
            description = f'Handout from {ctx.author.name}',
            data = amount
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
    
        BLOCKCHAIN.addBlock(new_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           
        
        """Return Message"""
        embed = discord.Embed(
            title = f'Handout',
            description = f'**{amount}** uwuCreds was handout to <@{reciever_id}>!',
            color = 16749300    
        ).set_image(url='https://i.imgur.com/zVdLFbp.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
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
    
    if amount > 5000:
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
        new_block = block.Block(
            user = reciever_id,
            name = await getName(reciever_id, client),
            timestamp = today(),
            description = f'Taken by {ctx.author.name}',
            data = -amount
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
    
        BLOCKCHAIN.addBlock(new_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           
        
        """Return Message"""
        embed = discord.Embed(
            title = f'Take',
            description = f'**{amount}** uwuCreds was taken from <@{reciever_id}>!',
            color = 16749300    
        ).set_image(url='https://i.gifer.com/7Z7b.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
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
        
        if left < 0.20 and right < 0.20 and left != right:
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
    await ctx.send(embed=embed)