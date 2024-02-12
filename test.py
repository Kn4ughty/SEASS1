import sys
import pygame
import math  # noqa: F401
import GameLib as gl
import random

pygame.init()

# Colours
BACKGROUND = pygame.Color(0, 0, 0)
SPACECOLOUR = (75, 21, 98)
UIColour = (198, 165, 235, 255)

# !!!!! FLags
DEBUG = False
RAINBOW = False

# Game settings
FPS = 60
clock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

# UI settings
fontSize = 25

rem = fontSize

# Setup

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Moonlander 🚀')


uiElements = []
uiLayer = pygame.Surface((15 * rem, 10 * rem), pygame.SRCALPHA, 32)
uiLayer = uiLayer.convert_alpha()

x = 0


def on_button_click():
    global x
    x = x + 1
    print(x)
    print("whoa event!!")
    if RAINBOW:
        BACKGROUND.r = random.randrange(0, 255)
        BACKGROUND.g = random.randrange(0, 255)
        BACKGROUND.b = random.randrange(0, 255)

button1 = gl.ui.Button({
    "surface": uiLayer,
    "posX": 10,
    "posY": 10,
    "sizeX": 90,
    "sizeY": 50,
    "anchorSpace": "%",
    "scaleSpace": "%",
    "Colour": pygame.Color(100, 0, 100, 255),
    "fontSize": rem,
    "text": "hello",
    "clickEventHandler": on_button_click
})
uiElements.append(button1)

def main():
    events()
    draw()


    clock.tick(FPS)

def draw():
    if DEBUG:
        WINDOW.fill((255, 0, 255)) # Obvoius colour to show un rendered area
    else:
        WINDOW.fill(BACKGROUND)

    drawBackground()

    drawUI()

    if DEBUG:
        Debug.ShowFPS()

    pygame.display.flip()
    pygame.display.update()

def drawUI():
    uiLayer.fill(UIColour)  # Fill the UI layer with white

    #print(uiElements)
    for element in uiElements:
        element.text = str(x)
        element.fontSize = rem
        element.update()


    WINDOW.blit(uiLayer, (0, 0)) #draw final ui to screen

def drawBackground():

    pass

class Debug():

    #def __init__():
    #    global rollingFPSAverage
    #    rollingFPSAverage = []


    def ShowFPS():
        fps = str(round(clock.get_fps(), 2))
        font = pygame.font.SysFont("Hack", 15, True)
        img = font.render(fps, True, pygame.Color(0, 255, 0))
        WINDOW.blit(img, ((0, 0)))

    #def ShowAverageFPS():
    #    pass
    #    # im not doing this

    #    rX = 50 # Get average for 50 frames

    #    fps = round(clock.get_fps(), 2)
    #    rLen = len(rollingFPSAverage)
    #    if rLen < rX:
    #        rollingFPSAverage.append(fps)
    #    elif rLen == rX:
    #        # move every element along,
    #        # delete last one,
    #        pass

    #    font = pygame.font.SysFont("Hack", 15, True)
    #    img = font.render(fps, True, pygame.Color(0, 255, 0))
    #    WINDOW.blit(img, ((0, 0)))


def events():
    global rem
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_EQUALS:
                print("k equals")
                rem = rem + 5
                print(rem)
            if event.key == pygame.K_MINUS:
                rem = rem - 5



running = True
while running:
    main()