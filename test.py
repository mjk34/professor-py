import random
import blockchain
from commands.user import findRecentName
from commands.stats import stats, getStat

BLOCKCHAIN = blockchain.Blockchain()

def star_count(BLOCKCHAIN):
    if len(BLOCKCHAIN.chain) == 1: return []
    
    unique_ids = []
    for block in BLOCKCHAIN.chain[1:]:
        unique_ids.append(block.getUser())
    unique_ids = list(set(unique_ids))

    leaderboard = []
    for user_id in unique_ids:
        user_name = findRecentName(user_id, BLOCKCHAIN)
        vitality = getStat(user_id, stats[0], BLOCKCHAIN)
        stamina = getStat(user_id, stats[1], BLOCKCHAIN)
        strength = getStat(user_id, stats[2], BLOCKCHAIN)
        dexterity = getStat(user_id, stats[3], BLOCKCHAIN)
        ego = getStat(user_id, stats[4], BLOCKCHAIN)
        fortune = getStat(user_id, stats[5], BLOCKCHAIN)
        
        leaderboard.append([user_id, user_name, vitality, stamina, strength, dexterity, ego, fortune])
        
    leaderboard.sort(key = lambda x: x[1], reverse=True)
    return leaderboard

def getTotalStars(user_id, BLOCKCHAIN):
    count = 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == 'Star':
                count += 1

    return count

leaderboard = star_count(BLOCKCHAIN)
for i in leaderboard:
    print(i)