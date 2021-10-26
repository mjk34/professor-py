import db_services.mongo_connection

conn = db_services.mongo_connection.getMongo_connection()
db = conn.uwuDB
collection = db.users

# post = {'_id':<discord ID>, 'name': <discord name>, 'creds': <uwuCreds>}
# collection.insert_one(post)

def fetchUser (id):
    return list(collection.find({'_id': id}))

def fetchCreds (id):
    user_data = fetchUser(id)
    return user_data[0]['creds']

def fetchName (id):
    user_data = fetchUser(id)
    return user_data[0]['name']

def fetchDaily (id):
    user_data = fetchUser(id)
    return user_data[0]['daily']

def fetchSubmit (id):
    user_data = fetchUser(id)
    return user_data[0]['val_submit']

def fetchTicket (id):
    user_data = fetchUser(id)
    return user_data[0]['tickets']

def fetchBirthday (id):
    user_data = fetchUser(id)
    return user_data[0]['birthday']

def birthdayToday (date):
    users = list(collection.find({}))
    for user_data in users:
        if user_data['birthday'] == date:
            return user_data['_id']
    return None

def createAccount (id, name, time):
    newUser = {
        '_id': id,
        'name': name,
        'creds': 0,
        'daily': time,
        'birthday': '',
        'val_submit': 2,
        'tickets': 0
    }

    collection.insert_one(newUser)

def addCreds (id, amount):
    user_data = fetchUser(id)
    user_creds = user_data[0]['creds']
    user_creds = user_creds + amount

    collection.find_one_and_update(
        {'_id': id}, {'$set': {'creds': user_creds}}
    )

def subCreds (id, amount):
    user_data = fetchUser(id)
    user_creds = user_data[0]['creds']
    user_creds = user_creds - amount

    collection.find_one_and_update(
        {'_id': id}, {'$set': {'creds': user_creds}}
    )

def updateDaily (id, time):
    user_daily = time
    collection.find_one_and_update(
        {'_id': id}, {'$set': {'daily': user_daily}}
    )
    collection.find_one_and_update(
        {'_id': id}, {'$set': {'val_submit': 0}}
    )

def incrementSubmit (id):
    user_data = fetchUser(id)
    user_submit = user_data[0]['val_submit']
    user_submit = user_submit + 1

    collection.find_one_and_update(
        {'_id': id}, {'$set': {'val_submit': user_submit}}
    )

def buyTicket (id):
    user_data = fetchUser(id)
    user_tickets = user_data[0]['tickets']
    user_tickets = user_tickets + 1

    collection.find_one_and_update(
        {'_id': id}, {'$set': {'tickets': user_tickets}}
    )

def updateBirthday (id, date):
    user_birthday = date

    collection.find_one_and_update(
        {'_id': id}, {'$set': {'birthday': user_birthday}}
    )

def removeUsers ():
    users = list(collection.find({}))
    for user_data in users:
        myQuery = {'_id': user_data['_id']}
        collection.delete_one(myQuery)

def getTopCreds ():
    users = list(collection.find({}))
    allUsers = []

    for user_data in users:
        user_name = user_data['name']
        user_creds = user_data['creds']
        user_ticket = user_data['tickets']

        user = [user_name, user_creds, user_ticket]
        allUsers.append(user)


    for i in range(len(allUsers)):
        min_index = i
        for j in range(i+1, len(allUsers)):
            if allUsers[min_index][1] < allUsers[j][1]:
                min_index = j
        allUsers[i], allUsers[min_index] = allUsers[min_index], allUsers[i]

    topUsers = []
    topSize = 0
    if len(allUsers) < 10:
        topSize = len(allUsers)
    else: topSize = 10

    for i in range(topSize):
        topUsers.append(allUsers[i])
    
    return topUsers

def updateName (id, name):
    user_name = name

    collection.find_one_and_update(
        {'_id': id}, {'$set': {'name': user_name}}
    )
        