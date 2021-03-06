import random
import math
import numpy
from copy import copy, deepcopy

#Cell properties
#state can be uncovered, mined, or clear
#mine property is whether or not the cell has a mine
#Note, X is vertical, Y is horizontal
#nei represents actual number of Neighbor mines, defaults to 0
#neiSafe, neiHidden, and neiMine are the Knowledge Base conclusions of the agent(number of safe/hidden/mine confirmations) around the specific cell
#cellX, cellY is used for UI purposes
class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.state = 'uncovered'
        self.mine = False
        self.nei = 0
        self.neiSafe = None
        self.neiHidden = None
        self.neiMine = None
        self.cellX= None
        self.cellY= None

#Generate a mine sweeper board, takes in d the dimension size, and n, the number of mines
#Board is 2d Array of Cells, after making the 2d array of cells, it will insert the mines based on n and update the cells to include the actual number of neighbor cells
def generateBoard(d,n):
    board = []
    #Create Board of x and y
    for x in range(d):
        board2 = []
        for y in range(d):
            board2.append(Cell(x,y))
        board.append(board2)
    #total Cells
    totalCells = d*d
    #Generate mines
    minePlacement = random.sample(range(1,totalCells),n)
    #insert the mines based on mine placement
    counter = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if counter in minePlacement:
                board[i][j].mine = True
            counter = counter + 1
    #Updates the neighbors based on mine count
    updateAllNei(board)
    return board

#Print out current board based on mines, takes in the board and its size
#0 is no mine, 1 is mine
def printBoard(board,n):
    tmp = []
    for row in board:
        tmp2 = []
        cellCounter = 0
        while cellCounter < 9:
            if row[cellCounter].mine == False:
                tmp2.append(0)
            if row[cellCounter].mine == True:
                tmp2.append(1)
            cellCounter = cellCounter + 1
        tmp.append(tmp2)
    for row in tmp:
        print(row)

#Changes Cell state, takes in a cell and the state you want to change
#s is string of state, uncovered, cleared, mined
def changeState(x,s):
    x.state = s

#Checks surrounding area for mines and returns the number
#takes in the board, and the coordinate of the cell you want to examine
#Note this is the actual number of mines, not revealed
def checkMine(board,x,y):
    counter = 0
    if x != 0:
        if board[x-1][y].mine == True:
            counter = counter + 1
    if y != 0:
        if board[x][y-1].mine == True:
            counter = counter + 1
    if y < len(board)-1:
        if board[x][y+1].mine == True:
            counter = counter + 1
    if x < len(board)-1:
        if board[x+1][y].mine == True:
            counter = counter + 1
    if x != 0 and y < len(board)-1:
        if board[x-1][y+1].mine == True:
            counter = counter + 1
    if x < len(board) - 1 and y != 0:
        if board[x+1][y-1].mine == True:
            counter = counter + 1
    if x != 0 and y != 0:
        if board[x-1][y-1].mine == True:
            counter = counter + 1
    if x < len(board)-1 and y < len(board)-1:
        if board[x+1][y+1].mine == True:
            counter = counter + 1
    board[x][y].nei = counter

#Checks surrounding area for Revealed or Flagged mines, not actual and returns the number
#takes in the board, and the coordinate of the cell you want to examine
def checkNeiMine(board,x,y):
    counter = 0
    if x != 0:
        if board[x-1][y].state == 'mined':
            counter = counter + 1
    if y != 0:
        if board[x][y-1].state == 'mined':
            counter = counter + 1
    if y < len(board)-1:
        if board[x][y+1].state == 'mined':
            counter = counter + 1
    if x < len(board)-1:
        if board[x+1][y].state == 'mined':
            counter = counter + 1
    if x != 0 and y < len(board)-1:
        if board[x-1][y+1].state == 'mined':
            counter = counter + 1
    if x < len(board) - 1 and y != 0:
        if board[x+1][y-1].state == 'mined':
            counter = counter + 1
    if x != 0 and y != 0:
        if board[x-1][y-1].state == 'mined':
            counter = counter + 1
    if x < len(board)-1 and y < len(board)-1:
        if board[x+1][y+1].state == 'mined':
            counter = counter + 1
    board[x][y].neiMine = counter


#Checks surrounding area for Safe cells confirmed and revealed and returns the number
#takes in the board, and the coordinate of the cell you want to examine
def checkNeiSafe(board,x,y):
    counter = 0
    if x != 0:
        if board[x-1][y].state == 'clear':
            counter = counter + 1
    if y != 0:
        if board[x][y-1].state == 'clear':
            counter = counter + 1
    if y < len(board)-1:
        if board[x][y+1].state == 'clear':
            counter = counter + 1
    if x < len(board)-1:
        if board[x+1][y].state == 'clear':
            counter = counter + 1
    if x != 0 and y < len(board)-1:
        if board[x-1][y+1].state == 'clear':
            counter = counter + 1
    if x < len(board) - 1 and y != 0:
        if board[x+1][y-1].state == 'clear':
            counter = counter + 1
    if x != 0 and y != 0:
        if board[x-1][y-1].state == 'clear':
            counter = counter + 1
    if x < len(board)-1 and y < len(board)-1:
        if board[x+1][y+1].state == 'clear':
            counter = counter + 1
    board[x][y].neiSafe = counter

#Checks surrounding area for Hidden neighbors(cells not yet touched or mined) and returns the number
#takes in the board, and the coordinate of the cell you want to examine
def checkNeiHidden(board,x,y):
    counter = 0
    if x != 0:
        if board[x-1][y].state == 'uncovered':
            counter = counter + 1
    if y != 0:
        if board[x][y-1].state == 'uncovered':
            counter = counter + 1
    if y < len(board)-1:
        if board[x][y+1].state == 'uncovered':
            counter = counter + 1
    if x < len(board)-1:
        if board[x+1][y].state == 'uncovered':
            counter = counter + 1
    if x != 0 and y < len(board)-1:
        if board[x-1][y+1].state == 'uncovered':
            counter = counter + 1
    if x < len(board) - 1 and y != 0:
        if board[x+1][y-1].state == 'uncovered':
            counter = counter + 1
    if x != 0 and y != 0:
        if board[x-1][y-1].state == 'uncovered':
            counter = counter + 1
    if x < len(board)-1 and y < len(board)-1:
        if board[x+1][y+1].state == 'uncovered':
            counter = counter + 1
    board[x][y].neiHidden = counter


#Update all Hidedenneighbors to be a be safe or a Mine
#Upon drawing a solid conclusion(basic agent), takes in the board, the coordinates x and y, and a state to change the surrounding cells (z)
#all surrounding cells state will be changed to that, returns the new board
def updateResult(board,x,y,z):
    if x != 0 and board[x-1][y].state == 'uncovered':
        board[x-1][y].state = z
    if y != 0 and board[x][y-1].state == 'uncovered':
        board[x][y-1].state = z
    if y < len(board)-1 and board[x][y+1].state == 'uncovered':
        board[x][y+1].state = z
    if x < len(board)-1 and board[x+1][y].state == 'uncovered':
        board[x+1][y].state = z
    if x != 0 and y < len(board)-1 and board[x-1][y+1].state == 'uncovered':
        board[x-1][y+1].state = z
    if x < len(board) - 1 and y != 0 and board[x+1][y-1].state == 'uncovered':
        board[x+1][y-1].state = z
    if x != 0 and y != 0 and board[x-1][y-1].state == 'uncovered':
        board[x-1][y-1].state = z
    if x < len(board)-1 and y < len(board)-1 and board[x+1][y+1].state == 'uncovered' :
        board[x+1][y+1].state = z
    return board


#Update the neighbor values of all Cells
#Used when generating the board, takes in the board, updates so all cells will have the correct number of actual mines surrounding it
def updateAllNei(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            checkMine(board,i,j)

#A Basic agent to play minesweeper
def basicAI(board):
    confirmation = False
    kb = deepcopy(board)
    #If mine neighbors = hidden neighbors, all hidden neighbors are mines
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            checkNeiMine(kb,i,j)
            checkNeiHidden(kb,i,j)
            if kb[i][j].state == 'clear' and kb[i][j].nei - kb[i][j].neiMine == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                confirmation = True
                print('p1')
                board = updateResult(board,i,j,'mined')
    #If 8-Clue minus number of safe neighbors is hidden neighbors, all neighbors are safe
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            checkMine(kb,i,j)
            checkNeiSafe(kb,i,j)
            checkNeiHidden(kb,i,j)
            if kb[i][j].state == 'clear' and 8 - kb[i][j].nei - kb[i][j].neiSafe  == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                print(i)
                print(j)
                print(kb[i][j].nei)
                print(kb[i][j].neiSafe)
                print(kb[i][j].neiHidden)

                print('p2')
                confirmation = True
                board =  updateResult(board,i,j,'clear')
    #Choose a Cell at random to flip
    if confirmation == False:
        print('p3')
        counter = 0
        for i in range(len(kb)):
            for j in range(len(kb[i])):
                if kb[i][j].state == 'uncovered':
                    counter = counter + 1
        rand = random.randint(1,counter)
        counter = 0
        for i in range(len(kb)):
            for j in range(len(kb[i])):
                counter = counter + 1
                if kb[i][j].state == 'uncovered' and counter == rand:
                    board[i][j].state = 'clear'

    return board


tmp = generateBoard(9,10)



