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
MODERATOR1 = int(os.getenv('VHCHENG'))

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
        cred_status = 'oof...'
    if luck > 550 and luck <= 850: 
        cred_amount = random.randint(250, 350)
        cred_status = 'Ok not bad,'
    if luck > 850 and luck <= 950: 
        cred_amount = random.randint(400, 500)
        cred_status = 'Super Pog,'
    if luck > 950 and luck <= 1000:
        cred_amount = random.randint(501, 600)
        cred_status = 'p-Pog master,'
    if luck == 1001:
        cred_amount = 1000
        cred_status = 'RNJesus has blessed you, '

    api.addCreds(id, cred_amount)
    api.updateDaily(id, today)

    user_name = api.fetchName(id)
    if user_name != name:
        api.updateName(id, name)
   
    await ctx.send(
        f'{cred_status} **+{cred_amount}** creds were added to your collection'
    )

async def getCreds (ctx):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()
    
    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_name = api.fetchName(id)
    if user_name != name:
        api.updateName(id, name)

    user_creds = api.fetchCreds(id)
    await ctx.send(
        f'You have a total of **{user_creds}** uwuCreds!'
    )


async def purchase (ctx):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    cred_cost = 0
    if ctx.name == 'paper': cred_cost = 500
    if ctx.name == 'iron': cred_cost = 1000
    if ctx.name == 'bronze': cred_cost = 5000
    if ctx.name == 'silver': cred_cost = 7000
    if ctx.name == 'gold': cred_cost = 12000
    if ctx.name == 'platinum': cred_cost = 20000
    if ctx.name == 'ticket':
        user_tickets = int(api.fetchTicket(id))
        cred_cost = 2000 + 400*(user_tickets)

    if ctx.name == 'ticket':
        user_tickets = api.fetchTicket(id)
        if int(user_tickets) == 10:
            await ctx.send(
                f'You already have reached the max amount of tickets! (10/10)'
            )
            return

    user_creds = api.fetchCreds(id)
    if user_creds - cred_cost > 0:
        api.subCreds(id, cred_cost)
        user_creds = api.fetchCreds(id)

        if ctx.name == 'ticket':
            api.buyTicket(id)
            user_tickets = api.fetchTicket(id)
            await ctx.send(
                f'You have purchased the a raffle **{ctx.name}** for {cred_cost}!   (remaining: {user_creds})' +
                f'\n You now have {user_tickets} ticket(s)'
            )
            return

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

def getTime():
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    today = today.strftime('%m-%d-%y %H:%M')
    yesterday = yesterday.strftime('%m-%d-%y %H:%M')

    return today, yesterday

async def handout(ctx, receiver, amount, client):
    if amount > 3000:
        await ctx.send(f'dO nOt AbUsE tHy PoWeR1!1!')
        return

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
        receive_db = api.fetchUser(receive_id)
        if len(receive_db) == 0:
            receive_object = await client.fetch_user(receive_id)
            receive_name = receive_object.name
            api.createAccount(receive_id, receive_name, yesterday)
        api.addCreds(receive_id, amount)
        newUwU = api.fetchCreds(receive_id)
        await ctx.send(f'Moderator <@{giver_id}> has graced <@{receive_id}> with {amount} uwuCreds!' +
                       f'\n<@{receive_id}> now has {newUwU}')
        await ctx.send()
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')

async def uwuTax(ctx, victim, amount, client):
    if amount > 1000:
        await ctx.send(f'dO nOt AbUsE tHy PoWeR1!1!')
        return

    today, yesterday = getTime()
    filler = ['<', '>', '!', '@']

    mod_id = ctx.author.id
    victim_id = victim
    for ch in filler:
        victim_id = victim_id.replace(ch, '')
    victim_id = int(victim_id)

    mod_db = api.fetchUser(mod_id)
    mod_name = ctx.author.name
    if len(mod_db) == 0: 
        api.createAccount(mod_id, mod_name, yesterday)
        await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')
        return 

    # check if user is a moderator
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        victim_db = api.fetchUser(victim_id)
        if len(victim_db) == 0:
            victim_object = await client.fetch_user(victim_id)
            victim_name = victim_object.name
            api.createAccount(victim_id, victim_name, yesterday)
        api.subCreds(victim_id, amount)
        newUwU = api.fetchCreds(victim_id)
        await ctx.send(f'Moderator <@{mod_id}> has taken {amount} uwuCreds! from <@{victim_id}>' +
                       f'\n<@{victim_id}> now has {newUwU}')
        await ctx.send()
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')

async def spy (ctx, target):
    today, yesterday = getTime()

    filler = ['<', '>', '!', '@']

    target_id = target
    for ch in filler:
        target_id = target_id.replace(ch, '')
    target_id = int(target_id)
    
    user = api.fetchUser(target_id)
    if len(user) == 0: ctx.reply(f'Target does not exist or has not UwUed')

    user_creds = api.fetchCreds(target_id)
    await ctx.send(
        f'The target has a total of **{user_creds}** uwuCreds'
    )

async def clearDatabase (ctx):
    id = ctx.author.id

    if id == ADMIN: 
        remove = api.removeUsers()
        await ctx.send(f'All users have been cleared')
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')