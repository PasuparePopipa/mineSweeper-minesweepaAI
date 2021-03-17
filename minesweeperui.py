import pygame, sys
import minesweepai
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (102, 0, 102)
YELLOW = (255,255,0)
CYAN = (0,255,255)
BLUE = (0, 0, 255)

pygame.init()

font = pygame.font.SysFont("Arial",40)
font2 = pygame.font.SysFont("Arial",20)
FPS = 30
fpsClock = pygame.time.Clock()

# This sets the margin between each cell
MARGIN = 5
scale = (720,480)
screen = pygame.display.set_mode(scale,RESIZABLE)
pygame.display.set_caption('MineSweeper!')

#Set dimensions for the board and create board 
dimen = 8
mineNumb = 10
tmpboard = minesweepai.generateBoard(dimen,mineNumb)


def gamestart():
    #Initialize Stuff
    text0 = font.render("MineSweepa",1,RED)
    text1 = font2.render("Single Play",1,BLACK)
    text2 = font2.render("Basic AI",1,BLACK)
    text3 = font2.render("Improved AI",1,BLACK)
    flagMine = 0
    rip = False
    text4 = font2.render("Mines Flagged:" + str(flagMine),1,BLACK)
    win = font.render("You Win!",1,GREEN)
    lose = font.render("You Lose :(",1,(255,0,0))

    #Event Starto
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            #If you want to play without the AI, minesweeper works from clicking!
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                activateCell(tmpboard,dimen,mouse)
                #Run Basic AI
                if 525 <= mouse[0] <= 525+140 and 120 <= mouse[1] <= 120+40:
                    minesweepai.basicAI(tmpboard)
                    flagMine, rip = checkWin(tmpboard,dimen)
                #Run Advanced AI
                if 525 <= mouse[0] <= 525+140 and 170 <= mouse[1] <= 170+40:
                    minesweepai.improvedAI(tmpboard)
                    flagMine, rip = checkWin(tmpboard,dimen)
                    print('clicked')


        text4 = font2.render("Mines Flagged:" + str(flagMine),1,BLACK)

        screen.fill(BLACK)
        #Generate the board on UI based on board generated
        genBoard(tmpboard,dimen)

        #Draw Buttons
        pygame.draw.rect(screen,(170,170,170),[525,70,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,120,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,170,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,220,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,270,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,320,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,370,140,40])
        #Add title
        screen.blit(text0,(495,5))
        #Add label to the buttons
        screen.blit(text1, (530,80))
        screen.blit(text2, (530,130))
        screen.blit(text3, (530,180))

        screen.blit(text4, (530,220))

        #Leaving if for coordinates of possible future buttons
        '''
        #Add text to Buttons
        screen.blit(text1, (530,80))
        screen.blit(text2, (530,130))
        screen.blit(text3, (530,180))
        screen.blit(text4, (530,230))
        screen.blit(text5, (530,280))
        screen.blit(text6, (530,330))
        screen.blit(text35, (530,380))
        '''
        if flagMine == mineNumb:
            screen.blit(win,(500,420))
        if rip == True:
            screen.blit(lose,(500,420))

        #update screen
        pygame.display.update()
        fpsClock.tick(10)

#Activates a cell if user clicks, irrelevant to AI, just an addition
def activateCell(board,x,mouse):
    WIDTH = int((480-(x*MARGIN))/x)
    HEIGHT = int((480-(x*MARGIN))/x)
    for row in range(x):
        for column in range(x):
            board[column][row].cellX = (MARGIN + WIDTH) * column
            board[column][row].cellY = (MARGIN + HEIGHT) * row
            if board[column][row].cellX <= mouse[0]<= board[column][row].cellX + WIDTH and board[column][row].cellY <= mouse[1] <= board[column][row].cellY + HEIGHT:
                board[row][column].state = 'clear'
                print('reached')
    return WIDTH,HEIGHT

#updates winning and losing scenario
def checkWin(board,x):
    counter = 0
    kaboom = False
    for row in range(x):
        for column in range(x):
            if board[column][row].state == 'mined':
                counter = counter + 1
            if board[column][row].state == 'clear' and board[column][row].mine == True:
                kaboom = True


    return counter, kaboom

#Generate the initial maze based on board generated
#Draws everything onto Pygames
def genBoard(board,x):
    WIDTH = int((480-(x*MARGIN))/x)
    HEIGHT = int((480-(x*MARGIN))/x)
    #Get all the assets
    clearCell = pygame.image.load('assets/clear.png').convert_alpha()
    clearCell = pygame.transform.scale(clearCell, (WIDTH, HEIGHT))
    minedCell = pygame.image.load('assets/mined.png').convert_alpha()
    minedCell = pygame.transform.scale(minedCell, (WIDTH, HEIGHT))
    unCovCell = pygame.image.load('assets/uncover.png').convert_alpha()
    unCovCell = pygame.transform.scale(unCovCell, (WIDTH, HEIGHT))
    boom = pygame.image.load('assets/boom.png').convert_alpha()
    boom = pygame.transform.scale(boom, (WIDTH, HEIGHT))
    three = pygame.image.load('assets/3.png').convert_alpha()
    three = pygame.transform.scale(three, (WIDTH, HEIGHT))
    one = pygame.image.load('assets/1.png').convert_alpha()
    one = pygame.transform.scale(one, (WIDTH, HEIGHT))
    two = pygame.image.load('assets/2.png').convert_alpha()
    two = pygame.transform.scale(two, (WIDTH, HEIGHT))
    four = pygame.image.load('assets/4.png').convert_alpha()
    four = pygame.transform.scale(four, (WIDTH, HEIGHT))
    five = pygame.image.load('assets/5.png').convert_alpha()
    five = pygame.transform.scale(five, (WIDTH, HEIGHT))
    six = pygame.image.load('assets/6.png').convert_alpha()
    six = pygame.transform.scale(six, (WIDTH, HEIGHT))
    seven = pygame.image.load('assets/7.png').convert_alpha()
    seven = pygame.transform.scale(seven, (WIDTH, HEIGHT))
    eight = pygame.image.load('assets/8.png').convert_alpha()
    eight = pygame.transform.scale(eight, (WIDTH, HEIGHT))

    #Blitz the assets based on the state of the Cell
    for row in range(x):
        for column in range(x):
            cell = unCovCell
            if board[row][column].state == 'mined':
                cell = minedCell
            if board[row][column].state == 'clear' and board[row][column].mine == False:
                cell = clearCell
            if board[row][column].nei == 1 and board[row][column].state == 'clear':
                cell = one
            if board[row][column].nei == 2 and board[row][column].state == 'clear':
                cell = two
            if board[row][column].nei == 3 and board[row][column].state == 'clear':
                cell = three
            if board[row][column].nei == 4 and board[row][column].state == 'clear':
                cell = four
            if board[row][column].nei == 5 and board[row][column].state == 'clear':
                cell = five
            if board[row][column].nei == 6 and board[row][column].state == 'clear':
                cell = six
            if board[row][column].nei == 7 and board[row][column].state == 'clear':
                cell = seven
            if board[row][column].nei == 8 and board[row][column].state == 'clear':
                cell = eight
            if board[row][column].state == 'clear' and board[row][column].mine == True :
                cell = boom
            screen.blit(cell,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])








#Game Starto
gamestart()
