import block, blockchain
import random

from commands.helper import today, getName
from dateutil import parser

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

"""Evaluated Blockchain:
        1. find the most recent claim based on user_id
        2. check if the date difference is greater than 0"""
def hasClaim(user_id, BLOCKCHAIN) -> bool: 
    if len(BLOCKCHAIN.chain) == 1: return True
    
    desc, date = 'Claim Bonus', ''
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                date = block.getTime()
                     
    if date == '': return True
    return {True:False, False:True}[date == today()]

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, add up all cred transactions"""
def totalCreds(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, desc2, desc3, total = 'Ticket', 'Submission V', 'Submission L', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc: continue
            if block.getDesc() == desc2: continue
            if block.getDesc() == desc3: continue
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
def totalSubsToday(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0
    
    desc, desc2, desc3, total = 'Submission V', 'Submission L', 'Bonus Submit', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc and block.getTime() == today():
                total += 1
            if block.getDesc() == desc2 and block.getTime() == today():
                total += 1
            if block.getDesc() == desc3 and block.getTime() == today():
                total -= 1
    
    return int(total)

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, average the most recent 10 submissions
        3. average requires a minimum of 3 submissions"""
def averageVScore(user_id, BLOCKCHAIN) -> float:
    if len(BLOCKCHAIN.chain) == 1: return -1
    
    desc, average, submissions = 'Submission V', 0, []
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
        ticket_value += 2000 + i*400
        
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
        user_name = findRecentName(user_id, BLOCKCHAIN)
        user_creds = totalCreds(user_id, BLOCKCHAIN)
        user_tickets = totalTickets(user_id, BLOCKCHAIN)
        total = totalValue(user_creds, user_tickets)

        print(f'{user_name} {user_creds} {user_tickets} {total}')
        
        leaderboard.append([user_name, total])
        
    leaderboard.sort(key = lambda x: x[1], reverse=True) 

    for i in leaderboard:
        print(i)   
    return leaderboard[:10]

"""Evaluate Blockchain:
        1. find a list of all unique user ids
        2. for each id, get the totalCreds
        3. sort the final list and return the top 10 users"""
def getTopIds(creds, HUMBLE, BLOCKCHAIN) -> list:
    if len(BLOCKCHAIN.chain) == 1: return []
    
    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))
    
    leaderboard = []
    for user_id in unique_ids:
        if user_id == HUMBLE: continue
        user_name = findRecentName(user_id, BLOCKCHAIN)
        user_creds = totalCreds(user_id, BLOCKCHAIN)
        if user_creds > creds:
            leaderboard.append([user_id, user_name])
    leaderboard.sort(key = lambda x: x[1], reverse=True)

    max = leaderboard[:10]
    while True:
        user1 = random.randint(0, len(max)-1)
        user2 = random.randint(0, len(max)-1)

        if user1 == user2: continue
        return [max[user1], max[user2]]

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