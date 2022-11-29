import pygame 
import time 
import sys 
from pygame import mixer

BLACK = (0, 0, 0) 
# WHITE = (200, 185, 229)
WHITE = (255, 255, 255)

RED = (155, 201, 210)
BLUE = (255, 247, 219)
GREY = (189, 180, 179)
LINE_COL = (241, 154, 156)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

def main():

	global screen, clock 

	pygame.init()
	pygame.display.set_caption('Fast TicTacToe')
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	clock = pygame.time.Clock()
	screen.fill(GREY)

	global coords
	global state
	
	coords = list()
	state = dict()
	
	global start, end 

	start = int(WINDOW_WIDTH/5)
	end = int(4 * WINDOW_WIDTH/5)

	for x in range(start, end, start):
		for y in range(start, end, start):
			coords.append((x, y))

	global firstPlayerMove
	firstPlayerMove = True 

	font = pygame.font.Font('freesansbold.ttf', 16)

	text = font.render('Press Enter to start game', True, BLACK, GREY)
	textRect = text.get_rect()

	textRect.center = (WINDOW_WIDTH // 2, 20) 
	
	global gameRunning 
	gameRunning = False 
	firstTime = True

	global lastMoveTime
	lastMoveTime = False

	max_time = 1.5

	global winner 
	winner = None

	while True:
		drawTicTacGrid()

		if not gameRunning and firstTime:
			displayOnBanner("Press Enter to start match", GREY)	

		if lastMoveTime and gameRunning:
			cur_time = time.time() - lastMoveTime
			displayOnFooter("%.2f" % cur_time) 
		
			if cur_time > max_time:
				winner = 'Blue' if not firstPlayerMove else 'Yellow'
				display(winner)
				stopGame()

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:		
				if event.key == pygame.K_RETURN:
					gameRunning = True	
					firstTime = False 
					lastMoveTime = time.time()
					screen.fill(WHITE)

			if gameRunning and event.type == pygame.MOUSEBUTTONDOWN:
				boxIndex = findBox(event.pos)

				if withinGrid(event.pos) and boxIndex not in state:
					lastMoveTime = time.time()
					playSound()

					if firstPlayerMove and boxIndex not in state: 
						state[boxIndex] = 'red'		
						firstPlayerMove = False
					elif not firstPlayerMove and boxIndex not in state:
						state[boxIndex] = 'blue'
						firstPlayerMove = True 
					
				winner, row  = findWinner(state)
		
				if winner:
					display(winner)
					stopGame()	
					drawFinishLine(row)	

				if len(state.keys()) == 9:
					displayOnBanner("It's a draw!", WHITE)	
					stopGame()

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

mixer.init()
mixer.music.load("snd_fragment_retrievewav-14728.mp3")

def playSound():
	mixer.music.play()	

def drawFinishLine(row):
	start_pos = ((row[0] // 3 + 1.5) * start, (row[0] % 3 + 1.5) * start)
	end_pos = ((row[2] // 3+ 1.5) * start, (row[2] % 3 + 1.5) * start)  

	pygame.draw.line(screen, LINE_COL, start_pos, end_pos, 5) 

def stopGame():
	drawTicTacGrid()

	global gameRunning 
	global firstPlayerMove

	gameRunning = False 
	promptRestart()
	firstPlayerMove = True

def displayOnBox(message, bgcolor, center_x, center_y):
	font = pygame.font.Font('freesansbold.ttf', 16)
	
	text = font.render(message, True, BLACK, bgcolor)
	textRect = text.get_rect()

	textRect.center = (center_x, center_y)
	screen.blit(text, textRect)


def displayOnBanner(message, bgcolor):
	font = pygame.font.Font('freesansbold.ttf', 16)

	text = font.render(message, True, BLACK, bgcolor)
	textRect = text.get_rect()

	textRect.center = (WINDOW_WIDTH // 2, 20) 
	screen.blit(text, textRect)

def displayOnFooter(message):
	font = pygame.font.Font('freesansbold.ttf', 16)

	text = font.render(message, True, BLACK, WHITE)

	textRect = text.get_rect()

	textRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20) 
		
	screen.blit(text, textRect)



def display(winner):
	if winner == 'red':
		winner = 'Blue'
	elif winner == 'blue':
		winner = 'Yellow'

	displayOnBanner(winner + " wins the match", WHITE) 	

def findWinner(state):

	winning_list = [
		[0,1,2],
		[3,4,5],
		[6,7,8],

		[0,4,8],
		[6,4,2],
		
		[0,3,6],
		[1,4,7],
		[2,5,8]
	]

	reds = [key for key in state if state[key] == 'red']

	blues = [key for key in state if state[key] == 'blue']

	for l in winning_list:
		if set(l).issubset(set(reds)):
			return ('red', l)

		if set(l).issubset(set(blues)):
			return ('blue', l)	

	return (None, None)

def promptRestart():	
	global state 
	state = dict()

def withinGrid(pos):
	print(pos, start)
	res = pos[0] > start and pos[0] < 4 * start and pos[1] > start and pos[1] < 4 * start 
	print(res)
	return res  

def drawBox():
	
	rect = pygame.Rect(50, 50, 40, 40)
	pygame.draw.rect(screen, BLACK, rect, 2)

def findBox(pos):
	
	x = int(pos[0]/start) - 1 
	y = int(pos[1]/start) - 1
	
	return x * 3 + y 

def drawTicTacGrid():

	blockSize =	WINDOW_WIDTH/5	
		
	for x in range(start, end, start):
		for y in range(start, end, start):
			
			rect = pygame.Rect(x, y, blockSize, blockSize)
			pygame.draw.rect(screen, BLACK, rect, 2) 

	## Fill grid with colours

	for key in state: 
		x, y = coords[key]
		rect = pygame.Rect(x + 2, y + 2, blockSize - 4, blockSize - 4)	
	
		if state[key] == 'red':
			pygame.draw.rect(screen, RED, rect, int(start/2))
			displayOnBox("X", RED, x + start//2, y + start//2)
		else:
			pygame.draw.rect(screen, BLUE, rect, int(start/2))
			displayOnBox("O", BLUE, x + start // 2, y + start // 2)

def drawGrid():
	blockSize = 40

	for x in range(0, WINDOW_WIDTH, blockSize):
		for y in range(0, WINDOW_HEIGHT, blockSize):
			rect = pygame.Rect(x, y, blockSize, blockSize)
			pygame.draw.rect(screen, BLACK, rect, 1)	

if __name__ == '__main__':
	main()





