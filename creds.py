import API.API, os

from dotenv import load_dotenv
from discord.utils import get

from helper import dailyLuck, getTime, lessThan24HRs, timeWait, timeDiff
from helper import rewardCost

api = API.API
load_dotenv()
ADMIN = int(os.getenv('ADMIN_ID'))
MODERATOR1 = int(os.getenv('VHCHENG'))

filler = ['<', '>', '!', '@']

async def daily (ctx):
    """user can earn uwuCreds based on rng, usage is checked to
       function every 20hrs, uwuDB is checked, new users will
       be added with yesterday's time to promote usage
    """
    id, name = ctx.author.id, ctx.author.name
    today, yesterday = getTime(False), getTime(True)
    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    """check if the user has used the command less than 20hrs ago"""
    user_daily = api.fetchDaily(id)
    time_diff = timeDiff(user_daily, today)
    if lessThan24HRs(time_diff):
        await ctx.send(f'<@{id}>, your next **/uwu** resets in **{timeWait(time_diff)}**')
        return

    """update uwuDB"""
    cred_amount, cred_status = dailyLuck()
    api.addCreds(id, cred_amount)
    api.updateDaily(id, today)

    user_name = api.fetchName(id)
    if user_name != name: api.updateName(id, name)
   
    await ctx.send(
        f'{cred_status} <@{id}> **+{cred_amount}** creds were added to your collection'
    )

async def getCreds (ctx):
    """user can check the uwuDB to see how many creds the they 
       have, uwuDB is checked, new users will have 0 creds
    """
    id, name = ctx.author.id, ctx.author.name
    user, yesterday = api.fetchUser(id), getTime(True)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_name = api.fetchName(id)
    if user_name != name: api.updateName(id, name)

    user_creds = api.fetchCreds(id)
    await ctx.send(
        f'<@{id}>, you currently have **{user_creds}** uwuCreds!'
    )

async def purchase (ctx):
    """allow user to exchange uwuCreds for rewards, reward costs
       are tier based, uwuDB is checked, users cannot have more than
       10 tickets, new users will have 0 tickets
    """
    id, name = ctx.author.id, ctx.author.name
    user, yesterday = api.fetchUser(id), getTime(True)
    if len(user) == 0: api.createAccount(id, name, yesterday)
    
    """check if the user has 10 tickets"""
    user_tickets = int(api.fetchTicket(id))
    if ctx.name == 'ticket':
        if user_tickets == 10:
            await ctx.send(
                f'<@{id}>, you already have the max amount of tickets allowed! (10/10)'
            )
            return
    cred_cost = rewardCost(ctx.name, user_tickets)

    """check if the user has enough uwuCreds, update uwuDB"""
    user_creds = api.fetchCreds(id)
    if user_creds - cred_cost > 0:
        api.subCreds(id, cred_cost)
        user_creds = api.fetchCreds(id)

        """update user ticket count"""
        if ctx.name == 'ticket':
            api.buyTicket(id)
            user_tickets = api.fetchTicket(id)
            await ctx.send(
                f'<@{id}>, you have purchased the a ticket for **{cred_cost}**!   (remaining: {user_creds})' +
                f'\nYou now have a total of **{user_tickets}** ticket(s)'
            )
            return

        message_to_pin = await ctx.send(
            f'<@{id}> has purchased the **{ctx.name}** tier reward!   (total: {user_creds})'
        )
        await message_to_pin.pin()
    else:
        await ctx.send(
            f'This tier requires **{cred_cost}** uwuCreds   (you have: {user_creds})'
        )

async def give (ctx, receive, amount, client):
    """allow the user to share their own creds with another user"""
    yesterday = getTime(False)

    """parses the receiver id from discord <@id> format"""
    giver_id, receive_id = ctx.author.id, receive
    for ch in filler: receive_id = receive_id.replace(ch, '')
    receive_id = int(receive_id)

    """check if the user exists in uwuDB"""
    giver_db, giver_name = api.fetchUser(giver_id), ctx.author.name
    if len(giver_db) == 0: api.createAccount(giver_id, giver_name, yesterday)
    
    """check if the user has enough uwuCreds"""
    giver_creds = api.fetchCreds(giver_id)
    if giver_creds < amount:
        await ctx.send(
            f'<@{giver_id}>, you do not have enough uwuCreds.   (total: {giver_creds})'
        )
        return

    """check if the reciever exists in uwuDB"""
    receive_db = api.fetchUser(receive_id)
    if len(receive_db) == 0:
        receive_object = await client.fetch_user(receive_id)
        receive_name = receive_object.name
        api.createAccount(receive_id, receive_name, yesterday)

    """update uwuDB"""
    if amount > 0:
        api.subCreds(giver_id, amount)
        api.addCreds(receive_id, amount)
    
    await ctx.send(
        f'**{amount}** uwuCreds was given to <@{receive_id}>!'
    )

async def handout(ctx, receiver, amount, client):
    """allow moderator user to give new creds to another user, mod
       cannot give more than 3000 creds in a single command
    """
    if amount > 3000:
        await ctx.send(f'dO nOt AbUsE tHy PoWeR1!1!')
        return

    yesterday = getTime()
    
    """parse the receiver id from discord <@id> format"""
    giver_id, receive_id = ctx.author.id, receiver
    for ch in filler: receive_id = receive_id.replace(ch, '')
    receive_id = int(receive_id)

    """check if the user exists in uwuDB"""
    giver_db = api.fetchUser(giver_id)
    giver_name = ctx.author.name
    if len(giver_db) == 0: 
        api.createAccount(giver_id, giver_name, yesterday)
        await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')
        return 

    """check if the user is a moderator"""
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        
        """check if the reciever exists in uwuDB"""
        receive_db = api.fetchUser(receive_id)
        if len(receive_db) == 0:
            receive_object = await client.fetch_user(receive_id)
            receive_name = receive_object.name
            api.createAccount(receive_id, receive_name, yesterday)
        
        """update uwuDB"""
        api.addCreds(receive_id, amount)
        newUwU = api.fetchCreds(receive_id)
        await ctx.send(f'Moderator <@{giver_id}> has graced <@{receive_id}> with {amount} uwuCreds!' +
                       f'\n<@{receive_id}> now has {newUwU}')
        await ctx.send()
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')

async def uwuTax(ctx, victim, amount, client):
    """allow moderator user to take creds from another user, mod
       cannot take more than 1000 creds in a single command
    """
    if amount > 1000:
        await ctx.send(f'dO nOt AbUsE tHy PoWeR1!1!')
        return

    yesterday = getTime()
    
    """parse the victim id from discord <@id> format"""
    mod_id, victim_id = ctx.author.id, victim
    for ch in filler: victim_id = victim_id.replace(ch, '')
    victim_id = int(victim_id)

    """check if the user exists in uwuDB"""
    mod_db = api.fetchUser(mod_id)
    mod_name = ctx.author.name
    if len(mod_db) == 0: 
        api.createAccount(mod_id, mod_name, yesterday)
        await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')
        return 

    """check if the user is a moderator"""
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        
        """check if the victim exists in uwuDB"""
        victim_db = api.fetchUser(victim_id)
        if len(victim_db) == 0:
            victim_object = await client.fetch_user(victim_id)
            victim_name = victim_object.name
            api.createAccount(victim_id, victim_name, yesterday)
            
        """update uwuDB"""
        api.subCreds(victim_id, amount)
        newUwU = api.fetchCreds(victim_id)
        await ctx.send(f'Moderator <@{mod_id}> has taken {amount} uwuCreds! from <@{victim_id}>' +
                       f'\n<@{victim_id}> now has {newUwU}')
        await ctx.send()
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')

async def spy (ctx, victim):
    """allow the user to check another user's uwuCred amount"""
    victim_id = victim
    
    """parse the victim id from discord <@id> format"""
    for ch in filler: victim_id = victim_id.replace(ch, '')
    victim_id = int(victim_id)
    
    """check if the victim exists in uwuDB"""
    victimDB = api.fetchUser(victim_id)
    if len(victimDB) == 0: ctx.reply(f'Target does not exist or has not UwUed')

    user_creds = api.fetchCreds(victim_id)
    await ctx.send(
        f'The target has a total of **{user_creds}** uwuCreds'
    )

async def clearDatabase (ctx):
    """wipes the entire mongoDB cluster documents"""
    id = ctx.author.id

    if id == ADMIN: 
        remove = api.removeUsers()
        await ctx.send(f'All users have been cleared')
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')