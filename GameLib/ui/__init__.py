import pygame

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
	
	@staticmethod
	def draw_button_alpha(surface, color, rect):
		shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
		pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
		surface.blit(shape_surf, rect)


	def update(self):
		
		self.draw_button_alpha(self.WINDOW, self.colour, self.rect)
		#pygame.draw.rect(self.WINDOW, self.colour, self.rect, width=0)
		#if isMouseOver():
			#highlight
		#	if isPressed():
				#fire event from Events package
		#		pass


