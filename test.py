import sys
import pygame
import GameLib as gl


# Colours
BACKGROUND = (123, 123, 5)

# Game settings
FPS = 60
clock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Moonlander 🚀')

uiLayer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))


config = {
    "coordSpace": "Center",
    "posX": 450,
    "posY": 250,
    "sizeX": 100,
    "sizeY": 50,
    "Colour": pygame.Color("blue"),
    "fontSize": 5,
    "text": "hello",
    "style": "default",
    "font": "default",
}

a = gl.ui.Button(uiLayer, config)

def main():
    events()
    draw()
    clock.tick(FPS)

def draw():
    WINDOW.fill(BACKGROUND)

    uiLayer.fill((255, 255, 255))  # Fill the UI layer with white
    a.update()
    WINDOW.blit(uiLayer, (0, 0))

    pygame.display.flip()
    pygame.display.update()


def events():
    for event in pygame.event.get() :
      if event.type == pygame.QUIT :
        pygame.quit()
        sys.exit()

running = True
while running:
    main()