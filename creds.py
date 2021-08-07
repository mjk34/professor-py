import random
import discord
import API.API
import os
import threading

from dotenv import load_dotenv
from datetime import date, timedelta, datetime
from dateutil import parser
from discord.utils import get

api = API.API
load_dotenv()
ADMIN = int(os.getenv('ADMIN_ID'))

async def checkBirthday(guild, client):
    hour_time = 3600
    threading.Timer(hour_time, checkBirthday, guild).start()

    now = datetime.now()
    current_time = now.strftime("%H")

    if current_time == '08':
        today = datetime.now()
        today = today.strftime('%m-%d')

        birthday_id = api.birthdayToday(today)
        if birthday_id != None:

            channels = guild.channels
            msg_channel = None
            for ch in channels:
                msg_channel = ch
                if msg_channel.name == 'bot-cmd': break
            
            num = random.randint(1, 23)
            filename = f'./birthday/{num}.jpg'
            f = open(filename, 'rb')

            await client.get_channel(msg_channel.id).send(
                f'We don\'t grow old. When we cease to grow, we become old. Happy Birthday <@{birthday_id}>!', file=discord.File(f)
            )
            f.close()

async def daily (ctx):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()
    
    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_daily = api.fetchDaily(id)
    today_parse = parser.parse(today)
    daily_parse = parser.parse(user_daily)

    time_diff = today_parse - daily_parse
    wait = timedelta(hours=20) - time_diff

    if time_diff < timedelta(hours= 20):
        await ctx.send(f'Next **/uwu** resets in **{wait}**')
        return

    luck = random.randint(1, 1001)
    cred_amount, cred_status = 0, ''

    if luck <= 550: 
        cred_amount = random.randint(50, 200)
        cred_status = 'Meh,'
    if luck > 550 and luck <= 850: 
        cred_amount = random.randint(250, 350)
        cred_status = 'Feeling good,'
    if luck > 850 and luck <= 950: 
        cred_amount = random.randint(400, 500)
        cred_status = 'Rare find,'
    if luck > 950 and luck <= 1000:
        cred_amount = random.randint(501, 600)
        cred_status = 'You\'re super lucky,'
    if luck == 1001:
        cred_amount = 1000
        cred_status = 'RNJesus has blessed you, '

    api.addCreds(id, cred_amount)
    api.updateDaily(id, today)
    
    await ctx.send(
        f'{cred_status} **+{cred_amount}** creds were added to your collection'
    )

async def getCreds (ctx):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()
    
    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_creds = api.fetchCreds(id)
    await ctx.send(
        f'You have a total of **{user_creds}** uwuCreds!'
    )

async def getBd (ctx):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_bd = api.fetchBirthday(id)
    if user_bd == '':
        await ctx.send(
            f'You have not registered your birthday! Use **/setbd** to assign one'
        )
    else:
        await ctx.author.send(
            f'The saved birthday date is: **{user_bd}**'
        )
        await ctx.send(f'*uwu*')
        await ctx.message.delete()
    

async def purchase (ctx):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)
    
    cred_cost = 0
    if ctx.name == 'paper': cred_cost = 300
    if ctx.name == 'iron': cred_cost = 500
    if ctx.name == 'bronze': cred_cost = 1000
    if ctx.name == 'silver': cred_cost = 2000
    if ctx.name == 'gold': cred_cost = 5000
    if ctx.name == 'platinum': cred_cost = 10000

    user_creds = api.fetchCreds(id)
    if user_creds - cred_cost > 0:
        api.subCreds(id, cred_cost)
        user_creds = api.fetchCreds(id)

        message_to_pin = await ctx.send(
            f'You have purchased the **{ctx.name}** tier reward!   (total: {user_creds})'
        )
        await message_to_pin.pin()
    else:
        await ctx.send(
            f'The **{ctx.name}** tier requires **{cred_cost}** uwuCreds...   (you have: {user_creds})'
        )

async def give (ctx, receive, amount, client):
    today, yesterday = getTime()

    filler = ['<', '>', '!', '@']

    giver_id = ctx.author.id
    receive_id = receive
    for ch in filler:
        receive_id = receive_id.replace(ch, '')
    receive_id = int(receive_id)

    giver_db = api.fetchUser(giver_id)
    giver_name = ctx.author.name
    if len(giver_db) == 0: api.createAccount(giver_id, giver_name, yesterday)
    
    giver_creds = api.fetchCreds(giver_id)
    if giver_creds < amount:
        await ctx.send(
            f'You do not have that much uwuCreds to give.   (total: {giver_creds})'
        )
        return

    receive_db = api.fetchUser(receive_id)
    if len(receive_db) == 0:
        receive_object = await client.fetch_user(receive_id)
        receive_name = receive_object.name
        api.createAccount(receive_id, receive_name, yesterday)

    if amount > 0:
        api.subCreds(giver_id, amount)
        api.addCreds(receive_id, amount)
    
    await ctx.send(
        f'**{amount}** uwuCreds was given to <@{receive_id}>!'
    )

async def clearDatabase (ctx):
    id = ctx.author.id

    if id == ADMIN: 
        remove = api.removeUsers()
        await ctx.send(f'All users have been cleared')
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')

async def setBirthday(ctx, birth_date):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    birthday = parser.parse(birth_date)
    birthday = birthday.strftime('%m-%d')

    api.updateBirthday(id, birthday)
    role = get(ctx.guild.roles, name='uwuCelebrate')

    await ctx.author.add_roles(role)
    await ctx.author.send(f'Birthday is set to: **{birthday}**')

    await ctx.send(f'*uwu*')
    await ctx.message.delete()

def getTime():
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    today = today.strftime('%m-%d-%y %H:%M')
    yesterday = yesterday.strftime('%m-%d-%y %H:%M')

    return today, yesterday

async def handout(ctx, receiver, amount, client):
    today, yesterday = getTime()

    filler = ['<', '>', '!', '@']

    giver_id = ctx.author.id
    receive_id = receiver
    for ch in filler:
        receive_id = receive_id.replace(ch, '')
    receive_id = int(receive_id)

    giver_db = api.fetchUser(giver_id)
    giver_name = ctx.author.name
    if len(giver_db) == 0: 
        api.createAccount(giver_id, giver_name, yesterday)
        await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')
        return 

    # check if user is a moderator
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        await ctx.send(f'<@{giver_id}> is a Moderator')

        receive_db = api.fetchUser(receive_id)
        if len(receive_db) == 0:
            receive_object = await client.fetch_user(receive_id)
            receive_name = receive_object.name
            api.createAccount(receive_id, receive_name, yesterday)
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')