import random

from commands.helper import today, checkMonday
from commands.stats import getStar, getStat, stats

"""Evaluated Blockchain:
        1. find the most recent daily based on user_id
        2. check if the date difference is greater than 0"""
def hasDaily(user_id, BLOCKCHAIN) -> bool: 
    if len(BLOCKCHAIN.chain) == 1: return True
    
    desc, date = 'Daily', ''
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                date = block.getTime()
                     
    if date == '': return True
    return {True:False, False:True}[date == today()]

def hasWish(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, count = 'Wish', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                if block.getTime() == today():
                    count += 1
    return count

def getAvgDaily(user_id, BLOCKCHAIN) -> float:
    if len(BLOCKCHAIN.chain) == 1: return -1.0
    
    desc, dayCount, avg = 'Daily', 0, 0.0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                bonus = int(dayCount/8)
                avg += block.getData() - bonus*100
                dayCount += 1
    
    return avg/dayCount

"""Evaluated Blockchain:
        1. find the most recent claim based on user_id
        2. check if the date difference is greater than 0"""
def hasClaim(user_id, BLOCKCHAIN) -> int: 
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, count = 'Claim Bonus', 0
    for block in BLOCKCHAIN.chain[1:]:
        if checkMonday(block.getTime()) == False: continue
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                count += 1
    return count

def hasDonated(user_id, reciever_name, BLOCKCHAIN) -> bool:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc = 'Donate'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            split = block.getDesc().split('$')
            if len(split) == 2:
                if split[0] == desc and split[1] == reciever_name:
                    return True

    return False

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, add up all cred transactions"""
def totalCreds(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, desc1, total = 'Ticket', 'Luck', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc: continue
            if block.getDesc() == desc1: continue
            total += block.getData()
    
    return int(total)

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, add up all cred transactions"""
def totalCredScore(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, total = 'Ticket', 0
    stats = ['Vitality', 'Stamina', 'Dexterity', 'Strength', 'Fortune', 'Star']
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc: continue
            if block.getDesc() in stats: continue
            total += block.getData()
    
    return int(total)

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, add up all ticket transactions"""
def totalTickets(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, total = 'Ticket', 0 
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                total += block.getData()
    
    return int(total)

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, add up all submissions dated today"""
def totalSubsWeek(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, desc3, total = f'Submission', f'Bonus Submit', 0
    for block in BLOCKCHAIN.chain[1:]:
        if checkMonday(block.getTime()) == False: continue
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                total += 1
            if block.getDesc() == desc3:
                total -= 1
    
    return int(total)

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, add up all submissions"""
def totalSubs(user_id, game, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, total = f'Submission {game}', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                total += 1
    
    return int(total)

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, average the most recent 10 submissions
        3. average requires a minimum of 3 submissions"""
def averageScore(user_id, game, BLOCKCHAIN) -> float:
    if len(BLOCKCHAIN.chain) == 1: return -1
    
    desc, average, submissions = f'Submission {game}', 0, []
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                submissions.append(block.data)
    
    if len(submissions) < 3: return -1
    elif len(submissions) < 10: 
        for score in submissions:
            average += score
        average = average/len(submissions)
    else:
        i = len(submissions) - 10
        for score in submissions[i:]:
            average += score
        average = average/10
    
    return float(average)

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, update name, return most recent"""
def findRecentName(user_id, BLOCKCHAIN) -> str:
    name = ''
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            name = block.getName()
            
    return str(name)

"""Find the total cost of ticket(s)"""
def totalValue(user_creds, user_tickets) -> int:
    ticket_value = 0
    for i in range(user_tickets):
        ticket_value += 1500 + i*300
        
    return int(user_creds + ticket_value)
    
"""Evaluate Blockchain:
        1. find a list of all unique user ids
        2. for each id, get the name, totalCreds, and ticket count
        3. sort the final list and return the top 10 users"""
def getTop(BLOCKCHAIN) -> list:
    if len(BLOCKCHAIN.chain) == 1: return []
    
    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))
    
    leaderboard = []
    for user_id in unique_ids:
        if user_id == 69: continue
        user_name = findRecentName(user_id, BLOCKCHAIN)
        user_creds = totalCreds(user_id, BLOCKCHAIN)
        user_tickets = totalTickets(user_id, BLOCKCHAIN)
        total = totalValue(user_creds, user_tickets)
        
        user_stars = getStar(user_id, BLOCKCHAIN)
        # print(f'{user_name} {user_creds} {user_tickets} {total}')
        
        leaderboard.append([user_name, total, user_stars])
        
    leaderboard.sort(key = lambda x: x[1], reverse=True) 

    for i in leaderboard:
        print(i)   
    return leaderboard[:10]

"""Evaluate Blockchain:
        1. find a list of all unique user ids
        2. for each id, get the name and average
        3. sort the final list and return the top 10 users"""
def getAverage(BLOCKCHAIN) -> list:
    if len(BLOCKCHAIN.chain) == 1: return []
    
    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))
    
    leaderboard = []
    for user_id in unique_ids:
        user_name = findRecentName(user_id, BLOCKCHAIN)

        user_avg_val = int(averageScore(user_id, 'V', BLOCKCHAIN))
        user_subs_val = int(totalSubs(user_id, 'V', BLOCKCHAIN))

        user_avg_ow = int(averageScore(user_id, 'O', BLOCKCHAIN))
        user_subs_ow = int(totalSubs(user_id, 'O', BLOCKCHAIN))
        leaderboard.append([user_name, user_avg_val, user_subs_val, user_avg_ow, user_subs_ow])
        
    leaderboard.sort(key = lambda x: x[1], reverse=True)
    return leaderboard[:10]

"""Evaluate Blockchain:
        1. get top 10 users from leaderboard
        2. pick 2 victims from that list"""
def getTopIds(creds, HUMBLE, BLOCKCHAIN) -> list:
    if len(BLOCKCHAIN.chain) == 1: return []
    
    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))
    
    leaderboard = []
    for user_id in unique_ids:
        user_name = findRecentName(user_id, BLOCKCHAIN)
        user_creds = totalCreds(user_id, BLOCKCHAIN)
        user_tickets = totalTickets(user_id, BLOCKCHAIN)
        total = totalValue(user_creds, user_tickets)

        # print(f'{user_name} {user_creds} {user_tickets} {total}')
        
        leaderboard.append([user_id, user_name, user_creds])
        
    leaderboard.sort(key = lambda x: x[2], reverse=True) 

    user1 = random.randint(0, len(leaderboard[:10]) - 1)
    user2 = random.randint(user1 + 1, len(leaderboard[:11]) - 1)

    return [leaderboard[user1], leaderboard[user2]]

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each daily block, add 1 to count"""
def getDailyCount(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, count = 'Daily', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                count += 1

    return int(count)

"""Evaluate Blockchain:
        1. find a list of all unique user ids
        2. for each id, get the name, totalCreds, and ticket count
        3. sort the final list and return the top 10 users"""
def getRaffle(BLOCKCHAIN) -> list:
    if len(BLOCKCHAIN.chain) == 1: return []
    
    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))
    
    raffle = []
    for user_id in unique_ids:
        user_name = findRecentName(user_id, BLOCKCHAIN)
        user_tickets = totalTickets(user_id, BLOCKCHAIN)

        if user_tickets == 0: continue
        
        raffle.append([user_name, user_tickets])   
    raffle.sort(key = lambda x: x[1], reverse=True)  
    return raffle

def getDailyCount(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return -1

    desc, count = 'Daily', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                count += 1

    return count

def getLuck (BLOCKCHAIN, HUMBLE) -> list:
    if len(BLOCKCHAIN.chain) == 1: return []

    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == HUMBLE: continue
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))

    luck = []
    for user_id in unique_ids:
        user_name = findRecentName(user_id, BLOCKCHAIN)
        user_avg  = getAvgDaily(user_id, BLOCKCHAIN)
        user_daily= getDailyCount(user_id, BLOCKCHAIN)
        humble_love= getHumbleLove(user_id, BLOCKCHAIN)

        if user_daily < 5: continue
        luck.append([user_name, user_avg, user_daily, humble_love[0], humble_love[1]])
    luck.sort(key = lambda x: x[1], reverse=True)
    return luck

def getHumbleLove(user_id, BLOCKCHAIN) -> float:
    if len(BLOCKCHAIN.chain) == 1: return -1.0\

    desc = ['~Given', '~Recieved', '~Taken', '~Lost', \
            'Given', 'Recieved', 'Taken', 'Lost']
    sum, count = 0.0, 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc().split(' ')[0] in desc:
                sum += block.getData()
                count += 1

    # print(f'user: {user_id}, sum: {sum}')
    return sum, count

def getServerBonus(BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))
    
    leaderboard = []
    for user_id in unique_ids:
        if user_id == 69: continue
        user_dex = int(getStat(user_id, stats[3], BLOCKCHAIN))
        user_bonus = int(getDailyCount(user_id, BLOCKCHAIN)/7)
        leaderboard.append([user_id, user_bonus + user_dex])
        
    leaderboard.sort(key = lambda x: x[1], reverse=True)
    print(leaderboard[:10])
    print(f'Highest bonus stack is: {leaderboard[0][1]}')

    return leaderboard[0][1]