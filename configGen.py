from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
config_object["STARTUP"] = {
    "startinmainmenu": False,
    "sillymode": True,
}

config_object["UI"] = {
    "backgroundcolour": "pain to convert"
}

config_object["CONTROLS"] = {
    "camspeed": -250,
    "camfriction": 7,
}
#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)