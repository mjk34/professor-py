import db_services.user_services
user_services = db_services.user_services

def fetchUser (id):
    return user_services.fetchUser(id)

def removeUsers ():
    return user_services.removeUsers()

def fetchCreds (id):
    return user_services.fetchCreds(id)

def fetchDaily (id):
    return user_services.fetchDaily(id)

def fetchBirthday (id):
    return user_services.fetchBirthday(id)

def birthdayToday (date):
    return user_services.birthdayToday(date)

def createAccount (id, name, time):
    return user_services.createAccount(id, name, time)

def addCreds (id, amount):
    return user_services.addCreds(id, amount)

def subCreds (id, amount):
    return user_services.subCreds(id, amount)

def updateDaily (id, time):
    return user_services.updateDaily(id, time)

def updateBirthday (id, date):
    return user_services.updateBirthday(id, date)