import pygame

class Element():
	def __init__(self, surface):
		self.WINDOW = surface

class Rectangle(Element):
	
	def __init__(self, surface, config):
		Element.__init__(self, surface)

		match config["coordSpace"]:
			case "Center":
				config["posX"] -= config["sizeX"] / 2
				config["posY"] -= config["sizeY"] / 2
		# left, top, width, height

		self.rect = pygame.Rect(config["posX"], config["posY"], config["sizeX"], config["sizeY"])
		self.colour = config["Colour"]
	
	def update():
		pygame.draw.rect(self.WINDOW, self.colour, self.rect, width=0)



class Button(Rectangle):

	def __init__(self, surface, config):
		Rectangle.__init__(self, surface, config)
		self.fontSize = config.get("fontSize", 12)
		self.text = config.get("text", "")
		self.style = config.get("style", "default")
		self.font = config.get("font", "default")
		
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
		pygame.draw.rect(self.WINDOW, self.colour, self.rect, width=0)
		#if isMouseOver():
			#highlight
		#	if isPressed():
				#fire event from Events package
		#		pass

