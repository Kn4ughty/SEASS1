import pygame as pg

# https://stackoverflow.com/questions/52939385/how-would-i-go-about-creating-smooth-camera-movement-in-pygame

class camera:
    def __init__(self, config: dict) -> None:
        self.x = config.get("x")
        self.y = config.get("y")

        self.vx = config.get("vx")
        self.vy = config.get("vy")


        self.tweenStrength = config.get("tweenStrength", 0)


        self.FPS = config.get("FPS")

    def update():
        pass

    def drawSurf(self, surface: pg.Surface, destSurf: pg.Surface, worldRect: pg.Rect) -> None:
        newrect = pg.Rect()

        # SDL_Rect dstrect = {this->world_pos_tl.x - tiles_to_render[i].x, this->world_pos_tl.y - tiles_to_render[i].y, TILE_WIDTH, TILE_HEIGHT};
        newrect = (self.x - worldRect.x, self.y - worldRect.y, worldRect.size)

        destSurf.blit(surface, newrect)
        pass

