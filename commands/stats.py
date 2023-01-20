import discord, block, blockchain, random, os
import commands.user as user

from commands.helper import today

vitality_benefits = [0, 0.10, 0.15, 0.25, 0.30, 0.40, 0.50]
vitality_costs = [0, 500, 1000, 1800, 2800, 5000, 7000]

stamina_benefits1 = [0, 2, 2, 4, 4, 5, 5]
stamina_benefits2 = [0, 0, 0, 0, 0, 1, 2]
stamina_costs = [0, 700, 1400, 2100, 2700, 3500, 6000]

strength_benefits = [0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50]
strength_costs = [0, 500, 1000, 1800, 2800, 5000, 7000]

dexterity_benefits = [0, 0.25, 0.25, 0.50, 0.50, 0.75, 1.00]
dexterity_costs = [0, 500, 1000, 1800, 2800, 5000, 7000]

fortune_benefits = [0, 1, 2, 3, 4, 5, 6]
fortune_costs = [0, 800, 1600, 2400, 3200, 6400, 8000]

"""Allow users to view their stat progress and benefits"""
"""Vitality, Stamina, Strength, Dexterity, Fortune, Star"""
async def stats (ctx, BLOCKCHAIN):
    
    id, name = ctx.author.id, ctx.author.name

    star = getStar(id, BLOCKCHAIN)
    luc_str = f'gain **+{star}** to all other stats'

    vitality = getVitality(id, BLOCKCHAIN)
    if vitality < 6: vitality += star
    vit_str = f'*gain* **+{vitality_benefits[vitality]*100}%** *uwuCreds from Dailies, including bonus*'

    stamina = getStamina(id, BLOCKCHAIN)
    if stamina < 6: stamina += star
    sta_str = f'*gain* **+{stamina_benefits1[stamina]}** *submission and* **+{stamina_benefits2[stamina]}** *weekly claim bonus*'

    strength = getStrength(id, BLOCKCHAIN)
    if strength < 6: strength += star
    str_str = f'*gain* **+{strength_benefits[strength]*100}** *additional uwuCreds per submission*'

    dexterity = getDexterity(id, BLOCKCHAIN)
    if dexterity < 6: dexterity += star
    dex_str = f'*gain* **+{dexterity_benefits[dexterity]*100}%** *uwuCreds from clip reviews bonuses*'

    fortune = getFortune(id, BLOCKCHAIN)
    if fortune < 6: fortune += star
    for_str = f'*gain* **+{fortune_benefits[fortune]}** *bonus stacks when claiming weekly bonuses*'

    desc = f'Below lists your current student stats and benefits:\n\n'
    desc += f'**Vitality {vitality}** \u3000 {vit_str}.\n'
    if vitality < 6: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(next upgrade: {vitality_costs[vitality-star+1]})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n'

    desc += f'**Stamina {stamina}** \u3000 {sta_str}.\n'
    if stamina < 6: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(next upgrade: {stamina_costs[stamina-star+1]})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n'

    desc += f'**Strength {strength}** \u3000 {str_str}.\n'
    if strength < 6: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(next upgrade: {strength_costs[strength-star+1]})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n\n'

    desc += f'**Dexterity {dexterity}**\u3000{dex_str}.\n'
    if dexterity < 6: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(next upgrade: {dexterity_costs[dexterity-star+1]})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n\n'

    desc += f'**Fortune {fortune}** \u3000 {for_str}.\n'
    if fortune < 6: desc += f' \u3000  \u3000  \u3000  \u3000  \u3000(next upgrade: {fortune_costs[fortune-star+1]})\n\n'
    else: desc += ' \u3000  \u3000  \u3000  \u3000  \u3000(MAX Level)\n\n'

    desc += f'**Star {star}**\u3000\u3000\u3000{luc_str}. \n\n'

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

    stat, stat_costs = 0, []
    if stat_name == 'Vitality':
        stat = getVitality(id, BLOCKCHAIN)
        stat_costs = vitality_costs
    if stat_name == 'Stamina':
        stat = getStamina(id, BLOCKCHAIN)
        stat_costs = stamina_costs
    if stat_name == 'Strength':
        stat = getStrength(id, BLOCKCHAIN)
        stat_costs = strength_costs
    if stat_name == 'Dexterity':
        stat = getDexterity(id, BLOCKCHAIN)
        stat_costs = dexterity_costs
    if stat_name == 'Fortune':
        stat = getFortune(id, BLOCKCHAIN)
        stat_costs = fortune_costs

    creds = user.totalCreds(id, BLOCKCHAIN)
    # print('%10s %d - %5d' % (stat_name, stat, stamina_costs[stat + 1]))

    if stat >= 6:
        desc = f'Your **{stat_name}** is at its max level, no further upgrades are available.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Level Up - {stat_name}',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    cost = stat_costs[stat+1]
    # print('%s %d - %5d' % (stat_name, stat + 1, cost))

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

    if user.hasWish(id, BLOCKCHAIN) >= 2:
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
    if random.random() < 0.008:
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

    desc = 'Star'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                star += 1
    return star