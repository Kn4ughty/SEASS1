import sys
import os
import pygame as pg
import random
import configparser
import time
import copy  # for backup vars for restart
import logging  # I wish i had known about this module earlier.. 15/03/2024

# My librarys

import GameLib as gl
import Lib.lib as lib
import leaderboard
import lemmer
import configGen
import data

logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(message)s",
)


# TODO - Fix physics to be constant regarless of FPS
## This one is a doozy

# TODO - Tweak values and make game fune

# TODO - Fix the moon surface being finite
## Potentially tile it?
## or make it reallly logn


serverURL = "http://localhost:5000"
scoreGetURL = serverURL + "/scores"
scorePostURL = scoreGetURL + "Post"

startTime = time.time()

prefPath = pg.system.get_pref_path("naught", "MOONLANDER")
logging.info(f"preferences path set at \"{prefPath}\"")

# Read config.ini file
if not os.path.isfile(prefPath + "config.ini"):
    configGen.gen(prefPath)


global name

userListPath = os.path.join(prefPath, "userList.json")




data.initName(userListPath)

print(sys.argv)
if len(sys.argv) > 1:
    match sys.argv[1]:
        case "+U":
            print("WAHHh!!")
            data.newUser(userListPath)

#data.selectUser(userListPath)

name, UU = data.getUser(userListPath)
logging.info(f"Name = {name}")

config_object = configparser.ConfigParser()
config_object.read(prefPath + "config.ini")

STARTUP = config_object["STARTUP"]
CONTROLS = config_object["CONTROLS"]


## Startup Variables
inMainMenu = lib.stringToBool(STARTUP["startinmainmenu"])
sillyMode = lib.stringToBool(STARTUP["sillymode"])

## Controls
camSpeed = float(CONTROLS["camspeed"])
camFriction = float(CONTROLS["camfriction"])
camScaleSpeed = float(CONTROLS["camScaleSpeed"])

hasSetup = False
mainHasSetup = False
inEndScreen = False
endScreenSetup = False

good = True
bad = False

if good:
    print("yay")
if bad:
    x = input(
        "bad :( help um jeeeifeejifjiefjeugfoglrflihj codingn its me im ashley codoing)"
    )
pg.init()

# Colours
opacityPercent = 0.7
## UI stuff
UIColour = pg.Color(77, 84, 123, int(255 * opacityPercent))
fontColour = pg.Color(255, 255, 255)
HudColour = pg.Color(44, 48, 71, int(255 * 0.8))

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


WINDOW = pg.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT), flags=0, depth=0, display=0, vsync=1
)
pg.display.set_caption("Moonlander 🚀")


# I cannot work out why the physics speed is wrong so
# For now you need to run at 60fps
# Sorry people with slow computers
# FPS = max(pg.display.get_desktop_refresh_rates())
FPS = 60


# UI settings
fontSize = int(WINDOW_WIDTH / 35)

rem = fontSize

uiPadding = 5

gravity = -4


startVX = 30
startVY = 0
startX = -1000
startY = -2500

lemRotStrength = 12

if sillyMode:
    lemRotStrength *= -1

global lem
lem = lemmer.lem(
    {
        "vx": startVX,
        "vy": startVY,
        "x": startX,
        "y": startY,
        "width": 9.4,
        "height": 3.231,
        "angle": 270,
        "omega": 0,
        "maxOmega": 100,
        "rotStrength": lemRotStrength,
        "angularFriction": 8,
        "throttleSens": 100,
        "maxThrottle": 100,
        "massFlowRate": 14,
        "fuel": 5000,
        "maxFuel": 5000,
        "ISP": 311,
        "mass": 2144,
        "gravity": gravity,
        "FPS": FPS,
    }
)

lem_copy = copy.deepcopy(lem)

camStartX = 1000
camStartY = -1000

camStartScale = 4

camera = gl.camera.camera(
    {
        "x": camStartX,
        "y": camStartY,
        "vx": 0,
        "vy": 0,
        "WinHeight": WINDOW_HEIGHT,
        "WinWidth": WINDOW_WIDTH,
        "friction": camFriction,
        "moveStrength": camSpeed,
        "scale":camStartScale,
        "scaleSpeed": camScaleSpeed,
        "FPS": FPS,
    }
)
camera_copy = copy.deepcopy(camera)

uiElements = []

global uiLayer
uiLayer = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA, 32)
uiLayer = uiLayer.convert_alpha()


scaleFactor = 0.75
LEMImg = pg.image.load("Assets/LEM.png")
LEMImg = pg.transform.smoothscale(
    LEMImg, (LEMImg.get_width() / scaleFactor, LEMImg.get_height() / scaleFactor)
)
LEMExhaustImg = pg.image.load("Assets/Exhaust1.png")
LEMexhaustImg = pg.transform.smoothscale(
    LEMExhaustImg,
    (LEMExhaustImg.get_width() / scaleFactor, LEMExhaustImg.get_height() / scaleFactor),
)


def toggleDebug():
    global isDebug
    if isDebug:
        isDebug = False
    else:
        isDebug = True


debugToggleButton = gl.ui.Button(
    {
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
        "clickEventHandler": toggleDebug,
    }
)
#uiElements.append(debugToggleButton)


LEMFuelBar = gl.ui.bar(
    {
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
        "progress": (lem.fuel / lem.maxFuel),
    }
)

hudVelX = gl.ui.Button(
    {
        "surface": uiLayer,
        "type": "button",
        "tag": "hudVX",
        "posX": 2,
        "posY": 85,
        "sizeX": 20,
        "sizeY": 10,
        "anchorSpace": "%",
        "scaleSpace": "%",
        "colour": HudColour,
        "fontColour": fontColour,
        "fontSize": int(fontSize / 1.25),
        "isBold": True,
        "textJusify": "left",
        "text": "VX: ",
        "doesHighlighting": False,
    }
)


hudVelY = gl.ui.Button(
    {
        "surface": uiLayer,
        "type": "button",
        "tag": "hudVY",
        "posX": 2,
        "posY": 73,
        "sizeX": 20,
        "sizeY": 10,
        "anchorSpace": "%",
        "scaleSpace": "%",
        "colour": HudColour,
        "fontColour": fontColour,
        "fontSize": int(fontSize / 1.25),
        "isBold": True,
        "textJusify": "left",
        "text": "VY: ",
        "doesHighlighting": False,
    }
)


hudHeight = gl.ui.Button(
    {
        "surface": uiLayer,
        "type": "button",
        "tag": "hudHeight",
        "posX": 2,
        "posY": 61,
        "sizeX": 20,
        "sizeY": 10,
        "anchorSpace": "%",
        "scaleSpace": "%",
        "colour": HudColour,
        "fontColour": fontColour,
        "fontSize": int(fontSize / 1.25),
        "isBold": True,
        "textJusify": "left",
        "text": "H: ",
        "doesHighlighting": False,
    }
)

def openPrefPath():
    lib.openPath(os.path.join(prefPath, "config.ini"))

#openPrefPath()

def resetGame():
    """
    I hate this function so freaking much
    """

    logging.info("resteting game")
    global \
        lem, \
        lem_copy, \
        camera, \
        camera_copy, \
        inEndScreen, \
        endScreenSetup, \
        mainHasSetup
    global startVX, startVY, startX, startY

    lem = lem_copy # WHY DOESNT THIS WORK???
    camera = camera_copy
    camera.x = camStartX
    camera.y = camStartY
    camera.scale = camStartScale

    print(lem.y)
    print(lem_copy.y)
    lem.vx = startVX
    lem.vy = startVY
    lem.x = startX
    lem.y = startY

    lem.fuel = lem.maxFuel
    lem.throttle = 0

    lem.angle = 270

    inEndScreen = False
    endScreenSetup = False

    uiElements.clear()

    mainHasSetup = False


def main():
    global mainHasSetup
    if not mainHasSetup:
        uiElements.append(LEMFuelBar)
        uiElements.append(hudVelX)
        uiElements.append(hudVelY)
        uiElements.append(hudHeight)
        mainHasSetup = True  # tee hee performace went weee downwards without this

    events()
    # print("eventing")

    if lem.y > -260 and not endScreenSetup:
        global landed
        landed = True

        # calcScore()
        global inEndScreen
        inEndScreen = True
        endScreen()

    if not inEndScreen:
        lem.update(clock)

    #print(lem.y)
    if lem.y > -1000:
        #print("hm")
        camera.scale = 2
        camera.x = lem.x
        camera.y = lem.y + 100

    #camera.x += (LEMImg.get_width() / 2) / camera.scale
    #camera.y += (LEMImg.get_height() / 2) / camera.scale

    camera.update(clock)

    draw()

    clock.tick(FPS)


def draw():
    if isDebug:
        WINDOW.fill((255, 0, 255))  # Obvoius colour to show un rendered area
    else:
        WINDOW.fill(BACKGROUND)

    uiLayer.fill((0, 0, 0, 0))

    drawBackground()

    drawMoonSurface()

    drawLEM()

    drawUI()

    if isDebug:
        Debug.ShowFPS()

    # pg.display.flip()
    pg.display.update()


def drawUI():
    # print(uiElements)
    for element in uiElements:
        if element.type == "bar":
            if element.title == "Fuel:":
                element.progress = lem.fuel / lem.maxFuel
                element.contents = f"{round(lem.fuel)} / {round(lem.maxFuel, 1)}"  # I love stupid hard coded things
                if inEndScreen:
                    continue
        if element.type == "button":
            if element.tag == "hudVX":
                element.text = f"VX: {lem.vx:.2f}"
            if element.tag == "hudVY":
                element.text = f"VY: {lem.vy:.2f}"
            if element.tag == "hudHeight":
                element.text = f"H : {lem.y*-1-260:.0f}"

        # element.text = str(x)
        element.em = rem  # cope future me hahahah
        element.update()

    if inMainMenu:
        WINDOW.blit(menuLayer, (0, 0))

    WINDOW.blit(uiLayer, (0, 0))  # draw final ui to screen


def drawBackground():
    WINDOW.blit(starBackground, (0, 0))


def drawMoonSurface():
    # draw moon
    camera.drawSurf(moonSurf, WINDOW, pg.Rect(- moonSurf.get_width() / 2 + 500, 0, 0, 0))
    


def drawLEM():
    if lem.fuel > 0:
        LEMexhaustImg.set_alpha(255 * (lem.throttle / lem.maxThrottle))
    else:
        LEMexhaustImg.set_alpha(0)

    lemExhaust, exhaustRect = gl.image.rotate(
        LEMexhaustImg, lem.angle, (lem.x, lem.y)
    )

    camera.drawSurf(lemExhaust, WINDOW, exhaustRect)

    lem_rotated_image, lemRect = gl.image.rotate(LEMImg, lem.angle, (lem.x, lem.y))

    #lem_rotated_imageington, lemRectington = gl.image.rotate(LEMImg, lem.angle, (0, 0))

    # lemRect.x -= lem_rotated_image.get_width() / 2
    # lemRect.y -= lem_rotated_image.get_height() / 2
    # The lem is gonna be off center and your gonna like it
    # UPDATE i decided i didnt like it

    camera.drawSurf(lem_rotated_image, WINDOW, lemRect)
    #WINDOW.blit(lem_rotated_imageington, lemRectington)


@lib.timing.logSpeed
def createStarBackground(starSize: int, starChance: int) -> pg.Surface:
    out = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    lineWidth = 1
    circle = pg.image.load("Assets/starBlack.png")
    cat = pg.image.load("Assets/cat.png")
    for x in range(0, WINDOW_WIDTH):
        for y in range(0, WINDOW_HEIGHT):
            a = random.randrange(0, starChance)
            if a == starChance - 1:
                # I should really try to create linse of code that are less long
                # starColour = p.Color((random.randrange(minColourDelta, 255)), (random.randrange(minColourDelta, 255)),(random.randrange(minColourDelta, 255)))
                starColour = gl.image.convert_K_to_RGB(
                    random.triangular(4000, 10000, 5000)
                )

                if not sillyMode: # cant have unoptomised silly mode
                    circle = gl.image.tint(circle, starColour)

                    

                pg.draw.line(
                    out, starColour, (x - starSize, y), (x + starSize, y), lineWidth
                )
                pg.draw.line(
                    out, starColour, (x, y - starSize), (x, y + starSize), lineWidth
                )
                # A circle ends up with an even pixel count, meaning it cannot be centered.
                # p.draw.circle(out, "White", (x, y), size - 3)

                if sillyMode:
                    out.blit(cat, (x - 4, y - 4))
                else:
                    out.blit(circle, (x - 4, y - 4))

    return out


@lib.timing.logSpeed
def createMoonSurface(
    craterSizeMin: int,
    craterSizeMax: int,
    size: tuple,
    craterChance: int,
    moonMedColour,
) -> pg.Surface:
    # This method is very expensive.
    # I could like set it up so it does this once and then like stores the image.
    # Maybe do it on startup for a new user and store it in like appdata/equivilant
    # then each user gets a uniqie surface.
    # it doesnt really matter TBH

    # cr is abreviation for crater

    out = pg.Surface((size))
    pg.draw.rect(out, moonMedColour, ((0, 0), size))

    minColour = 50
    maxColour = 200

    for i in range(0, size[0] * size[1]):
        a = random.randrange(0, craterChance)
        if a == 1:
            x = random.randrange(size[0])
            y = random.randrange(size[1])
            crSize = random.triangular(craterSizeMin, craterSizeMax)
            crColourNum = random.triangular(minColour, maxColour)
            crColour = pg.Color(crColourNum, crColourNum, crColourNum)
            # Main circle
            pg.draw.circle(out, crColour, (x, y), crSize)

            pg.draw.circle(
                out,
                pg.Color(crColourNum - 10, crColourNum - 10, crColourNum - 10),
                (x, y),
                crSize / 1.25,
            )

            subCrMin = int(crSize / 30)
            subCrMax = int(crSize / 10)

            Subcraters = random.randrange(
                subCrMin, subCrMax
            )  # could be proprtional to crater size?
            for k in range(Subcraters):
                subCrColourNum = random.triangular(minColour, maxColour)
                subCrColour = pg.Color(subCrColourNum, subCrColourNum, subCrColourNum)

                ratio = int(crSize / 1.5)

                xOffset = random.randrange(-ratio, ratio)
                yOffset = random.randrange(-ratio, ratio)

                subCrSize = random.triangular(4, crSize / 4)

                pg.draw.circle(out, subCrColour, (x + xOffset, y + yOffset), subCrSize)

                # pg.draw.circle()

    return out


class Debug:
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

        button1 = gl.ui.Button(
            {
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
                "clickEventHandler": on_button1_click,
            }
        )
        uiElements.append(button1)


def events():
    global rem
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            #print("key pressed")
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
                print(uiElements)
                print("wagh!!")
                resetGame()
        if event.type == pg.MOUSEWHEEL:
            camera.scale += camera.scaleSpeed * event.y * camera.scale


def StartGame():
    global inMainMenu
    inMainMenu = False


def mainMenu():
    global hasSetup
    # print("in main meu")
    # print(time.time())

    if not hasSetup:
        global fontObj
        fontObj = pg.font.SysFont("Hack", 15, True)
        # create buttons,
        global menuLayer
        menuLayer = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA, 32)
        menuLayer = menuLayer.convert_alpha()

        # pg.image.save(starBackground, "star.png")

        global StartGameButton
        StartGameButton = gl.ui.Button(
            {
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
                "clickEventHandler": StartGame,
            }
        )
        uiElements.append(StartGameButton)

        global openPrefPathButton
        openPrefPathButton = gl.ui.Button(
            {
                "surface": menuLayer,
                "type": "button",
                "posX": 30,
                "posY": 45,
                "sizeX": 40,
                "sizeY": 10,
                "anchorSpace": "%",
                "scaleSpace": "%",
                "colour": UIColour,
                "fontColour": fontColour,
                "fontSize": fontSize,
                "isBold": True,
                "text": "Open Preferences",
                "clickEventHandler": openPrefPath,
            }
        )
        uiElements.append(openPrefPathButton)

        # TODO options menu maybe maybe

        # title
        titleFont = pg.font.Font("Assets/Moonlander.otf", fontSize * 5)
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
        uiElements.remove(openPrefPathButton)
        StartGameButton = None

    clock.tick(FPS)


def calcScore():
    if lem.angle > 180:
        angFromCenter = 360 - lem.angle
    else:
        angFromCenter = lem.angle

    angScore = -(angFromCenter * 0.2)  ** 2 + 40
    if angScore < 0:
        angScore = 0

    yVelScore = -((lem.vy * 0.32) ** 2 + 10) * 2

    xVelScore = -((lem.vy * 0.75)** 2) + 10

    #fuelScore = (lem.fuel / lem.maxFuel) * 100 * 1.5
    fuelScore = 0

    totalScore = ((angScore + yVelScore + xVelScore) * 5) + fuelScore
    totalScore = int(totalScore * 10000 * 2)

    return totalScore # i sure hope noone cheats and returns like a billion. That would make me sad :( dont do it1!!

def get_humancrytext(totalScore):
    thresholds = {
        0: "Woah thats really really bad :(",
        50: "mmm strawberry jammm mmmmm 😋",
        100: "every single bone is shattered",
        200: "Not every single bone is shattered!",
        300: "Woah you might make it home",
        350: "The landing legs were not crushed!",
        400: "Actually decent!",
        425: "You did a great job!",
        440: "Very well done comrade",
        448: "Pretty much perfect landing!!!!",
        450: "I didnt even think this was possible"
    }

    if totalScore < 0:
        return thresholds[0]

    for threshold, message in sorted(thresholds.items(), reverse=True):
        if totalScore > threshold:
            return message


def endScreen():
    global endScreenSetup
    if not endScreenSetup and inEndScreen:
        totalScore = calcScore()

        humancrytext = ""

        leaderboard.submit_score(scorePostURL, name, totalScore, UU)

        logging.info(f"Total score calcualted is {totalScore}")

        # There has got to be a better way (12898b4d639c55acea50cc9f0fdb513781c09404)
        # Update i found a better way
        humancrytext = get_humancrytext(totalScore)

        global ScoreText  # i am not a fan of this
        ScoreText = gl.ui.Button(
            {
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
                "doesHighlighting": False,
            }
        )
        uiElements.append(ScoreText)

        # - {int(len(str(round(totalScore, 5))) / 2)}
        global ScoreDisplayText
        ScoreDisplayText = gl.ui.Button(
            {
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
                "text": f"{totalScore:^30}" + f"\n {humancrytext:^30}",  # formatting strings is hard okay
                "doesHighlighting": False,
            }
        )
        uiElements.append(ScoreDisplayText)

        global leaderBoardDisplay
        leaderBoardDisplay = gl.ui.Button(
            {
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
                "text": leaderboard.parse(leaderboard.get(scoreGetURL)),
                "doesHighlighting": False,
            }
        )
        uiElements.append(leaderBoardDisplay)
        endScreenSetup = True

    if not inEndScreen and endScreenSetup:
        print("wowah about to delete things!")
        print(f"{inEndScreen} {endScreenSetup}")

        uiElements.remove(ScoreText)
        uiElements.remove(ScoreDisplayText)
        uiElements.remove(leaderBoardDisplay)

        endScreenSetup = False


global starBackground
starBackground = createStarBackground(8, 5000)


running = True


global moonSurf
moonSurf = createMoonSurface(12, 100, (6000, 1000), 10000, moonMedColour)
moonSurf = pg.transform.smoothscale(moonSurf, (moonSurf.get_width() * 2, moonSurf.get_height() * 2))


logging.info(f"Total startup time (s): {time.time()- startTime}")


if __name__ == "__main__":
    while running:
        while inMainMenu:
            mainMenu()
        main()
