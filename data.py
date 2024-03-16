import os
import json
import uuid
import logging
import time
from dataclasses import dataclass, asdict



@dataclass(frozen=True, order=True)
class User:
    iden: str
    name: str
    creationTime: float = time.time()



def initName(userListPath):
    if not os.path.isfile(userListPath):
        
        print("INFO!!!!!!!!!!\n"*5)
        print("existing user not found")
        print("Your name will be used for online leaderboard scores and will be visible to other players")
        name = input("Please enter your name here: ")
        UU = str(uuid.uuid1())

        newUser = User(UU, name)

        logging.info(f"generated new user \nname: {name}, UUID: {UU}\n result var {newUser}")

        with open(userListPath, "w") as usersListFile:
            data = json.dumps([asdict(newUser)])
            print(data)
            usersListFile.write(data)

    
def selectUser(userListPath) -> int:
    with open(userListPath, "r") as usersListFile:
        users = json.load(usersListFile)

    #if len(users) == 1:
    #    return 1


    print("Multiple users found")
    print("Please select which user you would like to play as")
    print("Each user has their own leaderboard entry")

    tries = 0
    x = 1
    while not isValid(x, users) or tries == 0:
        if tries > 0:
            print("Not a valid user please try again.")
        for i in range(len(users)):
            user = users[i]
            print(f"{i+1}. {user['name']}")
        
        tries += 1

        print(len(users))
        x = input("#: ")
    
    return int(x)

    

def isValid(x, users) -> bool:
    try:
        x = int(x)
    except ValueError:
        print("invalid input. (could not change to int)")
        return False

    if x >= len(users):
        if x > 0:
            return True
        else:
            print(f"{x} is negative 🤪 <- you rn")
    else:
        print(f"{x} is too large")
    
    return False


def getUser(userListPath, userNum=0):
    with open(userListPath, "r") as usersListFile:
        users = json.load(usersListFile)

    print(len(users))

    #sortedDB = sorted(users, key=lambda x: float(x['creationTime']), reverse=True)

    print(users)

    return users[0]['name']



def newUser(prefPath):
    print("So you want a new user huhu?")
    print("okay")
    newUser = input("Enter the new")

    userFile = open(prefPath + "name", "w")
    userFile.write(newUser)
    userFile.close()
    #userlistF = open(prefPath + "userList.json", "r+")
    #userlist = userlistF.read()

def createAndWriteUUID(prefPath):
    UU = str(uuid.uuid1())
    uuidFile = open(prefPath + "UUID", "w")
    uuidFile.write(UU)
    uuidFile.close()