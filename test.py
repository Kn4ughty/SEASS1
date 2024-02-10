import sys
import pygame
import GameLib as gl


# Colours
BACKGROUND = (0, 0, 0)

# Game settings
FPS = 60
clock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Moonlander 🚀')

uiLayer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))


a = gl.ui.Button((uiLayer, "Center", 450, 250, 100, 50, "blue"), 5, "hello")

def main():
    events()
    draw()
    clock.tick(FPS)

def draw():
    WINDOW.fill(BACKGROUND)

    a.update()

    pygame.display.update()


def events():
    for event in pygame.event.get() :
      if event.type == pygame.QUIT :
        pygame.quit()
        sys.exit()

running = True
while running:
    main()