import pygame
import math

class Element():
	"""Generic ui element. Only has a surface"""
	def __init__(self, config):
		self.WINDOW = config["surface"]
		self.Sconfig = config


class Rectangle(Element):
	"""A rectangle UI element

		draws a rectangle, can have transparency and its position
		can be a percentage of its parent surface.
		Every config value with default values:

	"""

	def __init__(self, config):
		Element.__init__(self, config)


		## Coordinate spaces caused problems with percentage anchours so depreicated for now
		## Would end with pos as a small number
		## Could be set up to take into account percentage but idrc
		#match config["coordSpace"]:
		#	case "Center":
		#		config["posX"] -= config["sizeX"] / 2
		#		config["posY"] -= config["sizeY"] / 2
		#	case "TopLeft":
		#		#do nothing
		#		pass


		self.anchorSpace = config.get("anchorSpace", "px")

		match self.anchorSpace:
			case "px":
				#do nothing
				pass
			case "%":
				print(str(self.WINDOW.get_height()))
				if self.WINDOW.get_width() == 0 or self.WINDOW.get_height() == 0:
					print("test")
					raise Exception("surface dimension equals 0 while in percent anchour space" + str(self.WINDOW) + str(config))
				config["posX"] = self.WINDOW.get_width() * (config["posX"] / 100)
				config["posY"] = self.WINDOW.get_height() * (config["posY"] / 100)

		self.scaleSpace = config.get("scaleSpace", "px")

		match self.scaleSpace:
			case "px":
				# do noting
				pass
			case "%":
				# interestingly the scaling is 1px off in this example
				#posX": 10,
    			#"sizeX": 90,
				config["sizeX"] = self.WINDOW.get_width() * (config["sizeX"] / 100)
				config["sizeY"] = self.WINDOW.get_height() * (config["sizeY"] / 100)
				pass



		self.posX = config.get("posX", 0)
		self.posY = config.get("posY", 0)

		self.sizeX = config.get("sizeX", 50)
		self.sizeY = config.get("sizeY", 20)

		self.rect = pygame.Rect(config["posX"], config["posY"], config["sizeX"], config["sizeY"])
		self.colour = config["Colour"]

	def update(self):
		#pygame.draw.rect(self.WINDOW, self.colour, self.rect, width=0)
		self.draw_rect_alpha(self.WINDOW, self.colour, self.rect)
		pass


	def draw_rect_alpha(surface, color, rect):
		shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
		pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
		surface.blit(shape_surf, rect)


class Button(Rectangle):
	"""A button UI element

	Inherits from rectangle
	At its most basic, highlights when mouse is over and runs a function when clicked
	Can have text of varying styles, highlight thickness etc.

	"""

	def __init__(self, config):
		Rectangle.__init__(self, config)
		self.fontSize = config.get("fontSize", 50)
		self.em = self.fontSize
		self.text = config.get("text", "")
		self.style = config.get("style", "default")
		self.font = config.get("font", "Hack")
		self.fontColour = config.get("fontColour", "Black")
		self.isBold = config.get("isBold", True)
		self.isItalic = config.get("isItalic", False)

		self.highlightThickness = config.get("highlightThickness", 0.2)

		self.clickEventHandler = config.get("clickEventHandler", None)

		self.prevMouseState = False
		


	def isMouseOver(self):
		x, y = pygame.mouse.get_pos()
		if x >= self.posX and x <= self.posX + self.sizeX:
			if y >= self.posY and y <= self.posY + self.sizeY:
				return True
		return False


	def highlight(self):
		#match self.style:
		#	case "default":
		outlineColour = pygame.Color(self.colour + pygame.Color(100, 100, 100))
		outlineColour.a = 50
		outlineSurf = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
		pygame.draw.rect(outlineSurf, outlineColour, outlineSurf.get_rect(), math.ceil(self.highlightThickness * self.em))
		self.WINDOW.blit(outlineSurf, self.rect)



	def draw_button_alpha(self, surface, color, rect):
		shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
		pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
		surface.blit(shape_surf, rect)

	def draw(self):
		self.draw_button_alpha(self.WINDOW, self.colour, self.rect)

		font = None
		font = pygame.font.SysFont(self.font, self.fontSize, self.isBold, self.isItalic)
		img = font.render(self.text, True, self.fontColour)

		# this is a very long line of code :/
		# its for centering text btw
		self.WINDOW.blit(img, ((self.posX + ((self.sizeX - img.get_width()) / 2)),(self.posY + ((self.sizeY - img.get_height()) / 2))))

	def update(self):
		#self.fontSize = self.Sconfig["fontSize"]
		self.draw()
		self.em = self.fontSize
		if self.isMouseOver():
			self.highlight()
			if pygame.mouse.get_pressed()[0] == 1 and not self.prevMouseState:
				print("clicked")
				if self.clickEventHandler:
					self.clickEventHandler()
			self.prevMouseState = pygame.mouse.get_pressed()[0] == 1

		#self.draw_button_alpha(self.WINDOW, self.colour, self.rect)
		#pygame.draw.rect(self.WINDOW, self.colour, self.rect, width=0)
		#if isMouseOver():
			#highlight
		#	if isPressed():
				#fire event from Events package
		#		pass


