import pygame

class Rectangle(object):
	
	def __init__(self, coordSpace: str, posX: int, posY: int, sizeX: int, sizeY: int , Colour: pygame.Color):
		match coordSpace:
			case "Center":
				posX = posX - sizeX / 2
				posY = posY - sizeY / 2
		# left, top, width, height
		rect = pygame.Rect(posX, posY, sizeX, sizeY)
	
	def update():
		pygame.draw.rect(WINDOW, Colour, rect, width=0)



class Button(Rectangle):

	def __init__(fontSize, text: str, style:str = "default", font:str = "default" ): #TODO font size type
		match style:
			case "default":
				pass
		pass
	
	def isMouseOver():
		# TODO isMouseOver
		return False

	def isPressed():
		# TODO isPressed button
		return False

	def highlight(self):
		match self.style:
			case "default":
				pass
		pass

	def update():
		if isMouseOver():
			#highlight
			if isPressed():
				#fire event from Events package
				pass
	pass
