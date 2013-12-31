import numpy as np
import time
import pygame, sys

NEIGHBOURS = {-1, 0, 1}
coordinates = [(i,j) for i in NEIGHBOURS for j in NEIGHBOURS if not (i==0 and j == 0)]

WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)

def pulsar():
	X = np.zeros((17, 17))
	X[2, 4:7] = 1
	X[4:7, 7] = 1
	X += X.T
	X += X[:, ::-1]
	X += X[::-1, :]
	return X

def setupBlinkerToad():
	blinker = [1, 1, 1]
	toad = [[1, 1, 1, 0],
		[0, 1, 1, 1]]
	X = np.zeros((6, 11))
	X[2, 1:4] = blinker
	X[2:4, 6:10] = toad
	return X

def setupBlinker():
	blinker = [1, 1, 1]
	X = np.zeros((3, 3))
	X[1, 0:3] = blinker
	return X

def setupGlider():
	glider = [[1, 0, 0],
	          [0, 1, 1],
	          [1, 1, 0]]
	X = np.zeros((8, 8))
	X[:3, :3] = glider
	return X

def setupUnbounded():
	unbounded = [[1, 1, 1, 0, 1],
	             [1, 0, 0, 0, 0],
	             [0, 0, 0, 1, 1],
	             [0, 1, 1, 0, 1],
	             [1, 0, 1, 0, 1]]
	X = np.zeros((30, 40))
	X[15:20, 18:23] = unbounded
	return X

def setupGliderGun():
	glider_gun =\
	[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
	 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
	 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
	 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
	 [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	 [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
	 [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
	 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	X = np.zeros((50, 70))
	X[1:10,1:37] = glider_gun
	return X

class Game:

	def __init__(self, board):
		self.board = board
		self.GRID_WIDTH = board.shape[1]
		self.GRID_HEIGHT = board.shape[0]

	def noOfAliveNeighbourCells(self, x,y):
		neighbours_list = self.neighbours(x,y)
		return sum([self.board[element[0],element[1]] for element in neighbours_list])

	def neighbours(self, x, y):
		return [(y+j, x+i) for i,j in coordinates if (0 <= x+i < self.GRID_WIDTH) and (0 <= y+j < self.GRID_HEIGHT)]

	def cellStatus(self, x,y):
		aliveNeighbours = self.noOfAliveNeighbourCells(x,y)
		return aliveNeighbours == 3 or (board[y,x] and aliveNeighbours == 2)

	def updateBoard(self):
		newBoard = np.zeros(self.board.shape )
		for x in range(self.GRID_WIDTH):
			for y in range(self.GRID_HEIGHT):
				newBoard[y,x] = self.cellStatus(x,y)
		self.board = newBoard
		return self.board

	def __str__(self):
		string_board = ''
		for j in range(self.GRID_HEIGHT):
			for i in range(self.GRID_WIDTH):		
				string_board+=self.cell(i,j)
			string_board+="\n"
		return string_board+"\r"
		
	def cell(self,x,y):
		if self.board[y,x]:
			return "X"
		else:
			return "."

class PyGameBoard:

	cellSize = 10
	
	def __init__(self, board):
		self.gridWidth = board.shape[1]
		self.gridHeight = board.shape[0]
		self.windowWidth = self.cellSize*board.shape[1]
		self.windowHeight = self.cellSize*board.shape[0]
		pygame.init()
		self.DISPLAYSURF = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		pygame.display.set_caption('Game of Life')
		self.backgroundColour = BLACK
		self.DISPLAYSURF.fill(self.backgroundColour)
		pygame.display.update()

	def boardToFillCells(self, board):
		for y in xrange(self.gridHeight):
			for x in xrange(self.gridWidth):
				self.fillCell(x,y, self.backgroundColour)
				if board[y,x]:
					self.fillCell(x,y, RED)
		pygame.display.update()

	def fillCell(self, cell_x, cell_y, colour):
		self.DISPLAYSURF.fill(colour, pygame.Rect(cell_x*self.cellSize, cell_y*self.cellSize, self.cellSize, self.cellSize))

if __name__ == '__main__':
	board = setupBlinkerToad()
	game = Game(board)
	pyBoard = PyGameBoard(board)
	
	done = False
	clock = pygame.time.Clock()
	
	while not done:
		clock.tick(10)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done=True 
		
		game.updateBoard()
		pyBoard.boardToFillCells(game.board)
