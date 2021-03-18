import random
import math
import numpy
from copy import copy, deepcopy
from itertools import combinations

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
        self.neiBoom = None
        self.cellX= None
        self.cellY= None
        self.safety = True


class Changes:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.change = None


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
        if board[x-1][y].state == 'clear' and board[x-1][y].mine == False:
            counter = counter + 1
    if y != 0:
        if board[x][y-1].state == 'clear' and board[x][y-1].mine == False:
            counter = counter + 1
    if y < len(board)-1:
        if board[x][y+1].state == 'clear' and board[x][y+1].mine == False:
            counter = counter + 1
    if x < len(board)-1:
        if board[x+1][y].state == 'clear' and board[x+1][y].mine == False:
            counter = counter + 1
    if x != 0 and y < len(board)-1:
        if board[x-1][y+1].state == 'clear' and board[x-1][y+1].mine == False:
            counter = counter + 1
    if x < len(board) - 1 and y != 0:
        if board[x+1][y-1].state == 'clear' and board[x+1][y-1].mine == False:
            counter = counter + 1
    if x != 0 and y != 0:
        if board[x-1][y-1].state == 'clear' and board[x-1][y-1].mine == False:
            counter = counter + 1
    if x < len(board)-1 and y < len(board)-1:
        if board[x+1][y+1].state == 'clear' and board[x+1][y+1].mine == False:
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

#For our special version of Minesweeper which allows the agent to keep going
#Checks surrounding area for number of mines that went boom
#takes in the board, and the coordinate of the cell you want to examine
def checkNeiBoom(board,x,y):
    counter = 0
    if x != 0:
        if board[x-1][y].state == 'clear' and board[x-1][y].mine == True:
            counter = counter + 1
    if y != 0:
        if board[x][y-1].state == 'clear' and board[x][y-1].mine == True:
            counter = counter + 1
    if y < len(board)-1:
        if board[x][y+1].state == 'clear' and board[x][y+1].mine == True:
            counter = counter + 1
    if x < len(board)-1:
        if board[x+1][y].state == 'clear' and board[x+1][y].mine == True:
            counter = counter + 1
    if x != 0 and y < len(board)-1:
        if board[x-1][y+1].state == 'clear' and board[x-1][y+1].mine == True:
            counter = counter + 1
    if x < len(board) - 1 and y != 0:
        if board[x+1][y-1].state == 'clear' and board[x+1][y-1].mine == True:
            counter = counter + 1
    if x != 0 and y != 0:
        if board[x-1][y-1].state == 'clear' and board[x-1][y-1].mine == True:
            counter = counter + 1
    if x < len(board)-1 and y < len(board)-1:
        if board[x+1][y+1].state == 'clear' and board[x+1][y+1].mine == True:
            counter = counter + 1
    board[x][y].neiBoom = counter

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
            checkNeiBoom(kb,i,j)
            if kb[i][j].state == 'clear' and kb[i][j].nei - kb[i][j].neiMine - kb[i][j].neiBoom == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                confirmation = True
                #print('p1')
                board = updateResult(board,i,j,'mined')
    #If 8-Clue minus number of safe neighbors is hidden neighbors, all neighbors are safe
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            checkMine(kb,i,j)
            checkNeiSafe(kb,i,j)
            checkNeiHidden(kb,i,j)
            if kb[i][j].state == 'clear' and 8 - kb[i][j].nei - kb[i][j].neiSafe  == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                #print('p2')
                confirmation = True
                board =  updateResult(board,i,j,'clear')
    #Choose a Cell at random to flip
    if confirmation == False:
        #print('p3')
        counter = 0
        for i in range(len(kb)):
            for j in range(len(kb[i])):
                if kb[i][j].state == 'uncovered':
                    counter = counter + 1
        rand = random.randint(1,counter)
        counter = 0
        for i in range(len(kb)):
            for j in range(len(kb[i])):
                if kb[i][j].state == 'uncovered':
                    counter = counter + 1
                    if counter == rand:
                        board[i][j].state = 'clear'
    return board



#An improved agent to play minesweeper
#Constraint Satisfaction Approach? 
#Keep basic AI logic, add CSP logic, when no definitive solution, go random
def improvedAI(board):
    confirmation = False
    kb = deepcopy(board)
    #Guarantee Cases of Basic Mines
    #If mine neighbors = hidden neighbors, all hidden neighbors are mines
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            checkNeiMine(kb,i,j)
            checkNeiHidden(kb,i,j)
            checkNeiBoom(kb,i,j)
            if kb[i][j].state == 'clear' and kb[i][j].nei - kb[i][j].neiMine - kb[i][j].neiBoom == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                confirmation = True
                board = updateResult(board,i,j,'mined')
    #If 8-Clue minus number of safe neighbors is hidden neighbors, all neighbors are safe
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            checkMine(kb,i,j)
            checkNeiSafe(kb,i,j)
            checkNeiHidden(kb,i,j)
            if kb[i][j].state == 'clear' and 8 - kb[i][j].nei - kb[i][j].neiSafe  == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                confirmation = True
                board =  updateResult(board,i,j,'clear')
    #Constraint Satisfaction Cases?
    #hypothetical, rn, fill up mines based on clues randomly that satisfy constraints, then work in that direction
 
    if confirmation == False:
        kb2 = deepcopy(board)
        #print(generateSolutions(kb2))
        boole, kb2 = generateSolutions(kb2)
        #No Optimal solution found, select a cell at random
        if boole == False:
            #print('no Opt')
          #Choose Cell at Random
            counter = 0
            for i in range(len(kb)):
                for j in range(len(kb[i])):
                    if kb[i][j].state == 'uncovered':
                        counter = counter + 1
            rand = random.randint(1,counter)
            counter = 0
            for i in range(len(kb)):
                for j in range(len(kb[i])):
                    if kb[i][j].state == 'uncovered':
                        counter = counter + 1
                        if counter == rand:
                            board[i][j].state = 'clear'
        elif boole == True:
            # Choose Cell thats safe in CSF solution
            counter = 0
            iList = []
            jList = []
            for i in range(len(kb2)):
                for j in range(len(kb2[i])):
                    checkNeiSafe(kb2,i,j)
                    checkNeiMine(kb2,i,j)
                    if kb2[i][j].state == 'uncovered' and kb2[i][j].neiSafe + kb2[i][j].neiMine > 1 and kb2[i][j].safety == True:
                        counter = counter + 1
                        iList.append(i)
                        jList.append(j)
            if counter == 0:
                # go random?
                counter = 0
                for i in range(len(kb)):
                    for j in range(len(kb[i])):
                        if kb[i][j].state == 'uncovered':
                            counter = counter + 1
                rand = random.randint(1,counter)
                counter = 0
                for i in range(len(kb)):
                    for j in range(len(kb[i])):
                        if kb[i][j].state == 'uncovered':
                            counter = counter + 1
                            if counter == rand:
                                board[i][j].state = 'clear'
            else:
                rand = random.randint(1,counter)
                counter = 0
                for i in range(len(iList)):
                    for j in range(len(jList)):
                        counter = counter + 1
                        if counter == rand:
                            board[iList[i]][jList[j]].state = 'clear'

    return board

#Based on Cell information, generate solutions
#if can find a solution that satisfies constraints, return true and the board
#otherwise, return false
def generateSolutions(board):
    #create copy for temp solution that satisfies constraints
    kb = deepcopy(board)
    validOptions = []
    #For each constraint, check current number of mined/clear+boom
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            if kb[i][j].state == 'clear' and kb[i][j].mine == False:
                checkNeiBoom(kb,i,j)
                checkNeiMine(kb,i,j)
                mineCount = kb[i][j].neiBoom + kb[i][j].neiMine
                if mineCount < kb[i][j].nei:
                    diff = kb[i][j].nei - mineCount
                    validOptions.append(generateValidChildren(kb,i,j,diff))
 
    numb = len(validOptions)
    for c in range(numb):
        kb = deepcopy(board)
        kb2 = deepcopy(board)
        numb2 = len(validOptions[c])
        for d in range(numb2):
            kb = applyChanges(kb,validOptions[c][d])
            kb2 = applySafety(kb2,validOptions[c][d])
        if checkConstraint(kb) == True:
            return True, kb2
    return False, board



#Apply changes of changes found that hopefully will not break constraint
def applySafety(board, x):
    if x.change == 'left':
        board[x.x-1][x.y].safety = False
    elif x.change == 'down':
        board[x.x][x.y-1].safety = False
    elif x.change == 'up':
        board[x.x][x.y+1].safety = False
    elif x.change == 'right':
        board[x.x+1][x.y].safety = False
    elif x.change == 'leftup':
        board[x.x-1][x.y+1].safety = False
    elif x.change == 'rightdown':
        board[x.x+1][x.y-1].safety = False
    elif x.change == 'leftdown':
        board[x.x-1][x.y-1].safety = False
    elif x.change == 'upright':
        board[x.x+1][x.y+1].safety = False
    return board

#Apply changes of changes found that hopefully will not break constraint
def applyChanges(board, x):
    if x.change == 'left':
        board[x.x-1][x.y].state = 'mined'
    elif x.change == 'down':
        board[x.x][x.y-1].state = 'mined'
    elif x.change == 'up':
        board[x.x][x.y+1].state = 'mined'
    elif x.change == 'right':
        board[x.x+1][x.y].state = 'mined'
    elif x.change == 'leftup':
        board[x.x-1][x.y+1].state = 'mined'
    elif x.change == 'rightdown':
        board[x.x+1][x.y-1].state = 'mined'
    elif x.change == 'leftdown':
        board[x.x-1][x.y-1].state = 'mined'
    elif x.change == 'upright':
        board[x.x+1][x.y+1].state = 'mined'
    return board

#Generates the children of possible positions of where a mine might be based on situation

def generateValidChildren(board,x,y,diff):
    children = Changes(x,y)
    tmp = deepcopy(board)
    if diff == 1:
        validChil = []
        if x != 0:
            tmp[x-1][y].mine = True
            if checkConstraint(tmp) == True and tmp[x-1][y].state == 'uncovered':
                children.change = 'left'
                validChil.append(children)
        tmp = deepcopy(board)
        if y != 0:
            tmp[x][y-1].mine = True
            if checkConstraint(tmp) == True and tmp[x][y-1].state == 'uncovered' :
                children.change = 'down'
                validChil.append(children)
        tmp = deepcopy(board)
        if y < len(tmp)-1:
            tmp[x][y+1].mine = True
            if checkConstraint(tmp) == True and tmp[x][y+1].state == 'uncovered':
                children.change = 'up'
                validChil.append(children)
        tmp = deepcopy(board)
        if x < len(tmp)-1:
            tmp[x+1][y].mine = True
            if checkConstraint(tmp) == True and tmp[x+1][y].state == 'uncovered':
                children.change = 'right'
                validChil.append(children)
        tmp = deepcopy(board)
        if x != 0 and y < len(tmp)-1:
            tmp[x-1][y+1].mine = True
            if checkConstraint(tmp) == True and tmp[x-1][y+1].state == 'uncovered':
                children.change = 'leftup'
                validChil.append(children)
        tmp = deepcopy(board)
        if x < len(board) - 1 and y != 0:
            tmp[x+1][y-1].mine = True
            if checkConstraint(tmp) == True and tmp[x+1][y-1].state == 'uncovered':
                children.change = 'rightdown'
                validChil.append(children)
        tmp = deepcopy(board)
        if x != 0 and y != 0:
            tmp[x-1][y-1].mine = True 
            if checkConstraint(tmp) == True and tmp[x-1][y-1].state == 'uncovered':
                children.change = 'leftdown'
                validChil.append(children)
        tmp = deepcopy(board)
        if x < len(tmp)-1 and y < len(tmp)-1:
            tmp[x+1][y+1].mine = True
            if checkConstraint(tmp) == True and tmp[x+1][y+1].state == 'uncovered':
                children.change = 'upright'
                validChil.append(children)
    else:
        validChil = []
        tmp = deepcopy(board)
        #Generate all Neighbors
        neiboor = []
        if x != 0:
            neiboor.append('left')
        if y != 0:
            neiboor.append('down')
        if y < len(tmp)-1:
            neiboor.append('up')
        if x < len(tmp)-1:
            neiboor.append('right')
        if x != 0 and y < len(tmp)-1:
            neiboor.append('leftup')
        if x < len(board) - 1 and y != 0:
            neiboor.append('rightdown')
        if x != 0 and y != 0:
            neiboor.append('leftdown')
        if x < len(tmp)-1 and y < len(tmp)-1:
            neiboor.append('upright')
        #Generate Permutations of Neighbors
        for perm in combinations(neiboor,diff):
            tmp = deepcopy(board)
            for chan in perm:
                if chan == 'left':
                    if tmp[x-1][y].state == 'uncovered':
                        tmp[x-1][y].mine = True
                elif chan == 'down':
                    if tmp[x][y-1].state == 'uncovered':
                        tmp[x][y-1].mine = True
                elif chan == 'up':
                    if tmp[x][y+1].state == 'uncovered':
                        tmp[x][y+1].mine = True
                elif chan == 'right':
                    if tmp[x+1][y].state == 'uncovered':
                        tmp[x+1][y].mine = True
                elif chan == 'leftup':
                    if tmp[x-1][y+1].state == 'uncovered':
                        tmp[x-1][y+1].mine = True
                elif chan == 'rightdown':
                    if tmp[x+1][y-1].state == 'uncovered':
                        tmp[x+1][y-1].mine = True
                elif chan == 'leftdown':
                    if tmp[x-1][y-1].state == 'uncovered':
                        tmp[x-1][y-1].mine = True
                elif chan == 'upright':
                    if tmp[x+1][y+1].state == 'uncovered':
                        tmp[x+1][y+1].mine = True
            #Add that permutation of changes to moves
            if checkConstraint(tmp) == True:
                for chan in perm:
                    children.change = chan
                    validChil.append(children)
                break
        #for c in range(diff):
    return validChil


#Checks if the current state of the board satisfies constraints
def checkConstraint(board):
    tmpboard = deepcopy(board)
    for i in range(len(tmpboard)):
        for j in range(len(tmpboard[i])):
            checkNeiBoom(tmpboard,i,j)
            checkNeiMine(tmpboard,i,j)
            if tmpboard[i][j].neiMine + tmpboard[i][j].neiBoom > tmpboard[i][j].nei and tmpboard[i][j].state == 'clear':
                return False
    return True

#checks if the game is over in that there are no more uncovered cells
def checkAllClear(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].state == 'uncovered':
                return False
    return True
#Counts the number of mined cells for final score
def countMined(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].state == 'mined':
                count = count + 1
    return count


#Get the Data for graph, x is number of runs
def getData(x):
    sum = 0
    for i in range(x):
        tmp = generateBoard(9,10)
        while checkAllClear(tmp) == False:
            tmp = basicAI(tmp)
        print(countMined(tmp))
        sum = sum + countMined(tmp)
    print(sum)

 #Get the Data for graph for improved agent, x is number of runs
def getDataImp(x):
    sum = 0
    for i in range(x):
        tmp = generateBoard(9,10)
        while checkAllClear(tmp) == False:
            tmp = improvedAI(tmp)
        print(countMined(tmp))
        sum = sum + countMined(tmp)
    print(sum)
   



#getData(50)
getDataImp(50)

