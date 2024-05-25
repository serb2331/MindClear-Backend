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

    typeOfUser = "employee"

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
            firstName = row[6]
            lastName = row[7]
            passwordToCheck = row[4].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), passwordToCheck):
                return {"code": 0, "userId": id, "firstName": firstName, "lastName": lastName,"message": "Success."}
        return {"code": 1, "message": "Email or password is incorrect."}
    else:
        return {"code": 2, "message": "Account doesn't exist."}

def isEmailValid(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9]{2,}$", email) is not None

def signupHandler(requestData, sqlConnector):
    email = requestData["email"]
    password = requestData["password"]
    company = requestData["company"]
    lastName = requestData["lastName"]
    firstName = requestData["firstName"]
    print(email)
    print(company)
    sqlConnector.insert("companies", {"company_name": company})
    companies = sqlConnector.search("companies", {"company_name": company})
    companyNumber = companies[0][0]

    if not isEmailValid(email):
        return {"code": 4, "message": "Email invalid."}
    if sqlConnector.isDataInTable("users", {"email": email}):
        return {"code": 1, "message": "Email already exists."}
    hashedPassword = createHashedCode(password)

    data = {"email": email, "type": "manager", "password": hashedPassword, "company": companyNumber, "firstName": firstName, "lastName": lastName}

    if sqlConnector.insert("users", data) == 0:
        return {"code": 0, "message": "Success."}
    else:
        return {"code": 5, "message": "Sql error. "}



def getAddedEmployees(requestData, sqlConnector):
    id = requestData["userId"]
    users = sqlConnector.search("users", {"id": id})

    print(users)
    companyid = users[0][5]

    company = sqlConnector.search("companies", {"id": id})
    companyName = company[0][1]
    data = {"company": companyName, "managers": [], "employees": []}

    managers = sqlConnector.search("users", {"company": companyid, "type": "manager"})
    for manager in managers:
        employeeData = {"firstName": manager[6], "lastName": manager[7]}
        data["managers"].append(employeeData)

    employees = sqlConnector.search("users", {"company": companyid, "type": "employee"})
    for employee in employees:
        managerData = {"firstName": employee[6], "lastName": employee[7]}
        data["employees"].append(managerData)
    print(data)
    return data