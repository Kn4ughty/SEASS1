import Lib.lib as lib
import pygame


pygame.init()

# Colours
BACKGROUND = (0, 0, 0)

# Game settings
FPS = 60
fpsClock = pygame.time.Clock
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Moonlander 🚀')

title = "\
 _____             _           _         \n\
|     |___ ___ ___| |___ ___ _| |___ ___ \n\
| | | | . | . |   | | .'|   | . | -_|  _|\n\
|_|_|_|___|___|_|_|_|__,|_|_|___|___|_|  \n\
                                         "

t = 0
height = 500
velocity = 50
fuel = 120

lib.clear_terminal()
print(title)

while fuel >= 1 and height > 0:
    print("Time    : {} Height  : {}".format(t, height))
    print("Velocity: {} Fuel    : {}".format(velocity, fuel))



    print("Burn? (0-30)")
    burnAmount = int(input())

    if fuel == 0:
        if burnAmount > fuel:
            burnAmount = fuel

    if burnAmount < 0:
        burnAmount = 0
        print("1")
    elif burnAmount > 30:
        burnAmount = 30
        print("2")
    elif burnAmount > fuel: #140
        burnAmount = fuel
        print("3")
    else:
        print("aa")

    v1 = velocity - burnAmount + 5

    fuel = fuel - burnAmount

    if (v1+velocity)/2 == height: #i dont get it
        fuel = 0
        #goto 220

    height = height - (v1+velocity)/2

    t = t + 1
    velocity = v1

v1 = velocity + (5 - burnAmount)*height/velocity # 220


if v1 > 8:
    print("you died all dead")
elif v1 > 3 and v1 <= 8:
    print("okay but injured")
elif v1 <= 3:
    print("good landing")
    print('hellob this idas me ashely :)')