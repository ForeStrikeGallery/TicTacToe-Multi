#!/usr/bin/env python3
import pygame
import sys 
from player import Player 
from renderer import Renderer 

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

SIZE = 6

start = WINDOW_WIDTH // (SIZE + 2) 
end = start * (SIZE + 1)

PLAYER_ONE = Player("X")
PLAYER_TWO = Player("O")

curr_player = PLAYER_ONE 

def main():
	global state, screen
	state = [[0 for i in range(SIZE)]  for j in range(SIZE)]	

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

	r = Renderer(screen, SIZE, start, pos, PLAYER_ONE, PLAYER_TWO)

	while True:
		r.drawGrid(state)	
		r.displayHeader()
		r.displayFooter()
		r.drawStretchLines()

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
	curr_player.printInfo()

def getBoxIndex(pos):
	return pos[0] // start - 1,  pos[1] // start - 1
	
				

if __name__ == '__main__':
	main()
