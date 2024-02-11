import sys
import pygame
import math
import GameLib as gl

pygame.init()

# Colours
BACKGROUND = (0, 0, 0)


# Game settings
FPS = 240
clock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

# UI settings
fontSize = 25

rem = fontSize

# Setup

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Moonlander 🚀')

uiLayer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA, 32)
uiLayer = uiLayer.convert_alpha()

def on_button_click():
    print("whoa event!!")

button1 = gl.ui.Button({
    "surface": uiLayer,
    "coordSpace": "Center",
    "posX": 450,
    "posY": 250,
    "sizeX": 100,
    "sizeY": 50,
    "Colour": pygame.Color(0, 0, 255, 50),
    "fontSize": rem,
    "text": "hello",
    "clickEventHandler": on_button_click
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