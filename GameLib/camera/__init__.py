import pygame as pg

# https://stackoverflow.com/questions/52939385/how-would-i-go-about-creating-smooth-camera-movement-in-pygame

class camera(object):
    def __init__(self, config: dict) -> None:
        self.x = config.get("x")
        self.y = config.get("y")

        self.vx = config.get("vx")
        self.vy = config.get("vy")

        self.friction = config.get("friction")
        self.moveStrength = config.get("moveStrength")


        self.tweenStrength = config.get("tweenStrength", 0)

        #self.scale = config.get("scale")
        #self.scaleSpeed = config.get("scaleSpeed")

        self.FPS = config.get("FPS")

    def update(self, clock):
        dt = clock.get_time()/1000

        keys = pg.key.get_pressed()

        if (keys[pg.K_j]):
            self.vx += self.moveStrength * dt
        if (keys[pg.K_l] ):
            self.vx -= self.moveStrength * dt
        if (keys[pg.K_i]):
            self.vy += self.moveStrength * dt
        if (keys[pg.K_k] ):
            self.vy -= self.moveStrength * dt

        #if (keys[pg.K_t]):
        #    self.scale += self.scaleSpeed * dt
        #
        #print(self.scale)


        self.vx -= self.vx * self.friction * dt
        self.vy -= self.vy * self.friction * dt

        self.x += self.vx
        self.y += self.vy

        #print(self.x)
        #print(self.y)


    def drawSurf(self, surface: pg.Surface, destSurf: pg.Surface, worldRect: pg.Rect) -> None:
        # Fun fact size of the rect does not matter it just draws the surface sooo
        # No camera scaling

        #print(worldRect)

        #newrect = ((self.x - worldRect.x), (self.y - worldRect.y)), worldRect.size

        newrect = ((worldRect.x - self.x), (worldRect.y - self.y)), worldRect.size

        #print(newrect)

        destSurf.blit(surface, newrect)

