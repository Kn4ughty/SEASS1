import sys
import pygame as pg
import random
# My librarys
import GameLib as gl
from lem import lem




pg.init()

# Colours
BACKGROUND = pg.Color(0, 0, 0)
SPACECOLOUR = (75, 21, 98)
UIColour = (198, 165, 235, 255)


# !!!!! FLags
DEBUG = True
RAINBOW = False

# Game settings
FPS = 60
clock = pg.time.Clock()
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

## Physics config
gravity = 1.625

# Max thrust = 45040 N
# ISP = 311
# https://www.omnicalculator.com/physics/specific-impulse
# 14.768 kg/s

# Mass including propellant: 10,334 kg
# prop mass is 8200
# 10344 - 8200 = 2144

lem = lem({
    "vx": 20,
    "vy": 3,
    "x": 0,
    "y": 500,
    "angle": 0,
    "omega": 0,
    "maxOmega": 10,
    "rotStrength": 10,
    "angularFriction": 2,
    "throttleSens": 200,
    "maxThrottle": 100,
    "massFlowRate": 14.768,
    "fuel": 8200,
    "ISP": 311,
    "mass": 2144,
    "gravity": gravity,
    "FPS": FPS
})

print(lem.x)
# Setup

WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption('Moonlander 🚀')


uiElements = []
uiLayer = pg.Surface((15 * rem, 10 * rem), pg.SRCALPHA, 32)
uiLayer = uiLayer.convert_alpha()

BACKGROUNDSURF = pg.Surface((0, 0))

LEMIMG = pg.image.load("Assets/LEM.png")

#TOP = ygame.Surface((0, 0), pg.SRCALPHA, 32)

## Startup Variables
inMainMenu = False
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
    "colour": pg.Color(56, 56, 56),
    "fontColour": pg.Color(255, 255, 255),
    "fontSize": fontSize,
    "isBold": True,
    "text": "Debug",
    "clickEventHandler": toggleDebug # works
})
uiElements.append(debugToggleButton)



def main():
    events()
    lem.update(clock)
    draw()


    clock.tick(FPS)


global loops
loops = 1

def draw():
    if DEBUG:
        WINDOW.fill((255, 0, 255)) # Obvoius colour to show un rendered area
    else:
        WINDOW.fill(BACKGROUND)
    
    #pg.image.save(WINDOW, f"start{loops}.png")
    
    drawBackground()

    #pg.image.save(WINDOW, f"background{loops}.png")
    
    drawLEM()
    

    #pg.image.save(WINDOW, f"lem{loops}.png")
    

    drawUI()

    #pg.image.save(WINDOW, f"!UI{loops}.png")
    


    if DEBUG:
        Debug.ShowFPS()


    pg.display.flip()
    #pg.display.update()

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

def drawLEM():

    newLEM = pg.transform.scale(LEMIMG, (960, 700))
    rotated_image = pg.transform.rotate(newLEM, -lem.angle)
    topleft = (0, 0)
    new_rect = rotated_image.get_rect(center = newLEM.get_rect(topleft = topleft).center)

    WINDOW.blit(rotated_image, new_rect)
    #newLEM = pg.transform.rotate(newLEM, LEMAngle)

    #WINDOW.blit(rot_image, (0, 0))


def createStarBackground(size: int, starChance: int) -> pg.Surface:
    out = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    lineWidth = 1
    circle = pg.image.load("Assets/starBlack.png")
    minColourDelta = 200
    for x in range(0, WINDOW_WIDTH):
        for y in range (0, WINDOW_HEIGHT):
            a = random.randrange(0, starChance)
            if a == starChance -1:

                # I should really try to create linse of code that are less long
                #starColour = p.Color((random.randrange(minColourDelta, 255)), (random.randrange(minColourDelta, 255)),(random.randrange(minColourDelta, 255)))
                starColour = gl.image.convert_K_to_RGB(random.triangular(4000, 10000, 5000))
                circle = gl.image.tint(circle, starColour)

                pg.draw.line(out, starColour, (x - size, y), (x + size, y), lineWidth) # IDE sure complains a lot about wrong colour fomat...
                pg.draw.line(out, starColour, (x, y - size), (x, y + size), lineWidth) # for something that works completely fine
                # A circle ends up with an even pixel count, meaning it cannot be centered.
                #p.draw.circle(out, "White", (x, y), size - 3)

                out.blit(circle, (x-4, y-4))


                #p.draw.line(BACKGROUNDSURF,)


    return out

class Debug():

    #def __init__():
    #    global rollingFPSAverage
    #    rollingFPSAverage = []


    def ShowFPS() -> None:
        fps = str(round(clock.get_fps(), 2))
        fontObj = pg.font.SysFont("Hack", 15, True)
        img = fontObj.render(fps, True, pg.Color(0, 255, 0))
        WINDOW.blit(img, ((0, 0)))

    def debugEnviroment(self):
        self.x = 0

        def on_button1_click():
            self.x = self.x + 1
            print(loops)
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
            "Colour": pg.Color(100, 0, 100, 255),
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
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN :
            if event.key == pg.K_EQUALS:
                print("k equals")
                rem = rem + 5
                print(rem)
            if event.key == pg.K_MINUS:
                rem = rem - 5

def StartGame():
    global inMainMenu
    inMainMenu = False




def mainMenu():
    global hasSetup

    if not hasSetup:

        global fontObj
        fontObj = pg.font.SysFont("Hack", 15, True)
        # create buttons,
        # TODO Game logo
        global menuLayer
        menuLayer = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA, 32)
        menuLayer = menuLayer.convert_alpha()


        #pg.image.save(starBackground, "star.png")


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
            "colour": pg.Color(56, 56, 56, 255),
            "fontColour": pg.Color(255, 255, 255),
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


    if loops == 3:
        running = False

    

global starBackground
starBackground = createStarBackground(8, 5000)

running = True
while running:
    while inMainMenu:
        mainMenu()
        loops = loops + 1
    main()
