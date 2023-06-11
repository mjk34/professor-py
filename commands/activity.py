import block, discord

from commands.helper import today
from commands.manager import pushBlock

level_xp = [0, 5, 25, 75, 150, 300, 600, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
level_wish = [0, 1, 2, 3, 5, 5, 5, 10, 10, 10, 10, 10, 10, 20, 20, 20]

def messageXP(id, name, ACTIVCHAIN, BLOCKCHAIN):
    current_xp = getLevelXP(id, ACTIVCHAIN)
    next_level = getLevel(id, ACTIVCHAIN) + 1
    embed_message = None
    
    """Generate XP Block"""
    xp_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'XP',
        data = 5
    )

    """Update ACTIVCHAIN"""
    pushBlock(xp_block, ACTIVCHAIN)

    """Check Level Up"""
    if next_level == 16: return
    if levelUp(current_xp, next_level):

        """Generate LEVEL BLOCK"""
        level_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'LEVEL',
            data = 0
        )

        """Generate Wish BLOCK"""
        wish_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'Wish',
            data = 0
        )

        pushBlock(level_block, ACTIVCHAIN)
        for i in range(level_wish[next_level]):
            pushBlock(wish_block, BLOCKCHAIN)

        """Return Message"""
        embed_message = discord.Embed(
            title = 'Activity',
            description = f'GG <@{id}>, your participation Level just advanced to **Level {next_level}**! (+{level_wish[next_level]} Wish)',
            color = 16777215    
        )
        embed_message.set_footer(text='@~ powered by UwUntu')

    return levelUp(current_xp, next_level), embed_message


def levelUp(current_xp, next_level) -> bool:
    if current_xp + 5 >= level_xp[next_level]:
        return True
    else:
        return False

def getLevelXP(user_id, ACTIVCHAIN) -> int:
    if len(ACTIVCHAIN.chain) == 1: return 0

    desc1, desc2, total = 'XP', 'LEVEL', 0
    for block in ACTIVCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc2:
                total = 0
                continue
            if block.getDesc() == desc1:
                total += block.getData()

    return total

def getLevel(user_id, ACTIVCHAIN) -> int:
    if len(ACTIVCHAIN.chain) == 1: return 0

    desc, level = 'LEVEL', 0
    for block in ACTIVCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                level += 1
    
    return level