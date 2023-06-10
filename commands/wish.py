import random, discord, block
import commands.user as user

from commands.helper import today
from commands.manager import pushBlock

async def wish(ctx, mode, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name

    star_pity = getStarPity(id, BLOCKCHAIN)
    item_pity = getItemPity(id, BLOCKCHAIN)
    check = guarenteed(id, BLOCKCHAIN)

    """Check for wish mode"""
    wish_count = user.wishCount(id, BLOCKCHAIN)
    max_iteration = 0
    if mode.lower() == 'single':
        """Check if user has at least 1 wish"""
        if wish_count < 1: 
            embed = discord.Embed(
                title = f'Wish',
                description = f'Insufficient wishes. Require at least 1 wish for a Single Pull. (wish count: {wish_count}).',
                color = 6053215    
            ).set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text='@~ powered by UwUntu')
            await ctx.send(embed=embed)
            return
        else: max_iteration = 1

    elif mode.lower() == 'multi':
        """Check if user has at least 10 wish"""
        if wish_count < 10: 
            embed = discord.Embed(
                title = f'Wish',
                description = f'Insufficient wishes. Require at least 10 wishes for a Multi Pull. (wish count: {wish_count}).',
                color = 6053215    
            ).set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text='@~ powered by UwUntu')
            await ctx.send(embed=embed)
            return
        else: max_iteration = 10

    else:
        embed = discord.Embed(
            title = f'Wish',
            description = f'Please use \'Single\' for 1 pull and \'Multi\' for 10 pulls...',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    items_pulled, scrap_sum = [], 0
    for i in range(max_iteration):
        item = pull(star_pity, item_pity, check)
        item_desc = ', '.join(item)

        """Generate Pull Block"""
        pull_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = item_desc,
            data = 0
        )

        """Generate Item Block"""
        content, server_bonus = 0, user.getServerBonus(BLOCKCHAIN)
        if item[2] == 'Creds': content = 300 * (server_bonus/3 + 1)
        if item[1] == '0*': 
            content = random.randint(10, 25)
            scrap_sum += content
                    
        item_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = item[2],
            data = content
        )

        pushBlock(pull_block, BLOCKCHAIN)
        pushBlock(item_block, BLOCKCHAIN)

        if max_iteration == 1:
            desc, color, gif = '', -1, ''
            if item[1] == '5*':
                desc = f'Holy ****! A Star Descends! (You got 1x{text2Emoji(item[2])})'
                color = 16700447
                gif = 'https://media.tenor.com/Z5kE_QEkGdgAAAAC/roll-wishing.gif'
            elif item[1] == '4*':
                desc = f'You reached for the Stars, and found something! (You got 1x{text2Emoji(item[2])})'
                color = 10027263
                gif = 'https://media.tenor.com/8OqlJIRATS0AAAAC/wishing-genshin.gif'
            else:
                desc = f'You reached for the Stars, but they were too far. (You got {content} creds)'
                color = 6053215
                gif = 'https://media0.giphy.com/media/nWPLGmsjvdQ4g/giphy.gif'

            """Return Message"""
            embed = discord.Embed(
                title = 'Daily',
                description = desc,
                color = color    
            ).set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text='@~ powered by UwUntu, sponsored by Dre\'s tears')
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
        else:
            items_pulled.append(item)
    
    """Get highest rarity"""
    desc, color, gif = '', -1, ''
    rarity = getHighestRarity(items_pulled)

    if rarity == '5*':
        color = 16700447
        gif = 'https://media.tenor.com/Z5kE_QEkGdgAAAAC/roll-wishing.gif'
    elif rarity == '4*':
        color = 10027263
        gif = 'https://media.tenor.com/8OqlJIRATS0AAAAC/wishing-genshin.gif'
    else:
        color = 6053215
        gif = 'https://media0.giphy.com/media/nWPLGmsjvdQ4g/giphy.gif'

    """Push Scrap Creds to Block"""
    scrap_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Scrap Sum',
        data = scrap_sum
    )

    pushBlock(scrap_block, BLOCKCHAIN)

    inventory = getInventory(items_pulled)
    desc = f'You reached for the Stars... and got {inventory}. (also {scrap_sum} creds)'

    """Return Message"""
    embed = discord.Embed(
        title = 'Daily',
        description = desc,
        color = color    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu, sponsored by Dre\'s tears')
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

def getInventory(item_list) -> str:
    inventory = ''
    items = ['Creds', 'Torn Ticket', 'Bonus Submit', 'Reforger', 'Star', 'Dark Star']

    for i in items:
        item_count = 0
        for j in item_list:
            if i == j: item_count += 1
        
        if item_count == 0: continue

        inventory += f'{item_count}x{text2Emoji(i)}'

        if i == 'Dark Star': continue
        else: inventory += ', '

    return inventory

def text2Emoji(item):
    if item == 'Creds': return '💰'
    if item == 'Torn Ticket': return '🎫'
    if item == 'Bonus Submit': return '🎞️'
    if item == 'Reforger': return '🔨'
    if item == 'Star': return '⭐'
    if item == 'Dark Star': return '💥'

def getHighestRarity(item_list) -> str:
    unique_list = []
    for i in item_list:
        unique_list.append(item_list[i][1])
    unique_list = list(set(unique_list))

    if '5*' in unique_list: return '5*'
    elif '4' in unique_list: return '4*'
    else: return '0*'

def randomItem() -> str:
    items = ['Creds', 'Torn Ticket', 'Bonus Submit', 'Reforger']
    index = random.randint(0, len(items)-1)

    return items[index]

def pull(total_pity, pity, guarenteed) -> list:
    
    # 5* probability check -------------------------------------
    item = None
    if total_pity < 74:
        if random.random() < 0.006:
            # Hit the 5*, WOOOT
            if random.random() < 0.5 or guarenteed:
                item = ['Pull', '5*', 'Star']
            else:
                item = ['Pull', '5*', 'Dark Star']
        
    if total_pity >= 74:
        if random.random() < 0.06:
            # Hit the 5*, less WOOOT
            if random.random() < 0.5 or guarenteed:
                item = ['Pull', '5*', 'Star']
            else:
                item = ['Pull', '5*', 'Dark Star']

    if total_pity == 89:
        # Hit the 5*, fucking hell
        if random.random() < 0.5 or guarenteed:
            item = ['Pull', '5*', 'Star']
        else:
            item = ['Pull', '5*', 'Dark Star']

    if item is not None:
        return item

    # 4* probability check -------------------------------------
    if pity < 8:
        if random.random() < 0.051:
            # Hit the 4*, WOOOT
            if random.random() < 0.5:
                item = ['Pull', '4*', 'Token']
            else:
                item = ['Pull', '4*', randomItem()]

    if pity == 8:
        if random.random() < 0.561:
            # Hit the 4*, less WOOOT
            if random.random() < 0.5:
                item = ['Pull', '4*', 'Token']
            else:
                item = ['Pull', '4*', randomItem()]

    if pity > 8:
        # Hit the 4*, fucking hell
        if random.random() < 0.5:
            item = ['Pull', '4*', 'Token']
        else:
            item = ['Pull', '4*', randomItem()]

    if item is not None:
        return item
    else:
        return ['Pull', '0*', '']

"""Pull Block Desc ---> Pull, 5*, Star """
def getStarPity(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc1, desc2, desc3, total_pity = '5*', '4*', '0*', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if len(block.getDesc().split(', ')) == 3:
                rarity = block.getDesc().split(', ')[1]

                if rarity == desc1:
                    total_pity = 0
                elif rarity == desc2:
                    total_pity += 1
                elif rarity == desc3:
                    total_pity += 1
                else: continue
                        
    return total_pity

def getItemPity(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc1, desc2, desc3, item_pity = '5*', '4*', '0*', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if len(block.getDesc().split(', ')) == 3:
                rarity = block.getDesc().split(', ')[1]

                if rarity == desc1:
                    item_pity = 1
                elif rarity == desc2:
                    item_pity += 0
                elif rarity == desc3:
                    item_pity += 1
                else: continue
                        
    return item_pity

def guarenteed(user_id, BLOCKCHAIN) -> bool:
    if len(BLOCKCHAIN.chain) == 1: return False

    guarenteed, desc1, desc2 = False, '5*', 'Dark Star'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if len(block.getDesc().split(', ')) == 3:
                if block.getDesc().split(', ')[1] == desc1:
                    if block.getDesc().split(', ')[2] == desc2:
                        guarenteed = True
                    else:
                        guarenteed = False
    
    return guarenteed