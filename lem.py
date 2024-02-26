import pygame as pg
import math


class lem(object):
    def __init__(self, config: dict) -> None:
        self.x = config.get("x")
        self.y = config.get("y")

        self.vx = config.get("vx")
        self.vy = config.get("vy")

        self.width = config.get("width")
        self.height = config.get("height")

        self.angle = config.get("angle")
        self.omega = config.get("omega")
        self.maxOmega = config.get("maxOmega")
        self.rotStrength = config.get("rotStrength")
        self.angularFriction = config.get("angularFriction")

        self.throttleSensitivity = config.get("throttleSens")
        self.throttle = 0
        self.maxThrottle = config.get("maxThrottle")

        self.massFlowRate = config.get("massFlowRate")
        self.fuel = config.get("fuel")
        self.ISP = config.get("ISP")
        self.mass = config.get("mass")

        self.gravity = config.get("gravity")

        self.FPS = config.get("FPS")

    def update(self, clock):
        self.physicsStep(clock)

    def physicsStep(self, clock):

        dt = clock.tick(self.FPS)/1000

        keys = pg.key.get_pressed()
        # There is probably a really cool way to do this where you have list of
        # keys like keys.left and check that, but this is probably fine
        if (keys[pg.K_a] or keys[pg.K_LEFT]):
            self.omega += self.rotStrength * dt
        if (keys[pg.K_d] or keys[pg.K_RIGHT]):
            self.omega -= self.rotStrength * dt


        if (keys[pg.K_w] or keys[pg.K_UP] or keys[pg.K_LSHIFT]):
            newThrottle = self.throttle + (self.throttleSensitivity * dt)
            if newThrottle <= self.maxThrottle:
                self.throttle = newThrottle
            else:
                self.throttle = self.maxThrottle

        if (keys[pg.K_s] or keys[pg.K_DOWN] or keys[pg.K_LCTRL]):
            newThrottle = self.throttle - (self.throttleSensitivity * dt)
            if newThrottle >= 0:
                self.throttle = newThrottle
            else:
                self.throttle = 0
        #if (pg.K_s or pg.K_DOWN or pg.K_LCTRL):
        #    newThrottle = self.throttle - (self.throttleSensitivity * dt)
        #    if newThrottle <= 0:
        #        pass
        #    else:
        #        self.throttle = newThrottle
        
        if abs(self.omega) > self.maxOmega:
            if self.omega < 0:
                self.omega = -self.maxOmega
            else:
                self.omega = self.maxOmega
        #angularVelocity *= dt * angleFriction

        self.omega -= self.omega * self.angularFriction * dt

        self.angle += self.omega

        self.angle = self.angle % 360

        print(self.throttle)

        self.realmass = self.mass + self.fuel



        # thrust in kilograms
        self.thrust = self.gravity * self.ISP * self.massFlowRate


        # x = sin(theta) * F
        # y = cos(theta) * F

        self.vy -= self.gravity * dt

        print(self.vy)

        self.x += self.vx
        self.y += self.vy






    def ballerdotwow():
        print('wow, you must be baller')