import pygame
import sys 

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

SIZE = 5

start = WINDOW_WIDTH // (SIZE + 2) 
end = start * (SIZE + 1)


class Player:
		
	def __init__(self, symbol):
		self.points = 0
		self.stretches = list()
		self.symbol = symbol

	def getSymbol(self):
		return self.symbol

	def getPoints(self):
		return self.points
	
	def getStretches(self):
		return self.stretches
		
	def reset(self):
		self.points = 0
		self.stretches = list()

	def addBox(self, x, y):	
		
		updatedStretches = list()
		sizeTwoStretches = list()
		sizeOneStretches = list()

		for stretch in self.stretches:
			s = fitIfPossible((x, y), stretch)
			print("fit if possible: ", s)

			if s:
				if len(s) == 2:
					sizeTwoStretches.append((stretch, s))	
					sizeOneStretches.append(stretch)
					continue
				updatedStretches.append(s)
			else:
				updatedStretches.append(stretch)	

		print("size two ", sizeTwoStretches)
		print("updated stretch", updatedStretches)

		filteredSizeTwo = list()
		
		for k in sizeTwoStretches:
			val = k[0][0]

			flag = True 
			for s in stretch:
				if val in s:
					flag = False
					break

			if flag:
				filteredSizeTwo.append(k[1])

		print("filtered size two ", filteredSizeTwo)
		updatedStretches.append([(x, y)])
		updatedStretches.extend(filteredSizeTwo)
		updatedStretches.extend(sizeOneStretches)
		self.stretches = updatedStretches
		
		self.updatePoints()

	def updatePoints(self):

		self.points = 0 
		for stretch in self.stretches:
			if len(stretch) < 3:
				continue

			self.points += (len(stretch) - 2) * 2 - 1

	def printInfo(self):
		print("Points: ", self.points)

PLAYER_ONE = Player("X")
PLAYER_TWO = Player("O")

curr_player = PLAYER_ONE 

def fitIfPossible(pos, stretch):

	result = stretch.copy()
	result.append(pos)
	if validStretch(result):
		return result 

	result = stretch.copy()
	result.insert(0, pos)
	if validStretch(result):
		return result

	return None 

def validStretch(stretch):
	if (len(stretch)) == 1:
		return True 

	print(stretch)
	diff_x = stretch[0][0] - stretch[1][0]
	diff_y = stretch[0][1] - stretch[1][1]

	if abs(diff_x) > 1 or abs(diff_y) > 1:
		return False

	for i in range(1, len(stretch) - 1):
		if stretch[i][0] - stretch[i+1][0] != diff_x:
			return False

		if stretch[i][1] - stretch[i+1][1] != diff_y:
			return False

	return True 
		 
		
def main():
	global state, screen
	state = [[0 for i in range(SIZE)]  for j in range(SIZE)]	
	print(state)

	pygame.init()

	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	screen.fill(GREY)

	global pos 
	pos = list()

	global curr_player
	curr_player = PLAYER_ONE 

	for x in range(start, end, start):
		for y in range(start, end, start):
			pos.append((x, y))

	while True:
		drawGrid()	
		displayHeader()
		displayFooter()
		drawFinishLine()

		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	
				pygame.quit()
				sys.exit()	

			if event.type == pygame.MOUSEBUTTONDOWN:
				handleClick(event.pos)

			if event.type == pygame.KEYDOWN:		
				if event.key == pygame.K_RETURN:
					resetGame()

def resetGame():
	global state 
	state = [[0 for i in range(SIZE)]  for j in range(SIZE)]	
 
	PLAYER_ONE.reset()
	PLAYER_TWO.reset()

	screen.fill(GREY)	

def drawFinishLine():

	for stretch in PLAYER_ONE.getStretches():
		if len(stretch) > 2:
			
			end_one = stretch[0]
			end_two = stretch[len(stretch) - 1]
			
			start_pos = ((end_one[0] + 1.5) * start, (end_one[1] + 1.5) * start) 
			end_pos = ((end_two[0] + 1.5) * start, (end_two[1] + 1.5) * start) 
 
			pygame.draw.line(screen, LINE_COL_P1, start_pos, end_pos, 5) 

	for stretch in PLAYER_TWO.getStretches():
		if len(stretch) > 2:
			
			end_one = stretch[0]
			end_two = stretch[len(stretch) - 1]
			
			start_pos = ((end_one[0] + 1.5) * start, (end_one[1] + 1.5) * start) 
			end_pos = ((end_two[0] + 1.5) * start, (end_two[1] + 1.5) * start) 
 
			pygame.draw.line(screen, LINE_COL_P2, start_pos, end_pos, 5) 


def displayHeader():
	pass 

def displayFooter():
	message = "O: " + str(PLAYER_ONE.getPoints()) + "    X: " + str(PLAYER_TWO.getPoints())
	font = pygame.font.Font('freesansbold.ttf', 16)

	text = font.render(message, True, BLACK, GREY)
	textRect = text.get_rect()

	textRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - start // 2)
	screen.blit(text, textRect)
				
def switchCurPlayer():
	global curr_player

	if curr_player == PLAYER_ONE:
		curr_player = PLAYER_TWO
	else:
		curr_player = PLAYER_ONE

def handleClick(pos):
	
	x, y = getBoxIndex(pos)
	
	if x < 0 or y < 0 or x >= SIZE or y >= SIZE:
		return 

	if state[x][y] == 0:
		state[x][y] = curr_player.getSymbol()
		switchCurPlayer()

	curr_player.addBox(x, y) 
	print(state)
	curr_player.printInfo()

def getBoxIndex(pos):
	return pos[0] // start - 1,  pos[1] // start - 1
	
def drawGrid():	
		
	blockSize = start 
	for v in pos:
		rect = pygame.Rect(v[0], v[1], blockSize, blockSize) # blocksize = start 
		pygame.draw.rect(screen, BLACK, rect, 2)

	for i in range(SIZE):
		for j in range(SIZE):
			ch = state[i][j]

			if ch != 0:
				posIndex = i * SIZE + j
				pos_x = pos[posIndex][0]
				pos_y = pos[posIndex][1]

				color = ""
				if ch == "O":
					color = BLUE 
				else:
					color = YELLOW	
		
				rect = pygame.Rect(pos_x + 2, pos_y + 2, blockSize - 4, blockSize - 4)
				pygame.draw.rect(screen, color, rect, blockSize // 2) 	


				font = pygame.font.Font('freesansbold.ttf', 24)

				text = font.render(ch, True, BLACK, color)

				textRect = text.get_rect()

				textRect.center = (pos_x + blockSize // 2, pos_y + blockSize // 2)
				screen.blit(text, textRect)
					

if __name__ == '__main__':
	main()
