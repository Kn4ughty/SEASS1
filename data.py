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
        print("Yes there is multi-user support, i found it useful when showing the game to friends")
        name = input("Please enter your name here: ")
        UU = str(uuid.uuid1())

        newUser = User(UU, name)

        logging.info(f"generated new user \nname: {name}, UUID: {UU}\n result var {newUser}")

        with open(userListPath, "w") as usersListFile:
            data = json.dumps(asdict(newUser))
            usersListFile.write(data)


    with open(userListPath, "r") as usersListFile:
        users = json.load(usersListFile)

    print(users['name'])
    



def getUser(userListPath):
    with open(userListPath, "r") as usersListFile:
        users = json.load(usersListFile)

    print(len(users))

    #sortedDB = sorted(users, key=lambda x: float(x['creationTime']), reverse=True)

    print(users)

    return users['name']



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