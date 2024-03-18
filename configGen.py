from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
config_object["STARTUP"] = {
    "startinmainmenu": True,
    "sillymode": False,
}

config_object["UI"] = {
    "backgroundcolour": "pain to convert"
}

config_object["CONTROLS"] = {
    "camspeed": -250,
    "camfriction": 7,
    "camScaleSpeed": 0.01,
}


#Write the above sections to config.ini file
def gen(prefPath):
    with open(prefPath + "config.ini", 'w') as conf:
        config_object.write(conf)