from commands.helper import today, checkMonday

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
        2. for each block, update name, return most recent"""
def findRecentName(user_id, BLOCKCHAIN) -> str:
    name = ''
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            name = block.getName()
            
    return str(name)
    
"""Evaluate Blockchain:
        1. find a list of all unique user ids
        2. for each id, get the name, totalCreds, and ticket count
        3. sort the final list and return the top 10 users"""
def getTop(BLOCKCHAIN) -> list:
    if len(BLOCKCHAIN.chain) == 1: return []
    
    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        if block.getName() == 'void_submit': continue
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))
    
    leaderboard = []
    for user_id in unique_ids:
        if user_id == 69: continue
        user_name = findRecentName(user_id, BLOCKCHAIN)
        user_creds = totalCreds(user_id, BLOCKCHAIN)
        
        
        leaderboard.append([user_name, user_creds])  
    leaderboard.sort(key = lambda x: x[1], reverse=True) 
 
    return leaderboard[:10]

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