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

def wishCount(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, desc1, count = 'Wish', '-Wish', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                count += 1
            if block.getDesc() == desc1:
                count -= 1
    return count

# implement this into wallet
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
def claimedCount(user_id, BLOCKCHAIN) -> int: 
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
        2. for each block, add up all stitched tickets"""
def totalStitchedTickets(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, total = 'Stitched Ticket', 0 
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                total += 1
    
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
        2. for each block, add up all submissions for a user"""
def totalSubsCount(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, total = f'Clip', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                total += 1
    
    return int(total)

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
        
        user_stars = getStar(user_id, BLOCKCHAIN)
        
        leaderboard.append([user_name, user_creds, user_stars])  
    leaderboard.sort(key = lambda x: x[1], reverse=True) 

    for i in leaderboard:
        print(i)   
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

        # print(f'{user_name} {user_creds} {user_tickets} {total}')
        
        leaderboard.append([user_id, user_name, user_creds])
    leaderboard.sort(key = lambda x: x[2], reverse=True) 

    user1 = random.randint(0, len(leaderboard[:10]) - 1)
    user2 = random.randint(user1 + 1, len(leaderboard[:10]) - 1)

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
        user_stitched = totalStitchedTickets(user_id, BLOCKCHAIN)

        if user_tickets + user_stitched == 0: continue
        
        raffle.append([user_name, user_tickets + user_stitched])   
    raffle.sort(key = lambda x: x[1], reverse=True)  
    return raffle

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

    return leaderboard[0][1]

def totalTokens(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, desc1, count = 'Token', '-Token', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                count += 1
            if block.getDesc() == desc1:
                count -= 1
    return count

def totalTornTickets(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, desc1, count = 'Torn Ticket', '-Torn Ticket', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                count += 1
            if block.getDesc() == desc1:
                count -= 1
    return count

def getShieldCount(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, desc1, count = 'Shield', '-Shield', 0
    for block in BLOCKCHAIN.chain[1:]:
        if checkMonday(block.getTime()) == False: continue
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                count += 1
            if block.getDesc() == desc1:
                count -= 1
    return count