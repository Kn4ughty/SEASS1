import pygame
import ui

running = True
clock = pygame.time.Clock()
pygame.display.set_caption('Mobile phone')

print("Test")


WIDTH, HEIGHT = 200, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

CenterX = WIDTH / 2
CenterY = HEIGHT / 2

Center = pygame.Vector2(CenterX, CenterY)
def main():
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		WIN.fill("white")

		# pygame.draw.circle(WIN, "blue", Center, 100)
	
	
		ui.button("Center", CenterX, CenterY, 100, 20, "blue")
	
		pygame.display.flip()
		clock.tick(60)  # limits FPS to 60
	

	pygame.quit()
