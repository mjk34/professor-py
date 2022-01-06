import db_services.user_services
user_services = db_services.user_services

def fetchUser (id):
    return user_services.fetchUser(id)

def removeUsers ():
    return user_services.removeUsers()

def fetchCreds (id):
    return user_services.fetchCreds(id)

def fetchName (id):
    return user_services.fetchName(id)

def fetchDaily (id):
    return user_services.fetchDaily(id)

def fetchSubmit (id):
    return user_services.fetchSubmit(id)

def fetchTicket (id):
    return user_services.fetchTicket(id)

def createAccount (id, name, time):
    return user_services.createAccount(id, name, time)

def addCreds (id, amount):
    return user_services.addCreds(id, amount)

def subCreds (id, amount):
    return user_services.subCreds(id, amount)

def updateDaily (id, time):
    return user_services.updateDaily(id, time)

def incrementSubmit (id):
    return user_services.incrementSubmit(id)

def decrementSubmit (id):
    return user_services.decrementSubmit(id)

def buyTicket (id):
    return user_services.buyTicket(id)

def removeUsers ():
    return user_services.removeUsers()

def getTopUsers ():
    return user_services.getTopCreds()

def updateName (id, name):
    return user_services.updateName(id, name)

def fetchValHistory(id):
    return user_services.fetchValHistory(id)

def updateValHistory(id, history):
    return user_services.updateValHistory(id, history)