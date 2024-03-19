import pygame as pg

# https://stackoverflow.com/questions/52939385/how-would-i-go-about-creating-smooth-camera-movement-in-pygame


class camera(object):
    def __init__(self, config: dict) -> None:
        self.x = config.get("x")
        self.y = config.get("y")

        self.vx = config.get("vx")
        self.vy = config.get("vy")

        self.WinHeight = config.get("WinHeight")
        self.WinWidth = config.get("WinWidth")

        self.friction = config.get("friction")
        self.moveStrengthConf = config.get("moveStrength")

        self.scale = config.get("scale", 1)
        self.scaleSpeed = config.get("scaleSpeed")

        self.tweenStrength = config.get("tweenStrength", 0)

        # self.scale = config.get("scale")

        self.FPS = config.get("FPS")

        self.zoomMin = 0.75

        self.centerX = self.WinWidth / 2
        self.centerY = self.WinHeight / 2

    def update(self, clock):
        dt = clock.get_time() / 1000
        # print(dt)

        keys = pg.key.get_pressed()


        if self.scale < self.zoomMin:
            self.scale = self.zoomMin


        self.moveStrength = self.moveStrengthConf * self.scale

        if keys[pg.K_j]:
            self.vx += self.moveStrength * dt
        if keys[pg.K_l]:
            self.vx -= self.moveStrength * dt
        if keys[pg.K_i]:
            self.vy += self.moveStrength * dt
        if keys[pg.K_k]:
            self.vy -= self.moveStrength * dt

        # if (keys[pg.K_t]):
        #    self.scale += self.scaleSpeed * dt
        #
        # print(self.scale)

        self.vx -= self.vx * self.friction * dt
        self.vy -= self.vy * self.friction * dt

        self.x += self.vx
        self.y += self.vy

        # print(self.x)
        # print(self.y)

    def drawSurf(
        self,
        surface: pg.Surface,
        destSurf: pg.Surface,
        worldRect: pg.Rect,
        scale: bool = True,
    ) -> None:

        # TODO - check if a surface on screen (or close probably)


        if scale:
            surface = pg.transform.scale(
                surface,
                (surface.get_width() / self.scale, surface.get_height() / self.scale),
            )
            newrect = (
                (
                    ((worldRect.x - self.x) / self.scale) + self.centerX,
                    ((worldRect.y - self.y) / self.scale) + self.centerY,
                ),
                worldRect.size,
            )
            destSurf.blit(surface, newrect)
            return None
        else:
            newrect = (
                (
                    ((worldRect.x - self.x) / self.scale) + self.centerX,
                    ((worldRect.y - self.y) / self.scale) + self.centerY,
                ),
                worldRect.size,
            )

            destSurf.blit(surface, newrect)
