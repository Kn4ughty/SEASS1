from configparser import ConfigParser


config_object = ConfigParser()

config_object["STARTUP"] = {
    "startinmainmenu": True,
    "sillymode": False,
    "serverURL": "http://localhost:5000"
}

config_object["UI"] = {
    "backgroundcolour": "pain to convert"
}

config_object["CONTROLS"] = {
    "camspeed": -250,
    "camfriction": 7,
    "cameraScaleMouseWheelSenstivity": 0.01,
}



def gen(prefPath):
    with open(prefPath + "config.ini", 'w') as conf:
        config_object.write(conf)