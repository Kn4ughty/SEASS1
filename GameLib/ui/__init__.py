import pygame

class Element():
	def __init__(self, surface):
		self.WINDOW = surface

class Rectangle(Element):
	
	def __init__(self, surface, coordSpace: str, posX: int, posY: int, sizeX: int, sizeY: int , Colour: pygame.Color):
		Element.__init__(self, surface)

		match coordSpace:
			case "Center":
				posX = posX - sizeX / 2
				posY = posY - sizeY / 2
		# left, top, width, height
		rect = pygame.Rect(posX, posY, sizeX, sizeY)
	
	def update():
		pygame.draw.rect(self.WINDOW, Colour, rect, width=0)



class Button(Rectangle):

	def __init__(self, Rectangle, fontSize, text: str, style:str = "default", font:str = "default"): #TODO font size type
		Rectangle.__init__(self, Rectangle)
		match style:
			case "default":
				pass
		pass
	#self.surface = Surface
	
	def isMouseOver(self):
		# TODO isMouseOver
		return False

	def isPressed(self):
		# TODO isPressed button
		return False

	def highlight(self):
		match self.style:
			case "default":
				pass
		pass

	def update(self):
		pygame.draw.rect(self.WINDOW, Colour, self.rect, width=0)
		#if isMouseOver():
			#highlight
		#	if isPressed():
				#fire event from Events package
		#		pass

