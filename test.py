import sys
import pygame as pg
import random
import configparser
import time
# My librarys
import GameLib as gl
import Lib.lib as lib
from lem import lem


# TODO - exhaust images (animated?)
# TODO - Add ending settings and scoring stuff
# TODO - Tweak values and make game fune


startTime = time.time()


#Read config.ini file
config_object = configparser.ConfigParser()
config_object.read("config.ini")

STARTUP = config_object["STARTUP"]
CONTROLS = config_object["CONTROLS"]

## Startup Variables
inMainMenu = lib.stringToBool(STARTUP["startinmainmenu"])

## Controls
camSpeed = int(CONTROLS["camspeed"])
camFriction = int(CONTROLS["camfriction"])

hasSetup = False

good = True
bad = False

if good:
    print("yay")
if bad:
    x = input('bad :( help um jeeeifeejifjiefjeugfoglrflihj codingn its me im ashley codoing)')
pg.init()

# Colours

## UI stuff
UIColour = pg.Color(77, 84, 123, 255 * 0.7)
fontColour = pg.Color(255, 255, 255)

barColour = pg.Color(50, 255, 186)
barOutlineColour = pg.Color(255, 185, 252)
contentFontColour = pg.Color(255, 90, 248)

# World stuff
BACKGROUND = pg.Color(0, 0, 0)
moonMedColour = pg.Color(127, 127, 127)

# !!!!! FLags
isDebug = True
RAINBOW = False

# Game settings
FPS = 60
clock = pg.time.Clock()
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900


# UI settings
fontSize = int(WINDOW_WIDTH / 35)

rem = fontSize

uiPadding = 5

# LEM stats
# all in SI units
#LaunchMass = 15200

# Descent stage
#DStageDeltaV = 2500
#DPropellantMass = 8200
#DThrust = 45040

# Dy mass
#Mass = 4280

## Physics config
#gravity = -1.625
gravity = -5

# Max thrust = 45040 N
# ISP = 311
# https://www.omnicalculator.com/physics/specific-impulse
# 14.768 kg/s

# Mass including propellant: 10,334 kg
# prop mass is 8200
# 10344 - 8200 = 2144



# 112 N on moon
# 686 N on earth


lem = lem({
    "vx": 0,
    "vy": 0,
    "x": 0,
    "y": 0,
    "width": 9.4,
    "height": 3.231,
    "angle": 0,
    "omega": 0,
    "maxOmega": 10,
    "rotStrength": 10,
    "angularFriction": 2,
    "throttleSens": 200,
    "maxThrottle": 100,
    "massFlowRate": 14.768,
    "fuel": 8200,
    "maxFuel": 8200,
    "ISP": 311,
    "mass": 2144,
    "gravity": gravity,
    "FPS": FPS
})

camera = gl.camera.camera({
    "x": 0,
    "y": 0,
    "vx": 0,
    "vy": 0,
    "friction": camFriction,
    "moveStrength": camSpeed,
    "FPS": FPS
})

# Setup

WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=0, depth=0, display=0, vsync=1)
pg.display.set_caption('Moonlander 🚀')


uiElements = []
#uiLayer = pg.Surface((15 * rem, 10 * rem), pg.SRCALPHA, 32)
#uiLayer = uiLayer.convert_alpha()

global uiLayer
uiLayer = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA, 32)
uiLayer = uiLayer.convert_alpha()


LEMImg = pg.image.load("Assets/LEM.png")


def toggleDebug():
    global isDebug
    if isDebug:
        isDebug = False
    else:
        isDebug = True

debugToggleButton = gl.ui.Button({
    "surface": WINDOW,
    "type": "button",
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


LEMFuelBar = gl.ui.bar({
    "surface": uiLayer,
    "type": "bar",
    "posX": 78,
    "posY": 88,
    "sizeX": 20,
    "sizeY": 10,
    "padding": uiPadding,
    "anchorSpace": "%",
    "scaleSpace": "%",
    "colour": UIColour,
    "barColour": barColour,
    "barOutlineColour": barOutlineColour,
    "fontColour": fontColour,
    "contentFontColour": contentFontColour,
    "fontSize": int(fontSize / 1.5),
    "isBold": False,
    "text": "Fuel:",
    "progress": (lem.fuel / lem.maxFuel)
})
# I have learned points in python dont really exist so ill have to
# update bars in a hard coded way for each bar.

uiElements.append(LEMFuelBar)

print((lem.fuel / lem.maxFuel))

def main():
    #pg.draw.rect(WINDOW, (138, 12, 123), (10, 10, 100, 100))
    events()
    camera.update(clock)
    lem.update(clock)
    draw()


    clock.tick(FPS)



def draw():
    if isDebug:
        WINDOW.fill((255, 0, 255)) # Obvoius colour to show un rendered area
    else:
        WINDOW.fill(BACKGROUND)


    drawBackground()

    drawMoonSurface()

    drawLEM()

    drawUI()


    if isDebug:
        Debug.ShowFPS()


    pg.display.flip()
    #pg.display.update()

def drawUI():

    #print(uiElements)
    for element in uiElements:
        if element.type == "bar":
            if element.title == "Fuel:":
                element.progress = lem.fuel / lem.maxFuel
                element.contents = f"{round(lem.fuel)} / {round(lem.maxFuel, 1)}"

        #element.text = str(x)
        element.em = rem # cope future me hahahah
        element.update()

    if inMainMenu:
        WINDOW.blit(menuLayer, (0, 0))


    WINDOW.blit(uiLayer, (0, 0)) #draw final ui to screen


def drawBackground():

    WINDOW.blit(starBackground, (0, 0))

def drawMoonSurface():
    # check if on screen (or close probably)
    # draw moon
    camera.drawSurf(moonSurf, WINDOW, pg.Rect(0, 0, 0, 0))

def drawLEM():
    # SMooth scale seems to work at good fps hmmm
    newLEM = pg.transform.smoothscale(LEMImg, (480, 350))
    rotated_image = pg.transform.rotate(newLEM, -lem.angle)
    topleft = (lem.x, lem.y)
    nr = rotated_image.get_rect(center = newLEM.get_rect(topleft = topleft).center)


    #print(pg.Rect(nr.x + lem.x, nr.y + lem.y, nr.width, nr.height))
    #print(pg.Rect(nr.x + lem.x, nr.y + lem.y, nr.width +lem.width, nr.height + lem.height))


    #WINDOW.blit(rotated_image, nr)
    #camera.drawSurf(rotated_image, WINDOW, pg.Rect(nr.x + lem.x, nr.y + lem.y, nr.width +lem.width, nr.height + lem.height))
    camera.drawSurf(rotated_image, WINDOW, nr)
    #newLEM = pg.transform.rotate(newLEM, LEMAngle)

    #WINDOW.blit(rot_image, (0, 0))


def createStarBackground(starSize: int, starChance: int) -> pg.Surface:
    out = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    lineWidth = 1
    circle = pg.image.load("Assets/starBlack.png")
    for x in range(0, WINDOW_WIDTH):
        for y in range (0, WINDOW_HEIGHT):
            a = random.randrange(0, starChance)
            if a == starChance -1:

                # I should really try to create linse of code that are less long
                #starColour = p.Color((random.randrange(minColourDelta, 255)), (random.randrange(minColourDelta, 255)),(random.randrange(minColourDelta, 255)))
                starColour = gl.image.convert_K_to_RGB(random.triangular(4000, 10000, 5000))
                circle = gl.image.tint(circle, starColour)

                pg.draw.line(out, starColour, (x - starSize, y), (x + starSize, y), lineWidth)
                pg.draw.line(out, starColour, (x, y - starSize), (x, y + starSize), lineWidth)
                # A circle ends up with an even pixel count, meaning it cannot be centered.
                #p.draw.circle(out, "White", (x, y), size - 3)

                out.blit(circle, (x-4, y-4))


    return out

def createMoonSurface(craterSizeMin: int, craterSizeMax: int, size: tuple, craterChance: int, moonMedColour) -> pg.Surface:

    #This method is very expensive.
    #I could like set it up so it does this once and then like stores the image.
    #Maybe do it on startup for a new user and store it in like appdata/equivilant
    #then each user gets a uniqie surface.
    #it doesnt really matter TBH

    # cr is abreviation for crater

    out = pg.Surface((size))
    pg.draw.rect(out, moonMedColour, ((0, 0), size))

    minColour = 50
    maxColour = 200


    for i in range(0, size[0]*size[1]):
        a = random.randrange(0, craterChance)
        if a == 1:
            x = random.randrange(size[0])
            y = random.randrange(size[1])
            crSize = random.triangular(craterSizeMin, craterSizeMax)
            crColourNum = random.triangular(minColour, maxColour)
            crColour = pg.Color(crColourNum, crColourNum, crColourNum)
            # Main circle
            pg.draw.circle(out, crColour, (x, y), crSize)

            pg.draw.circle(out, pg.Color(crColourNum - 10, crColourNum - 10, crColourNum - 10), (x, y), crSize / 1.25)

            subCrMin = int(crSize / 30)
            subCrMax = int(crSize / 10)

            Subcraters = random.randrange(subCrMin, subCrMax) # could be proprtional to crater size?
            for k in range(Subcraters):
                subCrColourNum = random.triangular(minColour, maxColour)
                subCrColour = pg.Color(subCrColourNum, subCrColourNum, subCrColourNum)

                ratio = int(crSize / 1.5)

                xOffset = random.randrange(-ratio, ratio)
                yOffset = random.randrange(-ratio, ratio)

                subCrSize = random.triangular(4, crSize / 4)

                pg.draw.circle(out, subCrColour, (x + xOffset, y + yOffset), subCrSize)

                #pg.draw.circle()




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
            "type": "button",
            "posX": 30,
            "posY": 30,
            "sizeX": 40,
            "sizeY": 10,
            "anchorSpace": "%",
            "scaleSpace": "%",
            "colour": UIColour,
            "fontColour": fontColour,
            "fontSize": fontSize,
            "isBold": True,
            "text": "Start Game",
            "clickEventHandler": StartGame
        })
        uiElements.append(StartGameButton)


        # TODO Controls guide
        # TODO Scaling options
        # TODO Scores

        # title
        titleFont = pg.font.Font("Assets/Moonlander.otf", fontSize*5)
        global titleImg
        titleImg = titleFont.render("MOONLANDER", True, "Grey")



    hasSetup = True



    events()
    drawBackground()
    drawUI()

    titlepos = (((WINDOW_WIDTH - titleImg.get_width()) / 2), 50)

    WINDOW.blit(titleImg, titlepos)


    keys = pg.key.get_just_released()
    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()

    pg.display.flip()

    # Clean up
    if not inMainMenu:
        uiElements.remove(StartGameButton) #Ide shut up
        StartGameButton = None

    clock.tick(FPS)



t1 = time.time()
global starBackground
starBackground = createStarBackground(8, 5000)
if isDebug:
    print(f"Star Bg Gen time (s): {time.time() - t1}")

running = True

t1 = time.time()
global moonSurf
moonSurf = createMoonSurface(12, 100, (4000, 500), 10000, moonMedColour)
if isDebug:
    print(f"MoonSurfGen time (s): {time.time() - t1}")


if isDebug:
    print(f"Total startup time (s): {time.time()- startTime}")



while running:
    while inMainMenu:
        mainMenu()
    main()

