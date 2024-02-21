import pygame as pg

class camera:
    def __init__(self, config: dict) -> None:
        self.pos = config.get("pos")

        self.vel = config.get("vel") 

        self.tweenStrength = config.get("tweenStrength", 0)


        self.FPS = config.get("FPS")

    def update():
        pass
