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

uiLayer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA, 32)
uiLayer = uiLayer.convert_alpha()



button1 = gl.ui.Button({
    "surface": uiLayer,
    "coordSpace": "Center",
    "posX": 450,
    "posY": 250,
    "sizeX": 100,
    "sizeY": 50,
    "Colour": pygame.Color(0, 0, 255, 50),
    "fontSize": 5,
    "text": "hello",
    "style": "default",
    "font": "default",
})

def main():
    events()
    draw()
    clock.tick(FPS)

def draw():
    WINDOW.fill(BACKGROUND)

    uiLayer.fill((255, 255, 255, 255))  # Fill the UI layer with white
    button1.update()
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