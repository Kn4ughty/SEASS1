import pygame
import math

class Element():
	def __init__(self, config):
		self.WINDOW = config.get("surface", None)

class Rectangle(Element):
	def __init__(self, config):
		Element.__init__(self, config)

		match config["coordSpace"]:
			case "Center":
				config["posX"] -= config["sizeX"] / 2
				config["posY"] -= config["sizeY"] / 2
		# left, top, width, height

		self.posX = config.get("posX", 0)
		self.posY = config.get("posY", 0)

		self.sizeX = config.get("sizeX", 50)
		self.sizeY = config.get("sizeY", 20)

		self.rect = pygame.Rect(config["posX"], config["posY"], config["sizeX"], config["sizeY"])
		self.colour = config["Colour"]
	
	def update():
		#pygame.draw.rect(self.WINDOW, self.colour, self.rect, width=0)
		draw_rect_alpha(self.WINDOW, self.colour, self.rect)
		pass
	
	#def draw():
	#	s = pygame.Surface((self.sizeX, self.sizeY), pygame.SRCALPHA, 32)
	#	s.fill(self.colour)
	#	return s

	def draw_rect_alpha(surface, color, rect):
		shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
		pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
		surface.blit(shape_surf, rect)

	def rect(screen, x1, y1, x2, y2, alpha = 255):
		#pygame.draw.rect(screen, (0,0,0), (x1,y1,x2,y2))
		draw_rect_alpha(screen, (0, 0, 0, alpha), (x1, y1, x2, y2))



class Button(Rectangle):

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

		self.highlightThickness = config.get("highlightThickness", 0.12)

		self.clickEventHandler = config.get("clickEventHandler", None)

		self.prevMouseState = False
		
		
	#self.surface = Surface
	
	def isMouseOver(self):
		x, y = pygame.mouse.get_pos()
		if x >= self.posX and x <= self.posX + self.sizeX:
			if y >= self.posY and y <= self.posY + self.sizeY:
				#print("mouse over!")
				#print(pygame.mouse.get_pos())
				return True
		#print(pygame.mouse.get_pos())
		return False


	def highlight(self):
		#match self.style:
		#	case "default":
		outlineColour = pygame.Color(self.colour - pygame.Color(10, 10, 10))
		outlineColour.a = 50
		#print(math.ceil(self.highlightThickness * self.em))
		outlineSurf = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
		pygame.draw.rect(outlineSurf, outlineColour, outlineSurf.get_rect(), math.ceil(self.highlightThickness * self.em))
		self.WINDOW.blit(outlineSurf, self.rect)

		

	def draw_button_alpha(self, surface, color, rect):
		shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
		pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
		surface.blit(shape_surf, rect)

	def draw(self):
		self.draw_button_alpha(self.WINDOW, self.colour, self.rect)

		font = pygame.font.SysFont(self.font, self.fontSize, self.isBold, self.isItalic)
		img = font.render(self.text, True, self.fontColour)

		# this is a very long line of code :/
		# its for centering text btw
		self.WINDOW.blit(img, ((self.posX + ((self.sizeX - img.get_width()) / 2)),(self.posY + ((self.sizeY - img.get_height()) / 2))))

	def update(self):
		self.draw()
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


