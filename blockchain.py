from helper import getTime
from block import *

import pickle, os
save_path = 'Blockchain'

class Blockchain:
    def __init__ (self):
        if os.path.exists(save_path):
            file = open(save_path, 'rb')
            self.chain = pickle.load(file)
        else: self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        return Block(-1, getTime(False), 'Genisis Block', 0, '0')

    def getLatestBlock(self):
        return self.chain[-1]

    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.hash = newBlock.calculateHash()

        self.chain.append(newBlock)
    
    def isChainValid(self):
        for i in range(len(self.chain)):
            if i == 0: continue
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]

            if currentBlock.hash != currentBlock.calculateHash(): return False
            if currentBlock.previousHash != previousBlock.hash: return False

            return True
    
    def printChain(self):
        for block in self.chain:
            print(f'user: {block.user}\
                  \ntime: {block.timestamp}\
                  \ndesc: {block.description}\
                  \ndata: {block.data}\
                  \nprev: {block.previousHash}\
                  \nhash: {block.hash}')
            print()
    
    def storeChain(self):
        with open(save_path, 'wb') as output:
            pickle.dump(self.chain, output)