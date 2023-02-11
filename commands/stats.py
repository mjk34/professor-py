import discord, block, blockchain, random, os
import commands.user as user

from commands.helper import today

"""Allow users to view their stat progress and benefits"""
"""Vitality, Stamina, Strength, Dexterity, Fortune, Star"""

async def stats (ctx, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name
    star = getStar(id, BLOCKCHAIN)

    vitality = getVitality(id, BLOCKCHAIN)
    vit_str = f'*gain* **+{10*vitality}%** *uwuCreds from Dailies, including bonus*'

    stamina = getStamina(id, BLOCKCHAIN)
    sta_str = f'*gain* **+{1*stamina}** *submission and* **+{int(stamina/2)}** *weekly claim bonus*'

    strength = getStrength(id, BLOCKCHAIN)
    str_str = f'*gain* **+{40*strength}** *additional uwuCreds per submission*'

    dexterity = getDexterity(id, BLOCKCHAIN)
    dex_str = f'*gain* **+{25*dexterity}%** *uwuCreds from clip reviews bonuses*'

    fortune = getFortune(id, BLOCKCHAIN)
    for_str = f'*gain* **+{1*fortune}** *bonus stacks and* **+{int(fortune/2)}** *daily wishes*'

    desc = f'Below lists your current student stats and benefits:\n\n'
    desc += f'**Vitality {vitality}** \u3000 {vit_str}.\n'
    if vitality < 5: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(NEXT: {800*(vitality + 1)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n'

    desc += f'**Stamina {stamina}** \u3000 {sta_str}.\n'
    if stamina < 5: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(NEXT : {600 + 800*(stamina)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n'

    desc += f'**Strength {strength}** \u3000 {str_str}.\n'
    if strength < 5: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(NEXT: {400 + 600*(strength)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n\n'

    desc += f'**Dexterity {dexterity}**\u3000{dex_str}.\n'
    if dexterity < 5: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(NEXT: {800 + 600*(dexterity)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n\n'

    desc += f'**Fortune {fortune}** \u3000 {for_str}.\n'
    if fortune < 5: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(NEXT: {800 + 900*(fortune)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n\n'

    desc += f'You have **{star} STAR**(s), bring them to the Starforger with /set_star to upgrade a core stat. \n\n'

    """Return Message"""
    embed = discord.Embed(
        title = f'{name}\'s Stats',
        description = desc,
        color = 15814693,
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
    return

async def levelUp (ctx, stat_name, BLOCKCHAIN):
    if stat_name == 'vitality' or stat_name == 'Vitality' or stat_name == 'VIT':
        await levelStat(ctx, 'Vitality', BLOCKCHAIN)
    if stat_name == 'stamina' or stat_name == 'Stamina' or stat_name == 'STA':
        await levelStat(ctx, 'Stamina', BLOCKCHAIN)
    if stat_name == 'strength' or stat_name == 'Strength' or stat_name == 'STR':
        await levelStat(ctx, 'Strength', BLOCKCHAIN)
    if stat_name == 'dexterity' or stat_name == 'Dexterity' or stat_name == 'DEX':
        await levelStat(ctx, 'Dexterity', BLOCKCHAIN)
    if stat_name == 'fortune' or stat_name == 'Fortune' or stat_name == 'FOR':
        await levelStat(ctx, 'Fortune', BLOCKCHAIN)

async def levelStat (ctx, stat_name, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name

    stat, cost = 0, 0
    if stat_name == 'Vitality':
        stat = getVitality(id, BLOCKCHAIN)
        cost = 800*(stat + 1)
    if stat_name == 'Stamina':
        stat = getStamina(id, BLOCKCHAIN)
        cost = 600 + 800*(stat + 1)
    if stat_name == 'Strength':
        stat = getStrength(id, BLOCKCHAIN)
        cost = 400 + 600*(stat + 1)
    if stat_name == 'Dexterity':
        stat = getDexterity(id, BLOCKCHAIN)
        cost = 800 + 600*(stat + 1)
    if stat_name == 'Fortune':
        stat = getFortune(id, BLOCKCHAIN)
        cost = 800 + 900*(stat + 1)

    creds = user.totalCreds(id, BLOCKCHAIN)

    if stat >= 5:
        desc = f'Your **{stat_name}** is at MAX level, use STARs to further this stat.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Level Up - {stat_name}',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    if creds < cost:
        desc = f'Insufficient funds. **{stat_name} {stat}** -> **{stat_name} {stat+1}** requires **{cost}** uwuCreds.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Level up - {stat_name}',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
    
    else: 
        """Generate new Block"""
        new_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = f'{stat_name}',
            data = -cost
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
    
        BLOCKCHAIN.addBlock(new_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           

        desc = f'Congratulations. **{stat_name} {stat}** -> **{stat_name} {stat+1}**!!!\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Level up - {stat_name}',
            description = desc,
            color = 2352682,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

async def wish (ctx, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name
    creds, cost = user.totalCreds(id, BLOCKCHAIN), 200
    fortune = getFortune(id, BLOCKCHAIN)

    if user.hasWish(id, BLOCKCHAIN) >= 2 + int(fortune/2):
        desc = f'You have no more Wishes left for today.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Wish Upon a Star',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    if creds < cost: 
        desc = f'Insufficient Funds. a wish costs **200** uwuCreds.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Wish Upon a Star',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
    
    star_flag = False
    if random.random() < 0.035:
        star_flag = True

    """Generate new Block"""
    new_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = f'Wish',
        data = -200
    )

    star_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description= 'Star',
        data = 0
    )
    
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(new_block)
    if star_flag: 
        BLOCKCHAIN.addBlock(star_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()   

    if star_flag: 
        desc = f'Congratulations. You gained a Star!!!.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Wish Upon a Star',
            description = desc,
            color = 2352682,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://media0.giphy.com/media/hd1ilw50Zdb8Y/giphy.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
    else:
        desc = f'You reached for the Stars, but they were too far.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Wish Upon a Star',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://media0.giphy.com/media/nWPLGmsjvdQ4g/giphy.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

async def setStar (ctx, stat_name, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name
    star = getStar(id, BLOCKCHAIN)

    if star < 0:
        embed = discord.Embed(
            title = f'Starforger',
            description = f'The Starforger does not sense the power of a STAR within you, return once you have a STAR.',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    # Check Spelling
    stat, stat_level = '', 0
    if stat_name == 'vitality' or stat_name == 'Vitality' or stat_name == 'VIT':
        stat = 'Vitality'
        stat_level = getVitality(id, BLOCKCHAIN) + 1
    if stat_name == 'stamina' or stat_name == 'Stamina' or stat_name == 'STA':
        stat = 'Stamina'
        stat_level = getStamina(id, BLOCKCHAIN) + 1
    if stat_name == 'strength' or stat_name == 'Strength' or stat_name == 'STR':
        stat = 'Strength'
        stat_level = getStrength(id, BLOCKCHAIN) + 1
    if stat_name == 'dexterity' or stat_name == 'Dexterity' or stat_name == 'DEX':
        stat = 'Dexterity'
        stat_level = getDexterity(id, BLOCKCHAIN) + 1
    if stat_name == 'fortune' or stat_name == 'Fortune' or stat_name == 'FOR':
        stat = 'Fortune'
        stat_level = getFortune(id, BLOCKCHAIN) + 1

    """Generate new Block"""
    anti_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = f'-Star',
        data = 0
    )

    stat_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description= stat,
        data = 0
    )

    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(anti_block)
    BLOCKCHAIN.addBlock(stat_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()
    
    """Return Message"""
    desc = f'The Starforger shaped your STAR into **{stat} {stat_level}**.\n\n'

    """Return Message"""
    embed = discord.Embed(
        title = f'Starforger',
        description = desc,
        color = 2352682,
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_image(url='https://media.tenor.com/N9tfR3_w9uYAAAAC/gojo-satoru-hollow-purple.gif')
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)

def getVitality (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    vitality = 0

    desc = 'Vitality'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                vitality += 1
    return vitality
    
def getStamina (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    stamina = 0

    desc = 'Stamina'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                stamina += 1
    return stamina

def getStrength (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    strength = 0

    desc = 'Strength'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                strength += 1
    return strength

def getDexterity (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    dexterity = 0

    desc = 'Dexterity'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                dexterity += 1
    return dexterity

def getFortune (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    fortune = 0

    desc = 'Fortune'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                fortune += 1
    return fortune

def getStar (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    star = 0

    desc, desc2 = 'Star', '-Star'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                star += 1
            if block.getDesc() == desc2:
                star -= 1
    return star