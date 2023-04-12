import openai
import discord, block, blockchain, random, os

from dotenv import load_dotenv
from commands.helper import today, getIcon

load_dotenv()
GPT_KEY = os.getenv('API_KEY')
PROFESSOR = int(os.getenv('PROFESSOR_ID'))
ADMIN = int(os.getenv('ADMIN_ID'))

openai.api_key = GPT_KEY

async def gpt_string(context, prompt):
    if random.random() < 0.8:
        uwu_prompt = prompt + f' (make it simple and answer in a cute tone with uwu emojis like a tsundere)'
    else: uwu_prompt = prompt + f' (make it simple and answer in a cute tone with murderous emojis like a yandere)'

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": context},
                {"role": 'user', "content": uwu_prompt}
            ]
        )
    except: 
        return "yo mama"

    return response.choices[0].message.content.strip()

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

    yandere_flag = False
    if random.random() < 0.8:
        uwu_prompt = prompt + ' (answer in a cute tone, make sure to insert intersperse "uwu"s and "nyaa"s and emojis like a tsundere)'
        url = professor_icon
        yandere_flag = False
    else:
        uwu_prompt = prompt + ' (answer in a cute tone, make sure to be a little threatening and insert intersperse emojis like a yandere)'
        url = 'https://i.pinimg.com/originals/a2/e5/99/a2e599e7e609db48b6f6c99548844ab7.jpg'
        yandere_flag = True

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
    desc = f'\n\n**Prompt**: \n```{prompt}```\n**Answer**:\n```'

    if yandere_flag: desc += 'ansi\n[2;31m'
    desc += response.choices[0].message.content.strip()
    if yandere_flag: desc += '[0m\n'

    if not id == ADMIN:
        desc += f'```\n\n (*Daily Requests Remaining: {int(15 - 1 - daily_count)}*)'
    else:
        desc += f'```\n\n'

    embed2 = discord.Embed(
        title = f'Professor',
        description = desc,
        color = 6943230    
    # ).set_thumbnail(url=professor_icon)
    ).set_thumbnail(url=url)
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