import openai
import discord, block, blockchain, random, os

from dotenv import load_dotenv
from commands.helper import today, getIcon

load_dotenv()
GPT_KEY = os.getenv('API_KEY')
PROFESSOR = int(os.getenv('PROFESSOR_ID'))

openai.api_key = GPT_KEY

"""Allow users to use Davinci API to Generate responses"""
async def gpt(ctx, prompt, client, BLOCKCHAIN):

    id, name = ctx.author.id, ctx.author.name
    professor_icon = await getIcon(PROFESSOR, client)

    daily_count = getGPTCount(id, BLOCKCHAIN)
    if daily_count > 15:
        embed = discord.Embed(
            title = f'ProfessorGPT',
            description = f'Class dismissed, you\'ve reached the maximum amount of requests. Try again tomorrow.',
            color = 6053215    
        ).set_thumbnail(url=professor_icon)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5
    )

    """Generate new Block"""
    gpt_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'GPT',
        data = 0
    )

    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(gpt_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()   

    desc = f'**Prompt**: \"{prompt}\"\n\n**Answer**:\n```'
    desc += response.choices[0].text.strip()
    desc += f'```\n\n (*Daily Requests Remaining: {int(15 - 1 - daily_count)}*)'
    embed = discord.Embed(
        title = f'ProfessorGPT',
        description = desc,
        color = 6943230    
    ).set_thumbnail(url=professor_icon)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
    return

def getGPTCount(user_id, BLOCKCHAIN):
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, count = 'GPT', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc and block.getTime() == today():
                count += 1
    return count