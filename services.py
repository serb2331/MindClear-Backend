import hashlib
import re

import bcrypt
from random import randint


def createHashedCode(unique_code):
    salt = bcrypt.gensalt()
    hashed_code = bcrypt.hashpw(unique_code.encode(), salt)
    return hashed_code

def createUser(data, sqlConnector):
    company = data["company"]
    companies = sqlConnector.search("companies", {"company_name": company})
    companyNumber = companies[0][0]

    typeOfUser = data["typeOfUser"]

    email = data["email"]
    sqlConnector.insert("users", {"login_code": "placeholder", "type": typeOfUser, "email": email})
    users = sqlConnector.search("users", {"email": email})
    userPersonalId = users[0][0]

    firstName = data["firstName"]
    lastName = data["lastName"]
    dayOfBirth = data["dayOfBirth"]
    monthOfBirth = data["monthOfBirth"]
    yearOfBirth = data["yearOfBirth"]

    randomNumber = randint(3, 613)

    concatenatedString = f"{email}{firstName}{lastName}{randomNumber}{dayOfBirth}{monthOfBirth}{yearOfBirth}"
    hash_object = hashlib.sha256(concatenatedString.encode())
    unique_code = str(companyNumber) + hash_object.hexdigest()[:6] + str(userPersonalId)

    hashed_code = createHashedCode(unique_code)

    sqlConnector.update("users", {"login_code": hashed_code}, {"email": email})

    return unique_code

def sendUniqueCode(code):
    pass

def loginHandler(requestData, sqlConnector):
    email = requestData["email"]
    password = requestData["password"]

    if sqlConnector.isDataInTable("users", {"email": email}) is True:
        user = sqlConnector.search("users", {"email": email})
        for row in user:
            id = row[0]
            passwordToCheck = row[4].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), passwordToCheck):
                return {"code": 0, "userId": id, "message": "Success."}
        return {"code": 1, "message": "Email or password is incorrect."}
    else:
        return {"code": 2, "message": "Account doesn't exist."}

def isEmailValid(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9]{2,}$", email) is not None

def signupHandler(requestData, sqlConnector):
    email = requestData["email"]
    password = requestData["password"]
    company = requestData["company"]
    print(email)
    print(company)
    sqlConnector.insert("companies", {"company_name": company})

    if not isEmailValid(email):
        return {"code": 4, "message": "Email invalid."}
    if sqlConnector.isDataInTable("users", {"email": email}):
        return {"code": 1, "message": "Email already exists."}
    hashedPassword = createHashedCode(password)

    data = {"email": email, "type": "manager", "password": hashedPassword}

    if sqlConnector.insert("users", data) == 0:
        return {"code": 0, "message": "Success."}
    else:
        return {"code": 5, "message": "Sql error."}