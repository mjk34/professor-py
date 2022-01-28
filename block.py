import hashlib

class Block:
    def __init__ (self, user, timestamp, description, data, previousHash = ''):
        self.user = user
        self.timestamp = timestamp
        self.description = description
        self.data = data
        self.previousHash = previousHash

        self.hash = self.calculateHash()

    def calculateHash(self):
        input = str(self.user) + str(self.previousHash) + str(self.timestamp) + str(self.description) + str(self.data)
        return hashlib.sha512(input.encode()).hexdigest()