import pygame


class Debug(object):
    def __init__(self, SURFACE):
        global rollingFPSAverage
        rollingFPSAverage = []

        self.WINDOW = SURFACE

    def ShowFPS(self, clock):
        fps = str(round(clock.get_fps(), 2))
        font = pygame.font.SysFont("Hack", 15, True)
        img = font.render(fps, True, pygame.Color(0, 255, 0))
        self.WINDOW.blit(img, ((0, 0)))
