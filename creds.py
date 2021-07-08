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

async def daily (message):
    id = message.author.id
    name = message.author.name
    today, yesterday = getTime()
    
    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_daily = api.fetchDaily(id)
    today_parse = parser.parse(today)
    daily_parse = parser.parse(user_daily)

    time_diff = today_parse - daily_parse
    wait = timedelta(hours=20) - time_diff

    if time_diff < timedelta(hours= 20):
        await message.reply(f'Next >uwu resets in **{wait}**')
        return

    luck = random.randint(1, 100)
    cred_amount, cred_status = 0, ''

    if luck <= 75: 
        cred_amount = random.randint(50, 250)
        cred_status = 'Meh,'
    if luck > 75 and luck <= 90: 
        cred_amount = random.randint(150, 350)
        cred_status = 'Feeling good,'
    if luck > 90 and luck <= 99: 
        cred_amount = random.randint(300, 450)
        cred_status = 'Rare find,'
    if luck == 100:
        cred_amount = random.randint(400, 500)
        cred_status = 'You\'re super lucky,'

    api.addCreds(id, cred_amount)
    api.updateDaily(id, today)
    
    await message.reply(
        f'{cred_status} **+{cred_amount}** creds were added to your collection'
    )

async def getCreds (message):
    id = message.author.id
    name = message.author.name
    today, yesterday = getTime()
    
    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_creds = api.fetchCreds(id)
    await message.reply(
        f'You have a total of **{user_creds}** uwuCreds!'
    )

async def purchase (message, tier):
    id = message.author.id
    name = message.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)
    
    cred_cost = 0
    if tier == 'bronze': cred_cost = 1000
    if tier == 'silver': cred_cost = 2000
    if tier == 'gold': cred_cost = 5000
    if tier == 'platinum': cred_cost = 10000

    user_creds = api.fetchCreds(id)
    if user_creds - cred_cost > 0:
        api.subCreds(id, cred_cost)
        user_creds = api.fetchCreds(id)

        message_to_pin = await message.reply(
            f'You have purchased the **{tier}** tier reward!   (total: {user_creds})'
        )
        await message_to_pin.pin()
    else:
        await message.reply(
            f'The **{tier}** tier requires **{cred_cost}** uwuCreds...   (you have: {user_creds})'
        )

async def give (message, msg_str, client):
    today, yesterday = getTime()

    filler = ['<', '>', '!', '@']
    message_content = msg_str.split(' ')

    giver_id = message.author.id
    amount = int(message_content[2])

    reciever_id = message_content[1]
    for ch in filler:
        reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

    giver_db = api.fetchUser(giver_id)
    giver_name = message.author.name
    if len(giver_db) == 0: api.createAccount(giver_id, giver_name, yesterday)
    
    giver_creds = api.fetchCreds(giver_id)
    if giver_creds < amount:
        await message.reply(
            f'You do not have that much uwuCreds to give.   (total: {giver_creds})'
        )
        return

    reciever_db = api.fetchUser(reciever_id)
    if len(reciever_db) == 0:
        reciever_object = await client.fetch_user(reciever_id)
        reciever_name = reciever_object.name
        api.createAccount(reciever_id, reciever_name, yesterday)

    if amount > 0:
        api.subCreds(giver_id, amount)
        api.addCreds(reciever_id, amount)
    
    await message.reply(
        f'**{amount}** uwuCreds was given to <@{reciever_id}>!'
    )

async def clearDatabase (message):
    id = message.author.id

    if id == ADMIN: 
        remove = api.removeUsers()
        await message.reply(f'All users have been cleared')
    else: await message.reply(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')

async def setBirthday(message):
    id = message.author.id
    name = message.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    birthday = message.content.lower()[7:]
    birthday = parser.parse(birthday)
    birthday = birthday.strftime('%m-%d')

    api.updateBirthday(id, birthday)
    role = get(message.guild.roles, name='uwuCelebrate')

    await message.author.add_roles(role)
    await message.reply(f'Birthday is set to: {birthday}')

def getTime():
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    today = today.strftime('%m-%d-%y %H:%M')
    yesterday = yesterday.strftime('%m-%d-%y %H:%M')

    return today, yesterday
