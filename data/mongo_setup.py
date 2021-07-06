from pymongo import MongoClient

def global_init():
    client = MongoClient('mongodb+srv://Dat1Weeaboo:5394@cluster0.itwoc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client.users
    return db