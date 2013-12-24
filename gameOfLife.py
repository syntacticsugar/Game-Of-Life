import pygame, sys
import numpy as np
import time


ALIVE = 1
DEAD = 0
NEIGHBOURS = {-1, 0, 1}

diehard = [[0, 0, 0, 0, 0, 0, 1, 0],
	[1, 1, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 1, 1, 1]]

boat = [[1, 1, 0],
	[1, 0, 1],
	[0, 1, 0]]

r_pentomino = [[0, 1, 1],
	[1, 1, 0],
	[0, 1, 0]]

beacon = [[0, 0, 1, 1],
	[0, 0, 1, 1],
	[1, 1, 0, 0],
	[1, 1, 0, 0]]

acorn = [[0, 1, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0],
	[1, 1, 0, 0, 1, 1, 1]]

spaceship = [[0, 0, 1, 1, 0],
	[1, 1, 0, 1, 1],
	[1, 1, 1, 1, 0],
	[0, 1, 1, 0, 0]]

block_switch_engine = [[0, 0, 0, 0, 0, 0, 1, 0],
	[0, 0, 0, 0, 1, 0, 1, 1],
	[0, 0, 0, 0, 1, 0, 1, 0],
	[0, 0, 0, 0, 1, 0, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0],
	[1, 0, 1, 0, 0, 0, 0, 0]]

class Board:

	def __init__(self, board):
		self.GRID = board
		self.GRID_WIDTH = self.GRID.shape[1]
		self.GRID_HEIGHT = self.GRID.shape[0]

	def  neighbours(self, x, y):
		return [(x+i, y+j) for j in NEIGHBOURS for i in NEIGHBOURS if (0 <= x+i < self.GRID_WIDTH) and (0 <= y+j < self.GRID_HEIGHT)]

	def updateCell(self, x, y, status):
		self.GRID[x,y] = status

	@classmethod
	def setup(cls):
		X = np.zeros((6, 21))
		X[2:4, 1:3] = 1
		X[1:4, 5:9] = [[0, 1, 1, 0],
			[1, 0, 0, 1],
			[0, 1, 1, 0]]
		X[1:5, 11:15] = [[0, 1, 1, 0],
			[1, 0, 0, 1],
			[0, 1, 0, 1],
			[0, 0, 1, 0]]
		X[1:4, 17:20] = [[1, 1, 0],
			[1, 0, 1],	
			[0, 1, 0]]
		return cls(X)

	@classmethod
	def setupBlinkerToad(cls):
		blinker = [1, 1, 1]
		toad = [[1, 1, 1, 0],
			[0, 1, 1, 1]]
		X = np.zeros((6, 11))
		X[2, 1:4] = blinker
		X[2:4, 6:10] = toad
		return cls(X)

	@classmethod
	def setupPulsur(cls):
		X = np.zeros((17, 17))
		X[2, 4:7] = 1
		X[4:7, 7] = 1
		X += X.T
		X += X[:, ::-1]
		X += X[::-1, :]
		return cls(X)

	@classmethod
	def setupGluder(cls):
		glider = [[1, 0, 0],
		[0, 1, 1],
		[1, 1, 0]]
		X = np.zeros((8, 8))
		X[:3, :3] = glider
		return cls(X)

	@classmethod
	def setupUnboundedGrowth(cls):
		unbounded = [[1, 1, 1, 0, 1],
		[1, 0, 0, 0, 0],
		[0, 0, 0, 1, 1],
		[0, 1, 1, 0, 1],
		[1, 0, 1, 0, 1]]
		X = np.zeros((30, 40))
		X[15:20, 18:23] = unbounded
		return cls(X)

	@classmethod 
	def setupGliderGun(cls):
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
		return cls(X)

	def __str__(self):
		stringBoard = ''
		for x in range(self.GRID_WIDTH):
			for y in range(self.GRID_HEIGHT):
				stringBoard += self.cellString(x,y)
			stringBoard += '\n'
		return stringBoard

	def cellString(self, x, y):
		print x , y
		cellStatus = self.GRID[x,y]
		if cellStatus == ALIVE:
			return 'X'
		else:
			return '-'

class PyGameBoard:

	def __init__(self, Board, windowWidth, windowHeight):
		self.gridWidth = Board.GRID_WIDTH
		self.gridHeight = Board.GRID_HEIGHT
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.cellWidth = windowWidth / float(gridWidth)
		self.cellHeight = windowHeight / float(gridHeight)

	def display(self):
		self.DISPLAYSURF = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		self.DISPLAYSURF.fill(white)
		self.drawCells()
		pygame.display.update()

	def drawCells(self):
		for x in xrange(0,windowWidth, cellWidth):
			for y in xrange(0, windowHeight, cellHeight):
				pygame.draw.line(self.DISPLAYSURF, DARKGRAY,(x,0), (x, self.windowWidth))
				pygame.draw.line(self.DISPLAYSURF, DARKGRAY, (y,0), (y, self.windowHeight))

class Game:

	def __init__(self, board):
		self.board = board

	def noOfAliveNeighbourCells(self, x,y):
		return len(self.board.neighbours(x,y))

	def cellStatus(self, x,y):
		aliveNeighbours = self.noOfAliveNeighbourCells(x,y)
		if aliveNeighbours == 2 or aliveNeighbours == 3:
			return ALIVE
		if aliveNeighbours == 3:
			return ALIVE
		return DEAD

	def updateBoard(self):
		for x in range(self.board.GRID_WIDTH):
			for y in range(self.board.GRID_HEIGHT):
				status = self.cellStatus(x,y)
				self.board.updateCell(x,y,status)
		return self.board

if __name__ == '__main__':
	board = Board.setupBlinkerToad()
	game = Game(board)
	while 1:
		print board
		time.sleep(5)
		game.updateBoard()