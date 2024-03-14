import sys
import os
import pygame as pg
import random
import configparser
import time
import copy # for backup vars for restart
# Server stuff
import requests
import uuid
# My librarys
import GameLib as gl
import Lib.lib as lib
from lem import lem
import configGen



# TODO - Fix physics to be constant regarless of FPS
## This one is a doozy

# TODO - Name entering


# TODO - Tweak values and make game fune

# TODO - run config gen if file not found

serverURL = "http://127.0.0.1:5000"
scoreGetURL = serverURL + "/scores"
scorePosURL = scoreGetURL + "Post"

startTime = time.time()

prefPath = pg.system.get_pref_path("naught", "MOONLANDER")

#Read config.ini file
if not os.path.isfile(prefPath + "config.ini"):
    configGen.gen(prefPath)

global name

if not os.path.isfile(prefPath + "name"):
    print("WARNINGG!!!!!!!!!!\n"*5)
    print("Name not found in config path")
    name = input("Please enter your name here: ")
    nameFile = open(prefPath + "name", "w")
    nameFile.write(name)
    nameFile.close()
else:
    nameFile = open(prefPath + "name", "r")
    name = nameFile.read()

config_object = configparser.ConfigParser()
config_object.read(prefPath+"config.ini")

STARTUP = config_object["STARTUP"]
CONTROLS = config_object["CONTROLS"]



if not os.path.isfile(prefPath + "UUID"): #UUID not set
    print("UUID not found, making one now")
    UU = str(uuid.uuid1())
    uuidFile = open(prefPath + "UUID", "w")
    uuidFile.write(UU)
    uuidFile.close()
else:
    uuidFile = open(prefPath + "UUID", "r")
    UU = uuidFile.read()
    uuidFile.close


## Startup Variables
inMainMenu = lib.stringToBool(STARTUP["startinmainmenu"])

## Controls
camSpeed = int(CONTROLS["camspeed"])
camFriction = int(CONTROLS["camfriction"])

hasSetup = False
mainHasSetup = False
inEndScreen = False
endScreenSetup = False

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
clock = pg.time.Clock()
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900


WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=0, depth=0, display=0, vsync=1)
pg.display.set_caption('Moonlander 🚀')


# I cannot work out why the physics speed is wrong so
# For now you need to run at 60fps
# Sorry people with slow computers
#FPS = max(pg.display.get_desktop_refresh_rates())
FPS = 60


# UI settings
fontSize = int(WINDOW_WIDTH / 35)

rem = fontSize

uiPadding = 5

gravity = -5


landHeight = 500

global luna
luna = lem({
    "vx": 10,
    "vy": 0,
    "x": -200,
    "y": -3000,
    "width": 9.4,
    "height": 3.231,
    "angle": 0,
    "omega": 0,
    "maxOmega": 10,
    "rotStrength": 15,
    "angularFriction": 10,
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

lem_copy = copy.copy(luna)

camera = gl.camera.camera({
    "x": 0,
    "y": -3000,
    "vx": 0,
    "vy": 0,
    "WinHeight": WINDOW_HEIGHT,
    "WinWidth": WINDOW_WIDTH,
    "friction": camFriction,
    "moveStrength": camSpeed,
    "scale": 3.5,
    "scaleSpeed": 0.01,
    "FPS": FPS
})
camera_copy = copy.copy(camera)

uiElements = []

global uiLayer
uiLayer = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA, 32)
uiLayer = uiLayer.convert_alpha()


scaleFactor = 4
LEMImg = pg.image.load("Assets/LEM.png")
LEMImg = pg.transform.smoothscale(LEMImg, (LEMImg.get_width() / scaleFactor, LEMImg.get_height() / scaleFactor))
LEMExhaustImg = pg.image.load("Assets/Exhaust1.png")
LEMexhaustImg = pg.transform.smoothscale(LEMExhaustImg, (LEMExhaustImg.get_width() / scaleFactor, LEMExhaustImg.get_height() / scaleFactor))


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
    "clickEventHandler": toggleDebug
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
    "progress": (luna.fuel / luna.maxFuel)
})
# I have learned pointerss in python dont really exist so ill have to
# update bars in a hard coded way for each bar.

#uiElements.append(LEMFuelBar)


def resetGame():
    global luna
    global lem_copy
    global camera_copy
    global camera
    global inEndScreen

    luna = lem_copy
    camera = camera_copy
    inEndScreen = False
    


def main():
    global mainHasSetup
    if not mainHasSetup:
        uiElements.append(LEMFuelBar)
        mainHasSetup = True # tee hee performace went weee downwards without this
    events()

    if luna.y > -340:
        global landed
        landed = True

        #calcScore()
        global inEndScreen
        inEndScreen = True


    endScreen()

    if not inEndScreen:
        luna.update(clock)

    camera.x = luna.x
    camera.y = luna.y

    camera.x += (LEMImg.get_width() / 2) / camera.scale
    camera.y += (LEMImg.get_height() / 2) / camera.scale

    camera.update(clock)


    draw()


    clock.tick(FPS)



def draw():
    if isDebug:
        WINDOW.fill((255, 0, 255)) # Obvoius colour to show un rendered area
    else:
        WINDOW.fill(BACKGROUND)
    
    uiLayer.fill((0, 0, 0, 0))


    drawBackground()

    drawMoonSurface()

    drawLEM()

    drawUI()


    if isDebug:
        Debug.ShowFPS()


    #pg.display.flip()
    pg.display.update()

def drawUI():

    #print(uiElements)
    for element in uiElements:
        if element.type == "bar":
            if element.title == "Fuel:":
                element.progress = luna.fuel / luna.maxFuel
                element.contents = f"{round(luna.fuel)} / {round(luna.maxFuel, 1)}" # I love stupid hard coded things
                if inEndScreen:
                    continue
        if element.type == "button":
            if element.text == "Your score is!...":
                #print("weeping rn")
                pass

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


    if luna.fuel > 0:
        LEMexhaustImg.set_alpha(255 * (luna.throttle / luna.maxThrottle))
    else:
        LEMexhaustImg.set_alpha(0)

    lemExhaust, exhaustRect = gl.image.rotate(LEMexhaustImg, luna.angle, (luna.x, luna.y))


    camera.drawSurf(lemExhaust, WINDOW, exhaustRect)


    lem_rotated_image, lemRect = gl.image.rotate(LEMImg, luna.angle, (luna.x, luna.y))
    
    #lemRect.x -= lem_rotated_image.get_width() / 2
    #lemRect.y -= lem_rotated_image.get_height() / 2
    # The lem is gonna be off center and your gonna like it

    camera.drawSurf(lem_rotated_image, WINDOW, lemRect)



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
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.key == pg.K_r:
                print("wagh!!")
                inEndScreen = False
                resetGame()
        if event.type == pg.MOUSEWHEEL:
            #print(event.x, event.y)
            camera.scale += camera.scaleSpeed * event.y * camera.scale

def StartGame():
    global inMainMenu
    inMainMenu = False


def mainMenu():
    global hasSetup
    #print("in main meu")
    #print(time.time())

    if not hasSetup:

        global fontObj
        fontObj = pg.font.SysFont("Hack", 15, True)
        # create buttons,
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
        uiElements.remove(StartGameButton)
        StartGameButton = None

    clock.tick(FPS)


def calcScore():
     #lem.land()
    if luna.angle > 180:
        angFromCenter = 360 - luna.angle
    else:
        angFromCenter = luna.angle

    angScore = -pow((angFromCenter * 0.2), 2) + 40
    if angScore < 0:
        angScore = 0

    yVelScore = (-pow((luna.vy * 0.32), 2) + 10) * 2

    xVelScore = -pow((luna.vy * 0.75), 2) + 10

    global totalScore
    totalScore = (angScore + yVelScore + xVelScore) * 5

    print(f"Score: {totalScore}")

def endScreen():
    global endScreenSetup
    if not endScreenSetup and inEndScreen:
        calcScore()

        humancrytext = ""

        print(totalScore)

        if totalScore < 0:
            humancrytext = "Woah thats really bad :("
        if totalScore > 50:
            humancrytext = "No strawberry jam on the walls this time!"
        if totalScore > 100:
            humancrytext = "Only a few broken bones"
        if totalScore > 200:
            humancrytext = "You might actually make it home!"
        if totalScore > 300:
            humancrytext = "Very good job!"
        if totalScore > 350:
            humancrytext = "I didnt even think this was possible"

        global ScoreText # i am not a fan of this
        ScoreText = gl.ui.Button({
            "surface": uiLayer,
            "type": "button",
            "posX": 30,
            "posY": 5,
            "sizeX": 40,
            "sizeY": 10,
            "anchorSpace": "%",
            "scaleSpace": "%",
            "colour": UIColour,
            "fontColour": fontColour,
            "fontSize": fontSize,
            "isBold": True,
            "text": "Your score is!...",
            "doesHighlighting": False
        })
        uiElements.append(ScoreText)

        # - {int(len(str(round(totalScore, 5))) / 2)}
        global ScoreDisplayText
        ScoreDisplayText = gl.ui.Button({
            "surface": uiLayer,
            "type": "button",
            "posX": 30,
            "posY": 20,
            "sizeX": 40,
            "sizeY": 20,
            "anchorSpace": "%",
            "scaleSpace": "%",
            "colour": UIColour,
            "fontColour": fontColour,
            "fontSize": int(fontSize * 0.7),
            "isBold": True,
            "text": f"{round(totalScore, 5):^30}" +  f"\n {humancrytext:^30}", #formatting strings is hard okay
            "doesHighlighting": False
        })
        uiElements.append(ScoreDisplayText)

        submit_score(name, totalScore)

        global leaderBoardDisplay
        leaderBoardDisplay = gl.ui.Button({
            "surface": uiLayer,
            "type": "button",
            "posX": 5,
            "posY": 45,
            "sizeX": 90,
            "sizeY": 50,
            "anchorSpace": "%",
            "scaleSpace": "%",
            "colour": UIColour,
            "fontColour": fontColour,
            "fontSize": int(fontSize * 0.8),
            "isBold": False,
            "text":parse_leaderboard(get_leaderboard()), #formatting strings is hard okay
            "doesHighlighting": False
        })
        uiElements.append(leaderBoardDisplay)
        endScreenSetup = True
    
    if not inEndScreen and endScreenSetup:
        print("wowah about to delete things!")
        print(f"{inEndScreen} {endScreenSetup}")

        uiElements.remove(ScoreText)
        uiElements.remove(ScoreDisplayText)
        uiElements.remove(leaderBoardDisplay)

        endScreenSetup = False


def get_leaderboard():
    scores = requests.get(scoreGetURL)
    return scores.json()

def parse_leaderboard(data) -> str:
    outStr = ""

    for i in range(0, min(len(data), 10)):
        name = data[i].get("name")
        score = data[i].get("score")
        row = f"{(i+1)}. {name:<10} {score:>20}"
        outStr += row + "\n"

    return outStr

def submit_score(name: str, score: float):
    json = {"name": name, "score": str(score), "UUID": UU}
    requests.post(scorePosURL, json = json)

#x = get_leaderboard() # would do this Async if i knew how

#print(parse_leaderboard(x))

#submit_score()

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



