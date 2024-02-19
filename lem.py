import pygame as pg

class lem(object):
    def __init__(self, config: dict) -> None:
        self.x = config.get("x")
        self.y = config.get("y")

        self.vx = config.get("vx")
        self.vy = config.get("vy")

        self.angle = config.get("angle")
        self.omega = config.get("omega")
        self.maxOmega = config.get("maxOmega")
        self.rotStrength = config.get("rotStrength")
        self.angularFriction = config.get("angularFriction")

        self.throttleSensitivity = config.get("throttleSens")
        self.throttle = 0
        self.maxThrottle = config.get("maxThrottle")

        self.fuel = config.get("fuel")
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
            print("adding AV")
            self.omega += self.rotStrength * dt
        if (keys[pg.K_d] or keys[pg.K_RIGHT]):
            print("subbing AV")
            self.omega -= self.rotStrength * dt

        if (pg.K_w or pg.K_UP or pg.K_LSHIFT):
            newThrottle = self.throttle + (self.throttleSensitivity * dt)
            if newThrottle >= self.maxThrottle:
                pass
            else:
                throttle = newThrottle
        if (pg.K_s or pg.K_DOWN or pg.K_LCTRL):
            newThrottle = throttle - (self.throttleSensitivity * dt)
            if newThrottle <= 0:
                pass
            else:
                throttle = newThrottle
        
        if abs(self.omega) > self.maxOmega:
            if self.omega < 0:
                self.omega = -self.maxOmega
            else:
                self.omega = self.maxOmega
        #angularVelocity *= dt * angleFriction
    
        self.omega -= self.omega * self.angularFriction * dt

        self.angle += self.omega

        self.vy -= self.gravity * dt

        self.x += self.vx
        self.y += self.vy

        print(self.vy)




    def ballerdotwow():
        print('wow, you must be baller')