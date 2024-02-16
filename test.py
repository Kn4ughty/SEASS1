import sys
import pygame
import GameLib as gl
import random
import math


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
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900


# UI settings
fontSize = int(WINDOW_WIDTH / 35)

rem = fontSize

# LEM stats
# all in SI units
LaunchMass = 15200

# Descent stage
DStageDeltaV = 2500
DPropellantMass = 8200
DThrust = 45040

# Dy mass
Mass = 4280

gravity = 1.625

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


def toggleDebug():
    global DEBUG
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
    "fontSize": fontSize,
    "isBold": True,
    "text": "Debug",
    "clickEventHandler": toggleDebug # works
})
uiElements.append(debugToggleButton)

def main():
    events()
    physicsStep()
    draw()


    clock.tick(FPS)

def physicsStep():

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_a or pygame.K_LEFT:
                #angularVelocity += 
                pass
    #angularVelocity 

    
    #xvel += xforce
    pass
    #vy += -5 # go down

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

    WINDOW.blit(starBackground, (0, 0))



def createStarBackground(size: int, starChance: int) -> pygame.Surface:
    out = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    lineWidth = 1
    circle = pygame.image.load("Assets/starBlack.png")
    minColourDelta = 200
    for x in range(0, WINDOW_WIDTH):
        for y in range (0, WINDOW_HEIGHT):
            a = random.randrange(0, starChance)
            if a == starChance -1:

                # I should really try to create linse of code that are less long
                #starColour = pygame.Color((random.randrange(minColourDelta, 255)), (random.randrange(minColourDelta, 255)),(random.randrange(minColourDelta, 255)))
                starColour = gl.image.convert_K_to_RGB(random.triangular(4000, 10000, 5000))
                circle = gl.image.tint(circle, starColour)

                pygame.draw.line(out, starColour, (x - size, y), (x + size, y), lineWidth) # IDE sure complains a lot about wrong colour fomat...
                pygame.draw.line(out, starColour, (x, y - size), (x, y + size), lineWidth) # for something that works completely fine
                # A circle ends up with an even pixel count, meaning it cannot be centered.
                #pygame.draw.circle(out, "White", (x, y), size - 3)

                out.blit(circle, (x-4, y-4))


                #pygame.draw.line(BACKGROUNDSURF,)


    return out

class Debug():

    #def __init__():
    #    global rollingFPSAverage
    #    rollingFPSAverage = []


    def ShowFPS() -> None:
        fps = str(round(clock.get_fps(), 2))
        fontObj = pygame.font.SysFont("Hack", 15, True)
        img = fontObj.render(fps, True, pygame.Color(0, 255, 0))
        WINDOW.blit(img, ((0, 0)))

    def debugEnviroment(self):
        self.x = 0

        def on_button1_click():
            self.x = self.x + 1
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

def StartGame():
    global inMainMenu
    inMainMenu = False


def mainMenu():
    global hasSetup
    if not hasSetup:

        global fontObj
        fontObj = pygame.font.SysFont("Hack", 15, True)
        # create buttons,
        # TODO Game logo
        global menuLayer
        menuLayer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        menuLayer = menuLayer.convert_alpha()

        global starBackground
        starBackground = createStarBackground(8, 5000)
        #pygame.image.save(starBackground, "star.png")


        print(((WINDOW_WIDTH / 2) - (menuLayer.get_width() / 2)))

        global StartGameButton
        StartGameButton = gl.ui.Button({
            "surface": menuLayer,
            "posX": 30,
            "posY": 30,
            "sizeX": 40,
            "sizeY": 10,
            "borderRadius": int(rem / 2),
            "anchorSpace": "%",
            "scaleSpace": "%",
            "colour": pygame.Color(56, 56, 56, 10),
            "fontColour": pygame.Color(255, 255, 255),
            "fontSize": fontSize,
            "isBold": True,
            "text": "Start Game",
            "clickEventHandler": StartGame
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
        uiElements.remove(StartGameButton) #Ide shut up
        StartGameButton = None

    clock.tick(FPS)



running = True
while running:
    while inMainMenu:
        mainMenu()
    main()
