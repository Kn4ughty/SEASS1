import os
import sys
import json
import uuid

def initName(prefPath):
    print("INFO!!!!!!!!!!\n"*5)
    print("Name not found in config path")
    print("Your name will be used for online leaderboard scores")
    name = input("Please enter your name here: ")

    if not os.path.isfile(prefPath + "userList.json"):
        userlistF = open(prefPath + "userList.json", "w")
        userlistF.write(name)
        userlistF.close()

    nameFile = open(prefPath + "name", "w")
    nameFile.write(name)
    nameFile.close()


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