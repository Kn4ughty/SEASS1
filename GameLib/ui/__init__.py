import pygame as pg
import math

# TODO Move these to seperate files


class Element():
	"""Generic ui element. Only has a surface"""
	def __init__(self, config):
		self.SURFACE = config["surface"]


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
				#(str(self.WINDOW.get_height()))
				if self.SURFACE.get_width() == 0 or self.SURFACE.get_height() == 0:
					#print("test")
					# stop cryptic dive by zero
					raise Exception("surface dimension equals 0 while in percent anchour space" + str(self.SURFACE) + str(config))
				config["posX"] = self.SURFACE.get_width() * (config["posX"] / 100)
				config["posY"] = self.SURFACE.get_height() * (config["posY"] / 100)

		self.scaleSpace = config.get("scaleSpace", "px")

		match self.scaleSpace:
			case "px":
				# do noting
				pass
			case "%":
				# interestingly the scaling is 1px off in this example
				#posX": 10,
    			#"sizeX": 90,
				config["sizeX"] = self.SURFACE.get_width() * (config["sizeX"] / 100)
				config["sizeY"] = self.SURFACE.get_height() * (config["sizeY"] / 100)
				pass

		

		self.posX = config.get("posX", 0)
		self.posY = config.get("posY", 0)

		self.sizeX = config.get("sizeX", 50)
		self.sizeY = config.get("sizeY", 20)

		self.width = config.get("width", 0) # Dont see a use but its cool
		self.borderRadius = config.get("borderRadius", 0)

		self.rect = pg.Rect(config["posX"], config["posY"], config["sizeX"], config["sizeY"])
		self.colour = config.get("colour", pg.Color(56, 56, 56))


	def update(self):
		self.draw(self)



	def draw(self):
		shape_surf = pg.Surface(self.rect.size, pg.SRCALPHA)
		pg.draw.rect(shape_surf, self.colour, shape_surf.get_rect(), self.width, self.borderRadius)
		self.SURFACE.blit(shape_surf, self.rect)





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
		self.fontColour = config.get("fontColour", "White")
		self.isBold = config.get("isBold", True)
		self.isItalic = config.get("isItalic", False)

		# Redone here bc i want a different default
		self.borderRadius = config.get("borderRadius", int(self.em / 2))

		self.highlightThickness = config.get("highlightThickness", 0.3)

		self.clickEventHandler = config.get("clickEventHandler", None)

		self.prevMouseState = False
		


	def isMouseOver(self) -> bool:
		x, y = pg.mouse.get_pos()
		if x >= self.posX and x <= self.posX + self.sizeX: #between xleft and xright
			if y >= self.posY and y <= self.posY + self.sizeY: # Between top and bottom
				return True
		return False


	def highlight(self) -> None:
		#match self.style:
		#	case "default":
		outlineColour = pg.Color(self.colour + pg.Color(100, 100, 100))
		outlineColour.a = 50
		outlineSurf = pg.Surface(self.rect.size, pg.SRCALPHA, 32)
		pg.draw.rect(outlineSurf, outlineColour, outlineSurf.get_rect(), math.ceil(self.highlightThickness * self.em), self.borderRadius)
		self.SURFACE.blit(outlineSurf, self.rect)


	def draw(self) -> None:
		Rectangle.draw(self) # poggers no re-written code

		font = None
		font = pg.font.SysFont(self.font, self.fontSize, self.isBold, self.isItalic)
		img = font.render(self.text, True, self.fontColour)

		# this is a very long line of code :/
		# its for centering text btw
		self.SURFACE.blit(img, ((self.posX + ((self.sizeX - img.get_width()) / 2)),(self.posY + ((self.sizeY - img.get_height()) / 2))))

	def update(self) -> None:
		self.draw()
		self.em = self.fontSize
		if self.isMouseOver():
			self.highlight()
			if pg.mouse.get_pressed()[0] == 1 and not self.prevMouseState:
				if self.clickEventHandler:
					self.clickEventHandler()
			self.prevMouseState = pg.mouse.get_pressed()[0] == 1

		#self.draw_button_alpha(self.WINDOW, self.colour, self.rect)
		#pg.draw.rect(self.WINDOW, self.colour, self.rect, width=0)
		#if isMouseOver():
			#highlight
		#	if isPressed():
				#fire event from Events package
		#		pass


class bar(Rectangle):
	""" A progress bar like element
	
	Displays a bar with text over the top,
	has min and max values, bar position is determined by current amount
	Displays text over the top with status

	Display text on top right of element?

	"""

	def __init__(self, config):
		Rectangle.__init__(self, config)

		self.fontSize = config.get("fontSize", 50)
		self.em = self.fontSize
		self.text = config.get("text", "")
		self.style = config.get("style", "default")
		self.font = config.get("font", "Hack")
		self.fontColour = config.get("fontColour", "White")
		self.isBold = config.get("isBold", True)
		self.isItalic = config.get("isItalic", False)

		# Redone here bc i want a different default
		self.borderRadius = config.get("borderRadius", int(self.em / 2))

	def drawBackground(self) -> pg.Surface:
		pass


