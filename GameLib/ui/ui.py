import pygame
from GameLib import WINDOW


def button(mode, posX, posY, sizeX, sizeY, buttonColour):
	match mode:
		case "Center":
			posX = posX - sizeX / 2
			posY = posY - sizeY / 2
	# left, top, width, height
	raa = pygame.Rect(posX, posY, sizeX, sizeY)
	pygame.draw.rect(WINDOW, buttonColour, raa, width=0)
	# buttonSurface.fill(buttonColour)
