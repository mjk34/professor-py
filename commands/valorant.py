import discord, block, blockchain
import commands.user as user

from commands.helper import today

filler = ['<', '>', '!', '@']
        
"""Allow users to submit a Valorant game to earn uwuCreds"""
async def getValScore(ctx, k, d, a, adr, head, rounds, submit, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user submissions will be checked
       2. Blockchain will be evaluated, recent submissions will be averaged
       3. Blockchain will be validated, new block will be added to the end of Blockchain"""
    id, name = ctx.author.id, ctx.author.name
    color, nd = 6053215, d

    """check if the user has submissions left"""
    user_subs = user.totalSubsWeek(id, BLOCKCHAIN)
    if 3 - user_subs <= 0 and submit == True:
        embed = discord.Embed(
            title = f'Submission',
            description = f'Out of Submissions, it now resets based on date!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by oogway desu')
        await ctx.send(embed=embed)
        return
    
    """calculate uwuScore, check for divide by zero"""
    if d <= 3: d = 3
    kda, game = (k + 0.5*a) / d, (rounds / 25)  
    score = int(kda*game*(adr + 3*head))
        
    if score < 0:
        text = f'Mr. Stark... I don\'t feel so good... (calculated: {score})'
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
                description = 'Submission',
                data = score
            )
            
            """Update Blockchain"""
            if BLOCKCHAIN.isChainValid() == False:
                print('The current Blockchain is not valid, performing rollback.')
                BLOCKCHAIN = blockchain.Blockchain()
        
            BLOCKCHAIN.addBlock(new_block)
            if BLOCKCHAIN.isChainValid():
                BLOCKCHAIN.storeChain()           
            
        """Return Message"""
        desc = 'Valorant Game Stats:\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\n\n'
        desc += f'KDA: \u3000**{k}**/**{nd}**/**{a}**\u3000\u3000ADR: \u3000\u3000\u3000**{adr}**\nHEAD:\u3000**{head}** \u3000\u3000\u3000\u3000ROUNDS: \u3000**{rounds}**\n\n'
        desc += f'Calculated Score: \u3000**{score}**'
        embed = discord.Embed(
            title = f'Submission',
            description = desc,
            color = color    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by oogway desu')
        message_to_pin = await ctx.send(embed=embed)   
 
        if submit: await message_to_pin.pin()