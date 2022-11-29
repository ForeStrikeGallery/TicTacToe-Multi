import pygame 

BLACK = (0, 0, 0) 
WHITE = (200, 185, 229)
# WHITE = (255, 255, 255)

YELLOW = (155, 201, 210)
BLUE = (255, 247, 219)
GREY = WHITE
LINE_COL_P1 = (241, 154, 156)
LINE_COL_P2 = (254, 181, 127)
WINDOW_HEIGHT = 800

WINDOW_WIDTH = 800


class Renderer: 

	def __init__(self, screen, SIZE, blockSize, coords, playerOne, playerTwo): 
		self.SIZE = SIZE 
		self.blockSize = blockSize 
		self.screen = screen	
		self.blockSize = blockSize 
		self.coords = coords 
		self.playerOne = playerOne
		self.playerTwo = playerTwo 

	def drawGrid(self, state):	
		
		for v in self.coords:
			rect = pygame.Rect(v[0], v[1], self.blockSize, self.blockSize) # blocksize = start 
			pygame.draw.rect(self.screen, BLACK, rect, 2)

		for i in range(self.SIZE):
			for j in range(self.SIZE):
				ch = state[i][j]

				if ch == 0:
					continue

				posIndex = i * self.SIZE + j
				pos_x = self.coords[posIndex][0]
				pos_y = self.coords[posIndex][1]

				color = ""
				if ch == "O":
					color = BLUE 
				else:
					color = YELLOW	

				self.renderCell(ch, pos_x, pos_y, color)
		

	def renderCell(self, ch, pos_x, pos_y, color):

		rect = pygame.Rect(pos_x + 2, pos_y + 2, self.blockSize - 4, self.blockSize - 4)
		pygame.draw.rect(self.screen, color, rect, self.blockSize // 2) 	

		font = pygame.font.Font('freesansbold.ttf', 24)
		text = font.render(ch, True, BLACK, color)
		textRect = text.get_rect()
		textRect.center = (pos_x + self.blockSize // 2, pos_y + self.blockSize // 2)
		self.screen.blit(text, textRect)

	def drawStretchLines(self):

		for stretch in self.playerOne.getStretches():
			if len(stretch) > 2:
				
				end_one = stretch[0]
				end_two = stretch[len(stretch) - 1]
				
				start_pos = ((end_one[0] + 1.5) * self.blockSize, (end_one[1] + 1.5) * self.blockSize) 
				end_pos = ((end_two[0] + 1.5) * self.blockSize, (end_two[1] + 1.5) * self.blockSize) 
	 
				pygame.draw.line(self.screen, LINE_COL_P1, start_pos, end_pos, 5) 

		for stretch in self.playerTwo.getStretches():
			if len(stretch) > 2:
				
				end_one = stretch[0]
				end_two = stretch[len(stretch) - 1]
				
				start_pos = ((end_one[0] + 1.5) * self.blockSize, (end_one[1] + 1.5) * self.blockSize) 
				end_pos = ((end_two[0] + 1.5) * self.blockSize, (end_two[1] + 1.5) * self.blockSize) 

				pygame.draw.line(self.screen, LINE_COL_P2, start_pos, end_pos, 5) 


	def displayHeader(self):
		pass 

	def displayFooter(self):
		message = "O: " + str(self.playerOne.getPoints()) + "    X: " + str(self.playerTwo.getPoints())
		font = pygame.font.Font('freesansbold.ttf', 16)

		text = font.render(message, True, BLACK, GREY)
		textRect = text.get_rect()

		textRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - self.blockSize // 2)
		self.screen.blit(text, textRect)
	
