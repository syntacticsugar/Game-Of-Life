import numpy as np
import time

NEIGHBOURS = {-1, 0, 1}
coordinates = [(i,j) for i in NEIGHBOURS for j in NEIGHBOURS if not (i==0 and j == 0)]
ALIVE = 1
DEAD = 0

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

class Game:

	def __init__(self, board):
		self.board = board
		self.GRID_WIDTH = board.shape[0]
		self.GRID_HEIGHT = board.shape[1]

	def noOfAliveNeighbourCells(self, x,y):
		neighbours_list = self.neighbours(x,y)
		neighbor_values = [self.board[element[0],element[1]] for element in neighbours_list]
		return sum(neighbor_values)

	def neighbours(self, x, y):
		neighbours =  [(x+i, y+j) for i,j in coordinates if (0 <= x+i < self.GRID_WIDTH) and (0 <= y+j < self.GRID_HEIGHT)]
		return neighbours

	def cellStatus(self, x,y):
		aliveNeighbours = self.noOfAliveNeighbourCells(x,y)
		if aliveNeighbours == 3:
			return ALIVE
		if board[x,y] == ALIVE and aliveNeighbours == 2:
			return ALIVE
		return DEAD

	def updateBoard(self):
		newBoard = np.zeros(self.board.shape )
		for x in range(self.GRID_WIDTH):
			for y in range(self.GRID_HEIGHT):
				status = self.cellStatus(x,y)
				newBoard[x,y] = status
		self.board = newBoard
		return self.board

	def __str__(self):
		string_board = ''
		for i in range(self.GRID_WIDTH):
			for j in range(self.GRID_HEIGHT):
				string_board+=self.cell(i,j)
			string_board+="\n"
		return string_board+"\r"
		
	def cell(self,x,y):
		if self.board[x,y] == ALIVE:
			return "X"
		else:
			return "."

if __name__ == '__main__':
	board = pulsar()
	game = Game(board)
	while 1:
		print game
		time.sleep(2)
		game.updateBoard()