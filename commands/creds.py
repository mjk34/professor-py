import discord, block, blockchain, random
import commands.user as user

from discord.utils import get

from commands.manager import pushBlock
from commands.helper import today, dailyLuck, dailyFortune, getName, fetchContentList, getIcon

filler = ['<', '>', '!', '@', '&']

"""Allow users to randomly generate free uwu once a day"""
async def daily (ctx, BLOCKCHAIN):
    """1. Users can generate uwuCreds based on rng
       2. Usage is checked to function once per day
       3. Blockchain will be validated, new block will be added to end of Blockchain
    """
       
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
    fortune, status = dailyLuck()

    multiplier = 1 + 0.15*bonus
    total = fortune*multiplier

    """Generate new Block"""
    daily_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Daily',
        data = total
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
    test = random.random()
    if test <= 0.40:
        orb_url = 'https://assets.dicebreaker.com/pondering-my-orb-header-art.png/BROK/resize/844%3E/format/jpg/quality/80/pondering-my-orb-header-art.png'
    if test > 0.40 and test <= 0.8:
        PONDER_LIST = fetchContentList('ponder.txt')
        index = random.randint(0, len(PONDER_LIST)-1)
        orb_url = PONDER_LIST[index]
    if test > 0.8:
        PONDER_LIST = fetchContentList('meme.txt')
        index = random.randint(0, len(PONDER_LIST)-1)
        orb_url = PONDER_LIST[index]

    read = ''
    read += dailyFortune()

    """Generate Description"""
    desc = f'{status} **+{total}** creds were added to your *Wallet*!\n'
    
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

"""Allow users to check out much uwuCreds they have accumulated"""
async def wallet (ctx, BLOCKCHAIN):
    """1. Users can view the total amount of CREDs they have
       2. Users can view the total amount of TICKETs they have
       3. Users can view DAILY counters for /uwu, SUBMITs and TOKENs
    """
     
    """Read Blockchain and return user total"""  
    id = ctx.author.id
    user_creds = user.totalCreds(id, BLOCKCHAIN)
    user_tickets = user.totalTickets(id, BLOCKCHAIN)

    user_subs = user.totalSubmits(id, BLOCKCHAIN)
    user_claim = user.claimedCount(id, BLOCKCHAIN)

    daily = {True:'Available', False:'Not Available'}[user.hasDaily(id, BLOCKCHAIN)]
    claim = {True:'Available', False:'Not Available'}[user_claim == 0]

    desc = ''
    desc += f'Daily UwU: \u3000 \u2000 **{daily}**\nClaim Bonus: \u3000**{claim}**\n'
    desc += f'Submissions: \u3000**{user_subs}**\n\n'
    desc += f'Total Creds:\u3000 **{user_creds}**\u3000 Total Tickets: \u2000**{user_tickets}**\n'

    """Return Message"""
    embed = discord.Embed(
        title = f'Wallet',
        description = desc,
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
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
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()

        BLOCKCHAIN.addBlock(recieving_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()
        
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
    
    if amount > 5000:
        text = f'Oi! This is a bit much, did you really try to take {amount} uwuCreds'
        await ctx.send(f'```CSS\n[{text}]\n```')
        return
    
    """Parses Reciever id from <@id>"""
    reciever_id = reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

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
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
    
        BLOCKCHAIN.addBlock(recieving_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()       
        
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

    threshold = 0.25
    if user_creds < 1000:
        threshold = 0.20
    elif user_creds >= 1000 and user_creds < 5000:
        threshold = 0.15
    elif user_creds >= 5000 and user_creds < 10000:
        threshold = 0.1
    elif user_creds >= 10000 and user_creds < 30000:
        threshold = 0.08
    elif user_creds >= 30000 and user_creds < 50000:
        threshold = 0.06
    else:
        threshold = 0.04

    while True:
        left = random.random()
        right = random.random()
        
        if left < threshold and right < threshold and left != right:
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