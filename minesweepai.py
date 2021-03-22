import random
import math
import numpy
from copy import copy, deepcopy
from itertools import combinations

#Cell properties
#state can be covered, mined, or clear
#mine property is whether or not the cell has a mine
#Note, X is vertical, Y is horizontal
#nei represents actual number of Neighbor mines, defaults to 0
#neiSafe, neiHidden, and neiMine are the Knowledge Base conclusions of the agent(number of safe/hidden/mine confirmations) around the specific cell
#cellX, cellY is used for UI purposes
class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.state = 'covered'
        self.mine = False
        self.nei = 0
        #The Following is used as a KB for the agent, the agent only has the information if the cell is not covered
        self.neiSafe = None #Number of safe neighbors
        self.neiHidden = None #Number of Hidden Neighbors
        self.neiMine = None #Number of Neighbors marked as a mine
        self.neiBoom = None #Number of neighbors that went boom, but you're still alive because of keep going rule

        self.cellX= None # UI Purposes
        self.cellY= None # UI Purposes
        self.safety = True #Whether or not Cell we have no info on is safe based on Projected CSP

#Used to project changes based on CSP solution
class Changes:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.change = None #The change, could be up, left, down, leftup, leftdown. rightup etc.


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
    minePlacement = random.sample(range(0,totalCells),n)
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
#s is string of state, covered, cleared, mined
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
        if board[x-1][y].state == 'covered':
            counter = counter + 1
    if y != 0:
        if board[x][y-1].state == 'covered':
            counter = counter + 1
    if y < len(board)-1:
        if board[x][y+1].state == 'covered':
            counter = counter + 1
    if x < len(board)-1:
        if board[x+1][y].state == 'covered':
            counter = counter + 1
    if x != 0 and y < len(board)-1:
        if board[x-1][y+1].state == 'covered':
            counter = counter + 1
    if x < len(board) - 1 and y != 0:
        if board[x+1][y-1].state == 'covered':
            counter = counter + 1
    if x != 0 and y != 0:
        if board[x-1][y-1].state == 'covered':
            counter = counter + 1
    if x < len(board)-1 and y < len(board)-1:
        if board[x+1][y+1].state == 'covered':
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
    if x != 0 and board[x-1][y].state == 'covered':
        board[x-1][y].state = z
    if y != 0 and board[x][y-1].state == 'covered':
        board[x][y-1].state = z
    if y < len(board)-1 and board[x][y+1].state == 'covered':
        board[x][y+1].state = z
    if x < len(board)-1 and board[x+1][y].state == 'covered':
        board[x+1][y].state = z
    if x != 0 and y < len(board)-1 and board[x-1][y+1].state == 'covered':
        board[x-1][y+1].state = z
    if x < len(board) - 1 and y != 0 and board[x+1][y-1].state == 'covered':
        board[x+1][y-1].state = z
    if x != 0 and y != 0 and board[x-1][y-1].state == 'covered':
        board[x-1][y-1].state = z
    if x < len(board)-1 and y < len(board)-1 and board[x+1][y+1].state == 'covered' :
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
            if kb[i][j].state == 'clear' and kb[i][j].mine == False:
                checkNeiMine(kb,i,j)
                checkNeiHidden(kb,i,j)
                checkNeiBoom(kb,i,j)
                if kb[i][j].nei - kb[i][j].neiMine - kb[i][j].neiBoom == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                    confirmation = True
                    #print('p1')
                    board = updateResult(board,i,j,'mined')
    #If 8-Clue minus number of safe neighbors is hidden neighbors, all neighbors are safe
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            if kb[i][j].state == 'clear' and kb[i][j].mine == False:
                checkMine(kb,i,j)
                checkNeiSafe(kb,i,j)
                checkNeiHidden(kb,i,j)
                if 8 - kb[i][j].nei - kb[i][j].neiSafe  == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                    #print('p2')
                    confirmation = True
                    board =  updateResult(board,i,j,'clear')
    #Choose a Cell at random to flip
    if confirmation == False:
        #print('p3')
        counter = 0
        for i in range(len(kb)):
            for j in range(len(kb[i])):
                if kb[i][j].state == 'covered':
                    counter = counter + 1
        rand = random.randint(1,counter)
        counter = 0
        for i in range(len(kb)):
            for j in range(len(kb[i])):
                if kb[i][j].state == 'covered':
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
            if kb[i][j].state == 'clear' and kb[i][j].mine == False: 
                checkNeiMine(kb,i,j)
                checkNeiHidden(kb,i,j)
                checkNeiBoom(kb,i,j)
                if kb[i][j].nei - kb[i][j].neiMine - kb[i][j].neiBoom == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                    confirmation = True
                    board = updateResult(board,i,j,'mined')
    #If 8-Clue minus number of safe neighbors is hidden neighbors, all neighbors are safe
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            if kb[i][j].state == 'clear' and kb[i][j].mine == False:
                checkMine(kb,i,j)
                checkNeiSafe(kb,i,j)
                checkNeiHidden(kb,i,j)
                if 8 - kb[i][j].nei - kb[i][j].neiSafe  == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                    confirmation = True
                    board =  updateResult(board,i,j,'clear')
    #Constraint Satisfaction Cases
    #If there are no guaranteed cases, start algorithm for CSP
    if confirmation == False:
        kb2 = deepcopy(board)
        #Call generate solutions, will return a boolean and the projected board based on CSP
        boole, kb2 = generateSolutions(kb2)
        #If the CSP does not give us any optimal projected solutions, then we will just choose a cell and random
        if boole == False:
            #print('no Opt')
          #Choose Cell at Random
            counter = 0
            for i in range(len(kb)):
                for j in range(len(kb[i])):
                    if kb[i][j].state == 'covered':
                        counter = counter + 1
            rand = random.randint(1,counter)
            counter = 0
            for i in range(len(kb)):
                for j in range(len(kb[i])):
                    if kb[i][j].state == 'covered':
                        counter = counter + 1
                        if counter == rand:
                            board[i][j].state = 'clear'
        #If the CSP gives us an optimal projected solution, we will choose a cell that's safe for sure based on the solution
        elif boole == True:
            # Choose Cell thats safe in CSF solution
            counter = 0
            iList = []
            jList = []
            #Get the i j coordinates of safe cells that are next to an covered or mined cell
            for i in range(len(kb2)):
                for j in range(len(kb2[i])):
                    if kb2[i][j].state == 'covered':
                        checkNeiSafe(kb2,i,j)
                        checkNeiMine(kb2,i,j)
                        if kb2[i][j].neiSafe + kb2[i][j].neiMine >= 1 and kb2[i][j].safety == True:
                            counter = counter + 1
                            iList.append(i)
                            jList.append(j)

            #Choose one of the cells that are safe among them
            rand = random.randint(1,counter)
            counter2 = 0

            for num in range(counter):
                counter2 = counter2 + 1
                if counter2 == rand:
                    board[iList[num]][jList[num]].state = 'clear'

    return board


#An improved agent to play minesweeper but also has global information
def improvedAIGlobal(board,mineCount):
    confirmation = False
    kb = deepcopy(board)
    #Guarantee Cases of Basic Mines
    #If mine neighbors = hidden neighbors, all hidden neighbors are mines
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            if kb[i][j].state == 'clear' and kb[i][j].mine == False: 
                checkNeiMine(kb,i,j)
                checkNeiHidden(kb,i,j)
                checkNeiBoom(kb,i,j)
                if kb[i][j].nei - kb[i][j].neiMine - kb[i][j].neiBoom == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                    confirmation = True
                    board = updateResult(board,i,j,'mined')
    #If 8-Clue minus number of safe neighbors is hidden neighbors, all neighbors are safe
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            if kb[i][j].state == 'clear' and kb[i][j].mine == False:
                checkMine(kb,i,j)
                checkNeiSafe(kb,i,j)
                checkNeiHidden(kb,i,j)
                if 8 - kb[i][j].nei - kb[i][j].neiSafe  == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                    confirmation = True
                    board =  updateResult(board,i,j,'clear')
    #Addition of Global Information Case here
     #If covered cells + mined Cells = Global MineCount, end game, set remaining cells as 'mined'
    mined = 0
    covered = 0
    boom = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].state == 'mined':
                mined = mined+ 1
            if board[i][j].state == 'covered':
                covered = covered + 1
            if board[i][j].state == 'clear' and board[i][j].mine == True:
                boom = boom + 1
    if mineCount == covered + mined + boom:
        #print('Mine' + str(mined))
        #print('Covered' + str(covered))
        #print('Boom' + str(boom))
        confirmation = True
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j].state == 'covered':  
                    board[i][j].state = 'mined'
    #Constraint Satisfaction Cases
    #If there are no guaranteed cases, start algorithm for CSP
    if confirmation == False:
        kb2 = deepcopy(board)
        #Call generate solutions, will return a boolean and the projected board based on CSP
        boole, kb2 = generateSolutions(kb2)
        #If the CSP does not give us any optimal projected solutions, then we will just choose a cell and random
        if boole == False:
          #Choose Cell at Random
            counter = 0
            for i in range(len(kb)):
                for j in range(len(kb[i])):
                    if kb[i][j].state == 'covered':
                        counter = counter + 1
            rand = random.randint(1,counter)
            counter = 0
            for i in range(len(kb)):
                for j in range(len(kb[i])):
                    if kb[i][j].state == 'covered':
                        counter = counter + 1
                        if counter == rand:
                            board[i][j].state = 'clear'
        #If the CSP gives us an optimal projected solution, we will choose a cell that's safe for sure based on the solution
        elif boole == True:
            # Choose Cell thats safe in CSF solution
            counter = 0
            iList = []
            jList = []
            #Get the i j coordinates of safe cells that are next to an covered or mined cell
            for i in range(len(kb2)):
                for j in range(len(kb2[i])):
                    if kb2[i][j].state == 'covered':
                        checkNeiSafe(kb2,i,j)
                        checkNeiMine(kb2,i,j)
                        if kb2[i][j].neiSafe + kb2[i][j].neiMine >= 1 and kb2[i][j].safety == True:
                            counter = counter + 1
                            iList.append(i)
                            jList.append(j)
            #Choose one of the cells that are safe among them
            rand = random.randint(1,counter)
            counter2 = 0
            for num in range(counter):
                counter2 = counter2 + 1
                if counter2 == rand:
                    board[iList[num]][jList[num]].state = 'clear'
    return board


#An improved agent to play minesweeper, but also takes into accoutn risky cells
#Uses Simulated Annealing to maybe get around it
def improvedAIBetter(board):
    confirmation = False
    kb = deepcopy(board)
    #Guarantee Cases of Basic Mines
    #If mine neighbors = hidden neighbors, all hidden neighbors are mines
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            if kb[i][j].state == 'clear' and kb[i][j].mine == False: 
                checkNeiMine(kb,i,j)
                checkNeiHidden(kb,i,j)
                checkNeiBoom(kb,i,j)
                if kb[i][j].nei - kb[i][j].neiMine - kb[i][j].neiBoom == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                    confirmation = True
                    board = updateResult(board,i,j,'mined')
    #If 8-Clue minus number of safe neighbors is hidden neighbors, all neighbors are safe
    for i in range(len(kb)):
        for j in range(len(kb[i])):
            if kb[i][j].state == 'clear' and kb[i][j].mine == False:
                checkMine(kb,i,j)
                checkNeiSafe(kb,i,j)
                checkNeiHidden(kb,i,j)
                if 8 - kb[i][j].nei - kb[i][j].neiSafe  == kb[i][j].neiHidden and kb[i][j].neiHidden != 0:
                    confirmation = True
                    board =  updateResult(board,i,j,'clear')
    #Constraint Satisfaction Cases
    #If there are no guaranteed cases, start algorithm for CSP
    if confirmation == False:
        kb2 = deepcopy(board)
        #Call generate solutions, will return a boolean and the projected board based on CSP
        boole, kb2 = generateSolutions(kb2)
        #If the CSP does not give us any optimal projected solutions, then we will just choose a cell and random
        if boole == False:
            #print('no Opt')
          #Choose Cell at Random
            counter = 0
            for i in range(len(kb)):
                for j in range(len(kb[i])):
                    if kb[i][j].state == 'covered':
                        counter = counter + 1
            rand = random.randint(1,counter)
            counter = 0
            for i in range(len(kb)):
                for j in range(len(kb[i])):
                    if kb[i][j].state == 'covered':
                        counter = counter + 1
                        if counter == rand:
                            board[i][j].state = 'clear'
        #If the CSP gives us an optimal projected solution, we will choose a cell that's safe for sure based on the solution
        elif boole == True:
            # Choose Cell thats safe in CSF solution
            counter = 0
            iList = []
            jList = []
            #Get the i j coordinates of safe cells that are next to an covered or mined cell
            for i in range(len(kb2)):
                for j in range(len(kb2[i])):
                    if kb2[i][j].state == 'covered':
                        checkNeiSafe(kb2,i,j)
                        checkNeiMine(kb2,i,j)
                        if kb2[i][j].neiSafe + kb2[i][j].neiMine >= 1 and kb2[i][j].safety == True:
                            #Filter out for Improved Case
                            #if checkCase(kb2,i,j) == False:
                                counter = counter + 1
                                iList.append(i)
                                jList.append(j)
            #Choose one of the cells that are safe among them
            rand = random.randint(1,counter)
            counter2 = 0
            for num in range(counter):
                counter2 = counter2 + 1
                if counter2 == rand:
                    #Check if this optimal solution safe deemed cell is risky
                    if checkCase(kb2,i,j) == True:
                        #Simulated Annealing Aspect
                        rand2 = random.randint(1,100)
                        if rand2 > 20:
                            board[iList[num]][jList[num]].state = 'clear'
                    else:
                        board[iList[num]][jList[num]].state = 'clear'

    return board

#Filter Mine if choosing it, is risky based on neighboring clues
def checkCase(board,x,y):
    kb = deepcopy(board)
    if x != 0:
        if board[x-1][y].state == 'clear' and board[x-1][y].mine == False and board[x-1][y].nei > 4:
            checkNeiHidden(kb,x-1,y)
            checkNeiBoom(kb,x-1,y)
            checkNeiMine(kb,x-1,y)
            if kb[x-1][y].neiHidden - (kb[x-1][y].nei - (kb[x-1][y].neiBoom + kb[x-1][y].neiMine)) < 2:
                return True
    if y != 0:
        if board[x][y-1].state == 'clear' and board[x][y-1].mine == False and board[x][y-1].nei > 4:
            checkNeiHidden(kb,x,y-1)
            checkNeiBoom(kb,x,y-1)
            checkNeiMine(kb,x,y-1)
            if kb[x][y-1].neiHidden - (kb[x][y-1].nei - (kb[x][y-1].neiBoom + kb[x][y-1].neiMine)) < 2:
                return True
    if y < len(board)-1:
        if board[x][y+1].state == 'clear' and board[x][y+1].mine == False and board[x][y+1].nei > 4:
            checkNeiHidden(kb,x,y+1)
            checkNeiBoom(kb,x,y+1)
            checkNeiMine(kb,x,y+1)
            if kb[x][y+1].neiHidden - (kb[x][y+1].nei - (kb[x][y+1].neiBoom + kb[x][y+1].neiMine)) < 2:
                return True
    if x < len(board)-1:
        if board[x+1][y].state == 'clear' and board[x+1][y].mine == False and board[x+1][y].nei > 4:
            checkNeiHidden(kb,x+1,y)
            checkNeiBoom(kb,x+1,y)
            checkNeiMine(kb,x+1,y)
            if kb[x+1][y].neiHidden - (kb[x+1][y].nei - (kb[x+1][y].neiBoom + kb[x+1][y].neiMine)) < 2:
                return True
    if x != 0 and y < len(board)-1:
        if board[x-1][y+1].state == 'clear' and board[x-1][y+1].mine == False and board[x-1][y+1].nei > 4:
            checkNeiHidden(kb,x-1,y+1)
            checkNeiBoom(kb,x-1,y+1)
            checkNeiMine(kb,x-1,y+1)
            if kb[x-1][y+1].neiHidden - (kb[x-1][y+1].nei - (kb[x-1][y+1].neiBoom + kb[x-1][y+1].neiMine)) < 2:
                return True
    if x < len(board) - 1 and y != 0:
        if board[x+1][y-1].state == 'clear' and board[x+1][y-1].mine == False and board[x+1][y-1].nei > 4:
            checkNeiHidden(kb,x+1,y-1)
            checkNeiBoom(kb,x+1,y-1)
            checkNeiMine(kb,x+1,y-1)
            if kb[x+1][y-1].neiHidden - (kb[x+1][y-1].nei - (kb[x+1][y-1].neiBoom + kb[x+1][y-1].neiMine)) < 2:
                return True
    if x != 0 and y != 0:
        if board[x-1][y-1].state == 'clear' and board[x-1][y-1].mine == False and board[x-1][y-1].nei > 4:
            checkNeiHidden(kb,x-1,y-1)
            checkNeiBoom(kb,x-1,y-1)
            checkNeiMine(kb,x-1,y-1)
            if kb[x-1][y-1].neiHidden - (kb[x-1][y-1].nei - (kb[x-1][y-1].neiBoom + kb[x-1][y-1].neiMine)) < 2:
                return True
    if x < len(board)-1 and y < len(board)-1:
        if board[x+1][y+1].state == 'clear' and board[x+1][y+1].mine == False and board[x+1][y+1].nei > 4:
            checkNeiHidden(kb,x+1,y+1)
            checkNeiBoom(kb,x+1,y+1)
            checkNeiMine(kb,x+1,y+1)
            if kb[x+1][y+1].neiHidden - (kb[x+1][y+1].nei - (kb[x+1][y+1].neiBoom + kb[x+1][y+1].neiMine)) < 2:
                return True
    return False


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
    #For the list of valid options in our optimal solution we will check and run them all and see if they break constraints
    #If we find one that does not break constraints, we will return the board with the safety of the projected mines marked as false
    #If we cannot find any, we return false and the board
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

#Apply change the safety property of the cell of projected mines to prepare to return in the case that it does not break constraint
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

#Apply changes of to board of projected miens, hopefully will not break constraint
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
    #If the difference of the mine clue and actual revealed mines/boom is one, follow. walks through the possible projected spaces of the mine placement
    if diff == 1:
        validChil = []
        if x != 0:
            tmp[x-1][y].mine = True
            if checkConstraint(tmp) == True and tmp[x-1][y].state == 'covered':
                children.change = 'left'
                validChil.append(children)
        tmp = deepcopy(board)
        if y != 0:
            tmp[x][y-1].mine = True
            if checkConstraint(tmp) == True and tmp[x][y-1].state == 'covered' :
                children.change = 'down'
                validChil.append(children)
        tmp = deepcopy(board)
        if y < len(tmp)-1:
            tmp[x][y+1].mine = True
            if checkConstraint(tmp) == True and tmp[x][y+1].state == 'covered':
                children.change = 'up'
                validChil.append(children)
        tmp = deepcopy(board)
        if x < len(tmp)-1:
            tmp[x+1][y].mine = True
            if checkConstraint(tmp) == True and tmp[x+1][y].state == 'covered':
                children.change = 'right'
                validChil.append(children)
        tmp = deepcopy(board)
        if x != 0 and y < len(tmp)-1:
            tmp[x-1][y+1].mine = True
            if checkConstraint(tmp) == True and tmp[x-1][y+1].state == 'covered':
                children.change = 'leftup'
                validChil.append(children)
        tmp = deepcopy(board)
        if x < len(board) - 1 and y != 0:
            tmp[x+1][y-1].mine = True
            if checkConstraint(tmp) == True and tmp[x+1][y-1].state == 'covered':
                children.change = 'rightdown'
                validChil.append(children)
        tmp = deepcopy(board)
        if x != 0 and y != 0:
            tmp[x-1][y-1].mine = True 
            if checkConstraint(tmp) == True and tmp[x-1][y-1].state == 'covered':
                children.change = 'leftdown'
                validChil.append(children)
        tmp = deepcopy(board)
        if x < len(tmp)-1 and y < len(tmp)-1:
            tmp[x+1][y+1].mine = True
            if checkConstraint(tmp) == True and tmp[x+1][y+1].state == 'covered':
                children.change = 'upright'
                validChil.append(children)
    #If it's greater than 1, then we will generate permulations of the possible projected mine placements
    #before adding them to the list of valid children
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
                    if tmp[x-1][y].state == 'covered':
                        tmp[x-1][y].mine = True
                elif chan == 'down':
                    if tmp[x][y-1].state == 'covered':
                        tmp[x][y-1].mine = True
                elif chan == 'up':
                    if tmp[x][y+1].state == 'covered':
                        tmp[x][y+1].mine = True
                elif chan == 'right':
                    if tmp[x+1][y].state == 'covered':
                        tmp[x+1][y].mine = True
                elif chan == 'leftup':
                    if tmp[x-1][y+1].state == 'covered':
                        tmp[x-1][y+1].mine = True
                elif chan == 'rightdown':
                    if tmp[x+1][y-1].state == 'covered':
                        tmp[x+1][y-1].mine = True
                elif chan == 'leftdown':
                    if tmp[x-1][y-1].state == 'covered':
                        tmp[x-1][y-1].mine = True
                elif chan == 'upright':
                    if tmp[x+1][y+1].state == 'covered':
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

#checks if the game is over in that there are no more covered cells
def checkAllClear(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].state == 'covered':
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
        tmp = generateBoard(10,10)
        while checkAllClear(tmp) == False:
            tmp = basicAI(tmp)
        print(countMined(tmp))
        sum = sum + countMined(tmp)
    print(sum)

 #Get the Data for graph for improved agent, x is number of runs
def getDataImp(x):
    sum = 0
    for i in range(x):
        tmp = generateBoard(10,10)
        while checkAllClear(tmp) == False:
            tmp = improvedAIBetter(tmp)
        print(countMined(tmp))
        sum = sum + countMined(tmp)
    print(sum)
   



#getData(150)
#getDataImp(100)

