import pygame as pg

# https://stackoverflow.com/questions/52939385/how-would-i-go-about-creating-smooth-camera-movement-in-pygame

class camera:
    def __init__(self, config: dict) -> None:
        self.pos = config.get("pos")

        self.vel = config.get("vel")

        self.tweenStrength = config.get("tweenStrength", 0)


        self.FPS = config.get("FPS")

    def update():
        pass
