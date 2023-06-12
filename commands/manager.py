import block, blockchain
from commands.helper import today

def pushBlock(block, BLOCKCHAIN):
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()   


def pushItem(id, name, item, BLOCKCHAIN):
    """Generate new Block"""
    item_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = item,
        data = 0
    )

    pushBlock(item_block, BLOCKCHAIN)

def pushWish(id, name, BLOCKCHAIN):

    """Generate new Block"""
    wish_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Wish',
        data = 0
    )

    """Update Blockchain"""
    pushBlock(wish_block, BLOCKCHAIN)

    return