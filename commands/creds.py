import discord, block, blockchain, random
import commands.user as user

from discord.utils import get
from commands.helper import today, dailyLuck, dailyFortune, getName, fetchContentList

filler = ['<', '>', '!', '@']

"""Allow users to randomly generate free uwu once a day"""
async def daily (ctx, BLOCKCHAIN):
    """1. Users can generate uwuCreds based on rng
       2. Usage is checked to function once per day
       3. Blockchain will be validated, new block will be added to end of Blockchain"""
       
    id, name = ctx.author.id, ctx.author.name
    """Check if the user has already done their daily"""
    if user.hasDaily(id, BLOCKCHAIN) == False:
        embed = discord.Embed(
            title = f'Daily',
            description = f'You next **/uwu** is tomorrow, it now resets based on date!',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by oogway desu')
        await ctx.send(embed=embed)
        return
    
    bonus = int(user.getDailyCount(id, BLOCKCHAIN) / 8)
    
    """Generate new Block"""
    fortune, status = dailyLuck()
    new_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Daily',
        data = fortune + bonus*100
    )
    
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(new_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()           
    BLOCKCHAIN.printChain()

    orb_url = 'https://assets.dicebreaker.com/pondering-my-orb-header-art.png/BROK/resize/844%3E/format/jpg/quality/80/pondering-my-orb-header-art.png'
    if random.random() < 0.50:
        PONDER_LIST = fetchContentList('ponder.txt')
        index = random.randint(0, len(PONDER_LIST)-1)
        orb_url = PONDER_LIST[index]

    read = ''
    read += dailyFortune()
    
    desc = f'{status} **+{fortune}** creds were added to your *Wallet*!\n'
    if bonus > 0:
        desc += f'From **+{bonus}** *Bonus*, you get an additional **+{bonus*100}** creds!'
    
    """Return Message"""
    embed = discord.Embed(
        title = 'Daily',
        description = desc,
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by oxygen tax')
    embed.add_field(
        name = f'Fortune\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000-',
        value = read
    )
    embed.set_image(url=orb_url)

    await ctx.send(embed=embed)
    
"""Allow users to check out much uwuCreds they have accumulated"""
async def wallet (ctx, BLOCKCHAIN):
    """1. Users can view the total amount of uwuCreds they have
       2. Users can view the total amount of tickets they have
       3. Users can view daily counters for /uwu and submissions"""
     
    """Read Blockchain and return user total"""  
    id = ctx.author.id
    user_creds = user.totalCreds(id, BLOCKCHAIN)
    user_tickets = user.totalTickets(id, BLOCKCHAIN)
    user_subs = user.totalSubsToday(id, BLOCKCHAIN)

    claim = {True:'Available', False:'Not Available'}[user.hasClaim(id, BLOCKCHAIN) == True]
    
    daily = {True:'Available', False:'Not Available'}[user.hasDaily(id, BLOCKCHAIN)]
    desc = f'Daily UwU:\u3000\u3000**{daily}**\nClaim Bonus: \u3000**{claim}**\nSubmissions: \u3000**{3 - user_subs}/3** \u3000Left\n\n'
    desc += f'Total Creds:\u3000**{user_creds}**\u3000 Total Tickets: \u3000**{user_tickets}**'

    BLOCKCHAIN.printChain()

    """Return Message"""
    embed = discord.Embed(
        title = f'Wallet',
        description = desc,
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by oxygen tax')
    await ctx.send(embed=embed)
   
"""Allow users to give their uwuCreds to another user""" 
async def give (ctx, reciever, amount, client, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user total is checked
       2. Blockchain will be validated, new blocks will be added to the end of Blockchain"""

    """Parses Reciever id from <@id>"""
    giver_id, reciever_id = ctx.author.id, reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)
    
    """Check if the Giver has sufficient uwuCreds"""
    giver_creds = user.totalCreds(giver_id, BLOCKCHAIN)
    if giver_creds < amount:
        embed = discord.Embed(
            title = f'Give',
            description = f'Insufficient funds, you currently have **+{giver_creds}** uwuCreds!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by oxygen tax')
        await ctx.send(embed=embed)
        return
    
    reciever_name = await getName(reciever_id, client)

    """Generate new Blocks"""
    new_block1 = block.Block(
        user = giver_id,
        name = ctx.author.name,
        timestamp = today(),
        description = f'Gave {amount} to {reciever_name}',
        data = -amount
    )

    new_block2 = block.Block(
        user = reciever_id,
        name = reciever_name,
        timestamp = today(),
        description = f'Recieved {amount} from {ctx.author.name}',
        data = amount
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
        description = f'**{amount}** uwuCreds was given to <@{reciever_id}>!',
        color = 16700447    
    ).set_image(url='https://2.bp.blogspot.com/-UMkbGppX02A/UwoAVpunIMI/AAAAAAAAGxo/W9a0M4njhOQ/s1600/4363+-+animated_gif+k-on+k-on!+k-on!!+moe+nakano_azusa.gif')
    embed.set_footer(text='@~ powered by oxygen tax')
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
        embed.set_footer(text='@~ powered by oxygen tax')
        await ctx.send(embed=embed)
    else: 
        embed = discord.Embed(
            title = f'Handout',
            description = f'Insufficient power, you are not a moderator!',
            color = 6053215    
        ).set_thumbnail(url='https://media1.tenor.com/images/80662c4e35cf12354f65f1d6f7beada8/tenor.gif')
        embed.set_footer(text='@~ powered by oxygen tax')
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
        embed.set_footer(text='@~ powered by oxygen tax')
        await ctx.send(embed=embed)
    else: 
        embed = discord.Embed(
            title = f'Take',
            description = f'Insufficient power, you are not a moderator!',
            color = 6053215    
        ).set_thumbnail(url='https://media1.tenor.com/images/80662c4e35cf12354f65f1d6f7beada8/tenor.gif')
        embed.set_footer(text='@~ powered by oxygen tax')
        await ctx.send(embed=embed)