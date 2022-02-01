import discord, block, blockchain
import commands.user as user

from commands.helper import today, getWeight

filler = ['<', '>', '!', '@']
        
"""Allow users to submit a Valorant game to earn uwuCreds"""
async def getLolScore(ctx, k, d, a, cs, time, wards, submit, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user submissions will be checked
       2. Blockchain will be evaluated, recent submissions will be averaged
       3. Blockchain will be validated, new block will be added to the end of Blockchain"""
    id, name = ctx.author.id, ctx.author.name
    color, nd = 6053215, d

    """check if the user has submissions left"""
    user_subs = user.totalSubsToday(id, BLOCKCHAIN)
    if user_subs >= 3 and submit == True:
        embed = discord.Embed(
            title = f'Submission',
            description = f'Out of Submissions, it now resets based on date!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by oogway desu')
        await ctx.send(embed=embed)
        return
    
    """calculate uwuScore, check for divide by zero"""
    if d <= 0: d = 1 # prevent scaling above 800
    kda, game = (k + a) / d, time / 30  
    score = int(kda*game*10 + cs + 3*wards)
    
    """fetch and calculate user average/score weight"""
    final_score, average = 0, user.averageLScore(id, BLOCKCHAIN)
    if average == -1: final_score = score
    else:
        weight = getWeight(average, score)
        if score > average: final_score = int(score + 0.666*score*weight)
        else: final_score = int(score - 1.5*score*weight)
        
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
                description = 'Submission L',
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
        desc = 'League Game Stats:\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\n\n'
        desc += f'KDA: \u3000**{k}**/**{nd}**/**{a}**\u3000\u3000CS: \u3000\u3000**{cs}**\n\n'
        desc += f'Calculated Score: \u3000**{final_score}**'
        embed = discord.Embed(
            title = f'Submission',
            description = desc,
            color = color    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by oogway desu')
        message_to_pin = await ctx.send(embed=embed)   
 
        if submit: await message_to_pin.pin()