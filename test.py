import random, block, blockchain
from main import BLOCKCHAIN

BLOCKCHAIN = blockchain.Blockchain()
DYL = 382028628227260418
JIM = 197049113924075521
VHC = 390685992194932746
HYE = 476194100769587201

def HumbleDyl (userID):
    if len(BLOCKCHAIN.chain) == 1: return '\nGenesis'

    desc = ['Given', 'Recieved', 'Taken', 'Lost']
    sum = 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == userID:
            if block.getDesc().split(' ')[0] in desc:
                sum += block.getData()
                print('% 4.0f %s' % (block.getData(), block.getDesc()))

    print('Total: ', sum)

def FindAverageUWU (userID):
    if len(BLOCKCHAIN.chain) == 1: return '\nGenesis'

    desc = 'Daily'
    dayCount, sum, bonuSum = 0, 0, 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == userID:
            if block.getDesc() == desc:
                bonus = int(dayCount/8)
                sum += block.getData() - bonus*100
                bonuSum += bonus*100
                dayCount += 1

    average = sum/dayCount

    print('Total: %4d\nAverage: %4.2f\nBonus Total: %4d' % \
        (sum, average, bonuSum))
    
print('START')
num1, num2 = 211, 221

str1 = print('%3d     %3d' % (num1, num2))

print(str1)

print('END\n')
