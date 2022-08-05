import discord, block, blockchain
import commands.user as user

from commands.helper import today, getWeight

filler = ['<', '>', '!', '@']
        
"""Allow users to submit a Valorant game to earn uwuCreds"""
async def getValScore(ctx, acs, submit, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user submissions will be checked
       2. Blockchain will be validated, new block will be added to the end of Blockchain"""
    id, name = ctx.author.id, ctx.author.name
    color = 6053215

    if submit == 'view': submit = False
    elif submit == 'submit': submit = True
    else: submit = True

    """check if the user has submissions left"""
    user_subs = user.totalSubsToday(id, BLOCKCHAIN)
    if user_subs >= 3 and submit == True:
        embed = discord.Embed(
            title = f'Submission',
            description = f'Out of Submissions, it now resets based on date!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by oxygen tax')
        await ctx.send(embed=embed)
        return
    
    """calculate uwuScore, check for divide by zero"""
    if   acs < 150: score = int(acs*1.30)
    elif acs < 250: score = int(acs*1.25)
    else:           score = int(acs*1.20)
    
    """fetch and calculate user average/score weight"""
    final_score, average = 0, int(user.averageVScore(id, BLOCKCHAIN))
    if average == -1: final_score = score
    else:
        weight = getWeight(average, score)
        if score > (average - 50): final_score = int(score + 1.25*score*weight)
        else: final_score = int(score - 1.15*score*weight)
        
    if final_score < 0:
        text = f'Mr. Stark... I don\'t feel so good... (calculated: {final_score})'
        await ctx.send(f'```CSS\n[{text}]\n```')
        return
    else:  
        if submit == True:
            color = 2352682
            
            """Generate new Block"""
            new_block = block.Block(
                user = id,
                name = name,
                timestamp = today(),
                description = 'Submission V',
                data = final_score
            )
            
            """Update Blockchain"""
            if BLOCKCHAIN.isChainValid() == False:
                print('The current Blockchain is not valid, performing rollback.')
                BLOCKCHAIN = blockchain.Blockchain()
        
            BLOCKCHAIN.addBlock(new_block)
            if BLOCKCHAIN.isChainValid():
                BLOCKCHAIN.storeChain()           
            
        """Return Message"""
        desc = 'Valorant Game:\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\n\n'
        desc += f'Name: \u3000**{name}**\u3000\u3000Average: \u3000**{average}**\n\n'
        desc += f'Calculated Score: \u3000**{final_score}**'
        embed = discord.Embed(
            title = f'Submission',
            description = desc,
            color = color    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by oxygen tax')
        message_to_pin = await ctx.send(embed=embed)   
 
        if submit: await message_to_pin.pin()