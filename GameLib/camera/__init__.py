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


        self.FPS = config.get("FPS")

    def update(self, clock):
        dt = clock.tick(self.FPS)/1000

        keys = pg.key.get_pressed()

        if (keys[pg.K_j]):
            self.vx += self.moveStrength * dt
        if (keys[pg.K_l] ):
            self.vx -= self.moveStrength * dt
        if (keys[pg.K_i]):
            self.vy += self.moveStrength * dt
        if (keys[pg.K_k] ):
            self.vy -= self.moveStrength * dt


        self.vx -= self.vx * self.friction * dt
        self.vy -= self.vy * self.friction * dt

        self.x += self.vx
        self.y += self.vy

        print(self.x)
        print(self.y)


    def drawSurf(self, surface: pg.Surface, destSurf: pg.Surface, worldRect: pg.Rect) -> None:
        #newrect = pg.Rect()

        # SDL_Rect dstrect = {this->world_pos_tl.x - tiles_to_render[i].x, this->world_pos_tl.y - tiles_to_render[i].y, TILE_WIDTH, TILE_HEIGHT};
        newrect = (self.x - worldRect.x, self.y - worldRect.y, worldRect.size)
        print(newrect)

        destSurf.blit(surface, newrect)
        pass

