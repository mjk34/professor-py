import openai
import discord, block, blockchain, random, os

from dotenv import load_dotenv
from commands.helper import today, getIcon

load_dotenv()
GPT_KEY = os.getenv('API_KEY')
PROFESSOR = int(os.getenv('PROFESSOR_ID'))
ADMIN = int(os.getenv('ADMIN_ID'))

openai.api_key = GPT_KEY

"""Allow users to use Davinci API to Generate responses"""
async def gpt(ctx, prompt, client, BLOCKCHAIN):

    id, name = ctx.author.id, ctx.author.name
    professor_icon = await getIcon(PROFESSOR, client)

    daily_count = getGPTCount(id, BLOCKCHAIN)
    if daily_count > 15 and not id == ADMIN:
        embed = discord.Embed(
            title = f'Professor',
            description = f'Class dismissed, you\'ve reached the maximum amount of requests. Try again tomorrow.',
            color = 6053215    
        ).set_thumbnail(url=professor_icon)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
    
    embed1 = discord.Embed(
        title = f'Professor',
        description = "Cogitating...",
        color = 6943230    
    ).set_thumbnail(url=professor_icon)
    embed1.set_footer(text='@~ powered by UwUntu')
    thinking = await ctx.send(embed=embed1)

    uwu_prompt = prompt + ' (answer in a cute tone, make sure to insert intersperse "uwu"s and "nyaa"s and ascii emojis and emoji like a tsundere)'
    # ' (answer in a cute tone, inserting random "uwu"s, as a personified cat)'
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{
                "role": "assistant",        
                "content": uwu_prompt
            }]
        )
    except: 
        embed = discord.Embed(
            title = f'Professor',
            description = f'Sorry I was sleeping... try again.',
            color = 6053215    
        ).set_thumbnail(url=professor_icon)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    # print(response.choices[0].message.content.strip())

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

    user = f'<@{id}>'
    desc = f'\n\n**Prompt**: \n{user}: {prompt}\n\n**Answer**:\n'
    desc += response.choices[0].message.content.strip()

    if not id == ADMIN:
        desc += f'\n\n (*Daily Requests Remaining: {int(15 - 1 - daily_count)}*)'

    embed2 = discord.Embed(
        title = f'Professor',
        description = desc,
        color = 6943230    
    ).set_thumbnail(url=professor_icon)
    embed2.set_footer(text='@~ powered by UwUntu')

    await thinking.edit(embed=embed2)
    
    return

def getGPTCount(user_id, BLOCKCHAIN):
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, count = 'GPT', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc and block.getTime() == today():
                count += 1
    return count