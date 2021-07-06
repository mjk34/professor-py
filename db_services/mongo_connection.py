from pymongo import MongoClient
mongo_connection = None

MONGO_CONNECTION_KEY = 'mongodb+srv://Dat1Weeaboo:5394@cluster0.itwoc.mongodb.net/users'
def getMongo_connection():
    global mongo_connection
    if not mongo_connection:
        mongo_connection = MongoClient(MONGO_CONNECTION_KEY)
    return mongo_connection