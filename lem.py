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
        self.maxFuel = config.get("maxFuel", self.fuel)
        self.ISP = config.get("ISP")
        self.mass = config.get("mass")

        self.gravity = config.get("gravity")

        self.FPS = config.get("FPS")

    def update(self, clock):
        self.physicsStep(clock)

    def physicsStep(self, clock):

        dt = clock.get_time()/1000

        keys = pg.key.get_pressed()
        # There is probably a really cool way to do this where you have list of
        # keys like keys.left and check that, but this is probably fine
        if (keys[pg.K_a] or keys[pg.K_LEFT]):
            self.omega -= self.rotStrength * dt
        if (keys[pg.K_d] or keys[pg.K_RIGHT]):
            self.omega += self.rotStrength * dt


        if (keys[pg.K_w] or keys[pg.K_UP] or keys[pg.K_LSHIFT]):
            newThrottle = self.throttle + (self.throttleSensitivity * dt)
            self.throttle = min(newThrottle, self.maxThrottle)

        if (keys[pg.K_s] or keys[pg.K_DOWN] or keys[pg.K_LCTRL]):
            newThrottle = self.throttle - (self.throttleSensitivity * dt)
            self.throttle = max(newThrottle, 0)

        if (keys[pg.K_x]):
            self.throttle = 0
        if (keys[pg.K_z]):
            self.throttle = self.maxThrottle

        if abs(self.omega) > self.maxOmega:
            if self.omega < 0:
                self.omega = -self.maxOmega
            else:
                self.omega = self.maxOmega


        # Apply angular friction
        self.omega -= self.angularFriction * self.omega * dt

        self.angle += self.omega

        self.angle = self.angle % 360


        self.realmass = self.mass + self.fuel



        # thrust in kilograms
        self.thrust = self.throttle * self.massFlowRate * dt

        #print(self.fuel)
        self.fuel -= self.throttle * dt * self.massFlowRate

        #print(self.thrust)
        #print(self.angle)

        self.vx += math.sin(math.radians(self.angle)) * self.thrust * dt
        self.vy -= math.cos(math.radians(self.angle)) * self.thrust * dt

        #print(f"vx: {self.vx}")
        #print(f"vy: {self.vy}")

        # GRAVITY!!
        #self.vy -= self.gravity * dt


        #print(self.vy)

        self.x += self.vx
        self.y += self.vy



    def ballerdotwow():
        print('wow, you must be baller')