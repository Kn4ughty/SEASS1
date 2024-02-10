import pygame



def button(WINDOW, mode, posX, posY, sizeX, sizeY, buttonColour):
	match mode:
		case "Center":
			posX = posX - sizeX / 2
			posY = posY - sizeY / 2
		# TODO more modes
	# left, top, width, height
	rect = pygame.Rect(posX, posY, sizeX, sizeY)
	return pygame.draw.rect(WINDOW, buttonColour, rect, width=0)
	# buttonSurface.fill(buttonColour)
