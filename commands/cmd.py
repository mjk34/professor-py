import random, discord
from commands.helper import fetchContentList, fetchContent, dailyFortune

"""Checks uwuBot's response to see if it is available"""
async def ping(ctx):
    images = fetchContentList('pong.txt')
    num = random.randint(0, 22)
    embed = discord.Embed(
        title = f'Pong!',
        color = 16251130
    ).set_image(url= images[num])
    embed.set_footer(text='@~ powered by oogway desu')
    
    await ctx.send(embed=embed)

"""Requests for a link to Anichart to see the in season running anime"""
async def anime (ctx):
    content, f = fetchContent('anichart.txt')
    embed = discord.Embed(
        title = f'Current Anime',
        url = 'https://anilist.co/search/anime/this-season',
        description = content,
        color = 6943230
    ).set_thumbnail(url = 'https://pbs.twimg.com/profile_images/1236103622636834816/5TFL-AFz_400x400.png')
    embed.set_footer(text='@~ powered by oogway desu')

    await ctx.send(embed=embed)
    f.close()
    
"""Reqests a reading from fortune api"""
async def fortune (ctx):
    name = ctx.author.name

    orb_url = 'https://i.imgur.com/1icMQHf.jpg'
    if random.random() < 0.5:
        PONDER_LIST = fetchContentList('ponder.txt')
        index = random.randint(0, len(PONDER_LIST)-1)
        orb_url = PONDER_LIST[index]

    read = ''
    read += dailyFortune()
    
    embed = discord.Embed(
        title = f'{name}\'s Fortune',
        description = read,
        color = 16251130
    ).set_image(url=orb_url)
    embed.set_footer(text='@~ powered by oogway desu')
    
    await ctx.send(embed=embed)
    
"""Converts input text with u and o syllabols and sprinkle in text emojis"""
def uwuify(text: str) -> str:
    uwu_emojis = [
        'ಇ( ꈍᴗꈍ)ಇ', '( ͡o ꒳ ͡o )', '(ó ꒳ ò✿)',
        '(ㅅꈍ ˘ ꈍ)', '(*ฅ́˘ฅ̀*)', ' (◡‿◡✿)',
        '(◠‿◠✿)', '(❦ ᴗ ❦ ✿)', '(ᅌ ˇ ᅌ✿)'
    ]

    output_text = '`*:･ﾟ✧ '

    if random.random() < 0.15:
        num = random.randint(0, 8)
        output_text += uwu_emojis[num] + ' '

    length = len(text)
    for i in range(length):
        c_char = text[i]
        p_char = text[i-1] if i > 0 else None

        if c_char == ' ':
            if random.random() < 0.15:
                num = random.randint(0, 8)
                output_text += ' ' + uwu_emojis[num] + ' '
            else: output_text += c_char
            continue

        if c_char == 'L'  and p_char != ' ' or c_char == 'R' and p_char != ' ':
            output_text += 'W'
        elif c_char == 'l'  and p_char != ' ' or c_char == 'r' and p_char != ' ':
            output_text += 'w'

        elif c_char == 'O' or c_char == 'o':
            check_list = ['N', 'n', 'K', 'k', 'G', 'g', 'M', 'm']
            if p_char in check_list:
                output_text += 'yo'
            else: output_text += c_char

        elif c_char == 'A' or c_char == 'a':
            check_list = ['N', 'n', 'K', 'k', 'G', 'g', 'M', 'm']
            if p_char in check_list:
                output_text += 'ya'
            else: output_text += c_char

        else:
            output_text += c_char
    
    output_text += ' ✧･ﾟ:*\n`'
    return str(output_text)

if __name__ == "__main__":
    test1 = "The quick brown fox jumps over the lazy dog."
    test2 = "Oh! Nooo! I was late for work!"

    print(uwuify(test1).encode('utf-8').decode('ascii', 'ignore'))
    print(uwuify(test2).encode('utf-8').decode('ascii', 'ignore'))