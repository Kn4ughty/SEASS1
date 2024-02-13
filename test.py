import sys
import pygame
import GameLib as gl
import random

from tempbackups.GameLib import WIN

pygame.init()

# Colours
BACKGROUND = pygame.Color(0, 0, 0)
SPACECOLOUR = (75, 21, 98)
UIColour = (198, 165, 235, 255)

# !!!!! FLags
DEBUG = True
RAINBOW = False

# Game settings
FPS = 60
clock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

starChance = 10

# UI settings
fontSize = 25

rem = fontSize

# Setup

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Moonlander 🚀')


uiElements = []
uiLayer = pygame.Surface((15 * rem, 10 * rem), pygame.SRCALPHA, 32)
uiLayer = uiLayer.convert_alpha()

BACKGROUNDSURF = pygame.Surface((0, 0))

#TOP = ygame.Surface((0, 0), pygame.SRCALPHA, 32)

## Startup Variables
inMainMenu = True
hasSetup = False

x = 0

def toggleDebug():
    global DEBUG
    print(DEBUG)
    if DEBUG:
        DEBUG = False
    else:
        DEBUG = True

debugToggleButton = gl.ui.Button({
    "surface": WINDOW,
    "posX": 90,
    "posY": 0,
    "sizeX": 10,
    "sizeY": 10,
    "anchorSpace": "%",
    "scaleSpace": "%",
    "colour": pygame.Color(56, 56, 56),
    "fontColour": pygame.Color(255, 255, 255),
    "fontSize": 15, #doesnt work
    "isBold": True,
    "text": "Debug",
    "clickEventHandler": toggleDebug # works
})
uiElements.append(debugToggleButton)

def main():
    events()
    draw()


    clock.tick(FPS)

def draw():
    drawBackground()

    drawUI()

    if DEBUG:
        Debug.ShowFPS()

    pygame.display.flip()
    pygame.display.update()

def drawUI():
    #uiLayer.fill(UIColour)  # Fill the UI layer with white

    #print(uiElements)
    for element in uiElements:
        #element.text = str(x)
        element.em = rem # cope future me hahahah
        element.update()

    if inMainMenu:
        WINDOW.blit(menuLayer, (0, 0))


    WINDOW.blit(uiLayer, (0, 0)) #draw final ui to screen

def drawBackground():
    if DEBUG:
        WINDOW.fill((255, 0, 255)) # Obvoius colour to show un rendered area
    else:
        WINDOW.fill(BACKGROUND)

    for i in range(0, WINDOW_WIDTH):
        for i in range (0, WINDOW_HEIGHT):
            a = random.randrange(0, starChance)
            if a == starChance:
                # Draw star
                pass
                #pygame.draw.line(BACKGROUNDSURF,)

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

    def debugEnviroment(self):

        def on_button1_click():
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
            "clickEventHandler": on_button1_click
        })
        uiElements.append(button1)
        



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

def exitMainMenu():
    global inMainMenu
    inMainMenu = False


def mainMenu():
    global hasSetup
    if not hasSetup:
        # create buttons,
        # TODO Game logo
        global menuLayer
        menuLayer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        menuLayer = menuLayer.convert_alpha()

        print(((WINDOW_WIDTH / 2) - (menuLayer.get_width() / 2)))

        global StartGameButton
        StartGameButton = gl.ui.Button({
            "surface": menuLayer,
            "posX": 30,
            "posY": 30,
            "sizeX": 40,
            "sizeY": 10,
            "anchorSpace": "%",
            "scaleSpace": "%",
            "colour": pygame.Color(56, 56, 56),
            "fontColour": pygame.Color(255, 255, 255),
            "fontSize": 15,
            "isBold": True,
            "text": "Start Game",
            "clickEventHandler": exitMainMenu
        })
        uiElements.append(StartGameButton)

        # TODO Controls guide
        # TODO Scaling options
        # TODO Scores

    hasSetup = True

    events()
    draw()



    # Clean up
    if not inMainMenu:
        uiElements.remove(StartGameButton)
        StartGameButton = None

    clock.tick(FPS)



running = True
while running:
    while inMainMenu:
        mainMenu()
    main()