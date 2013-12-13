import pygame, sys

class Board:

	GRID = [][]
	GRID_WIDTH = 0
	GRID_HEIGHT = 0
	NEIGHBOURS = {-1, 0, 1}

	def __init__(self, board):
		self.GRID = board

	def  neighbours(x,y):
		return [(x+i, y+j) for x in NEIGHBOURS for y in NEIGHBOURS if 0 <= x+i < GRID_WIDTH and 0 <= y+j < GRID_HEIGHT and x ]

	def updateBoard(self, x, y, status):
		self.GRID[x][y] = status

class PyGameBoard:

	def __init__(self, Board, windowWidth, windowHeight):
		self.gridWidth = Board.GRID_WIDTH
		self.gridHeight = Board.GRID_HEIGHT
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.calculateCellSize()

	def calculateCellSize(self):
		self.cellWidth = windowWidth / float(gridWidth)
		self.cellHeight = windowHeight / float(gridHeight)

	def display(self):
		self.DISPLAYSURF = pygame.display.set_mode((windowWidth, windowHeight))
		self.DISPLAYSURF.fill(white)
		self.drawCells()
		pygame.display.update()

	def drawCells(self):
		for x in range(0,windowWidth, cellWidth):
			for y in range(0, windowHeight, cellHeight):
				pygame.draw.line(self.DISPLAYSURF, DARKGRAY,(x,0), (x, windowWidth))
				pygame.draw.line(self.DISPLAYSURF, DARKGRAY, (y,0), (y, windowHeight))


class Game:

	ALIVE = 1
	DEAD = 0

	def __init__(self):
		pass

	def noOfAliveNeighbourCells(self, x,y):
	return sum(neighbours(x,y))

	def cellStatus(self, x,y):
		noOfAliveNeighbours = noOfAliveNeighbours(x,y)
		if noOfAliveNeighbours == 2 or noOfAliveNeighbours == 3:
			return ALIVE
		if noOfAliveNeighbours == 3:
			return ALIVE
		return DEAD