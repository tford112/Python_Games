#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:12:06 2019

@author: tomtom
"""

import random, sys, os, pygame
from pygame.locals import *

os.chdir('/Users/tomtom/Documents/Python_Games')

fps = 30 ## frames per second 
ww = 640 ## windowidth in pixels
wh = 480 ## size of window height 
reveal_speed = 8 ## speed boxes' sliding reveals and covers 
box_size = 40 # size of box height and width 
gap_size = 10 # size of gap between boxes in pixels 

board_w = 2 ## number of columns of icons 
board_h = 2 ## number of rows 

## write assert statements early so crash earlier and can be easier detecting bugs 
assert (board_w * board_h) % 2 == 0, 'Board needs to have an even number of boxes for pairs'

## margins 
xmarg = int((ww - (board_w  * (box_size + gap_size)))/2)
ymarg = int((wh - (board_h * (box_size + gap_size)))/2)

## colors 
gray = (100, 100, 100)
magenta = (60, 1, 100)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 00, 255)
yellow = (255, 255, 0)
orange = (255, 128, 0)
purple = (255, 0, 255)
cyan = (0, 255, 255)

bg_color = magenta 
light_bg_color = gray 
box_color = white 
highlight_color = blue 

## using constant variables instead of strings allows for bugs to be detected faster 
donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

all_colors = (red, green, blue, yellow, orange, purple, cyan)
all_shapes = (donut, square, diamond, lines, oval)
assert len(all_colors) * len(all_shapes) * 2 >= board_w * board_h, "Board is too big for number of shapes/colors defined"

pygame.init()
display = pygame.display.set_mode((ww, wh))
pygame.display.set_caption("Memory Game")

def main():
    
    ## mouse_state
    mousex = 0 ## used to store x coord of mouse event
    mousey = 0 ## used to store y coord of mouse event
    
    ## board_state 
    main_board = getRandomizedBoard() ## returns a data struct representing board state 
    revealed_boxes = generateRevealedBoxesData(False) ## returns data struct representing which boxes are covered
    
    first_select = None 
    display.fill(bg_color)
    startGameAnimation(main_board)
    
    ## Game Loop 
    while True:
        mouse_clicked = False 
        display.fill(bg_color) # draw window 
        drawBoard(main_board, revealed_boxes)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos 
            elif event.type == MOUSEBUTTONUP: ## mouse button clicked and let go which is registered as an event
                mousex, mousey = event.pos
                mouse_clicked = True 
                
        box_x, box_y = getBoxAtPixel(mousex, mousey)
        if box_x != None and box_y != None:
            # the mouse is currently over a box-- hovering  
            if not revealed_boxes[box_x][box_y]:
                drawHighlightBox(box_x, box_y)
            if not revealed_boxes[box_x][box_y] and mouse_clicked: ## actual click 
                revealBoxesAnimation(main_board, [(box_x, box_y)])
                revealed_boxes[box_x][box_y] = True ## set the box as 'revealed' 
                if first_select == None: ## the current box was the first box clicked
                    first_select = (box_x, box_y)
                else: ## current box is not the first box selected 
                    # check if there is a match between the two icons 
                    icon1_shape, icon1_color = getShapeAndColor(main_board, first_select[0], first_select[1])
                    icon2_shape, icon2_color = getShapeAndColor(main_board, box_x, box_y)
                    
                    if icon1_shape != icon2_shape or icon1_color != icon2_color:
                        # icons don't match so re-cover both selections 
                        pygame.time.wait(500) ## 1000 milliseconds = 1 sec 
                        ## cover the two selected boxes (first_select, and second box)
                        coverBoxesAnimation(main_board, [(first_select[0], first_select[1]), (box_x, box_y)])
                        revealed_boxes[first_select[0]][first_select[1]] = False
                        revealed_boxes[box_x][box_y] = False 
                    elif hasWon(revealed_boxes): ## check if all pairs found 
                        revealBoxesAnimation(main_board, revealed_boxes)
                        gameWon(main_board)
                        gameWonAnimation(main_board)
                        pygame.time.wait(3000)
                        
                        # reset the board 
                        main_board = getRandomizedBoard()
                        revealed_boxes = generateRevealedBoxesData(False)
                        
                        # show the fully unrevealed board for a second 
                        drawBoard(main_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        
                        # replay the start game animation 
                        startGameAnimation(main_board)
                    first_select = None # reset first_select variable 
                    
        pygame.display.update()
        pygame.time.Clock().tick(fps)
        
# populates board size with list of lists of boolean values to reveal or not
def generateRevealedBoxesData(val):
    revealed_boxes = []
    for i in range(board_w):
        revealed_boxes.append([val] * board_h)
    return revealed_boxes 

# randomly assign board with all possible icons
def getRandomizedBoard():
    # get a list of every possible shape in every possible color 
    icons = []
    for color in all_colors:
        for shape in all_shapes:
            icons.append((shape, color))
    random.shuffle(icons)
    num_icons_used = int(board_w * board_h/ 2) ## calculate how many icons needed 
    icons = icons[:num_icons_used] * 2 ## make two of each 
    assert len(icons) == board_w * board_h, "Number of icons does not equal number of board spaces" 
    random.shuffle(icons)  
    ## place icons on board 
    board = []
    for x in range(board_w):
        col = []
        for y in range(board_h):
            col.append(icons[0]) ## extract first (shape, color) tuple from list of tuples 
            del icons[0] ## delete the icon from randomly shuffled list 
        board.append(col)
    assert len(icons) == 0, "Icons remaining to be used on board"
    return board 

# shape value for x, y spot is stored in board[x][y][0]
# color value for x, y spot is stored in board[x][y][1]    
def getShapeAndColor(board, box_x, box_y):
    return board[box_x][box_y][0], board[box_x][box_y][1]

# splits a list into a list of lists where the inner lists have at 
# most groupSize number of items 
def splitIntoGroups(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize): ## note that even if list slicing 'exceeds' the last value of list, 
        result.append(theList[i:i+groupSize])   ## it'll fill up with the remaining items and slicing isn't destroying so this won't raise an Out-of-bounds index error
    return result 

## The next two functions relate to how we translate the randomized board to the actual pygame display 
## by translating each box into a pixelated box equally spaced out from each other 
def leftTopCoordsOfBox(board_box_x, board_box_y):
    # convert board coords of list of lists to pixel coordinates for display boar
    left = board_box_x * (box_size + gap_size) + xmarg
    top = board_box_y * (box_size + gap_size) + ymarg
    return (left, top)

def getBoxAtPixel(mousex,mousey):
    for x in range(board_w):
        for y in range(board_h):
            left, top = leftTopCoordsOfBox(x, y)
            boxRect = pygame.Rect(left, top, box_size, box_size)
            if boxRect.collidepoint(mousex, mousey): ## if mouse button clicks on this box then will reveal
                return (x, y)
    return (None, None)
                    
def drawIcon(shape, color, box_x, box_y):
    quarter = int(box_size * 0.25) # syntactic sugar
    half = int(box_size * 0.5) # syntactic sugar 
    
    left, top = leftTopCoordsOfBox(box_x, box_y) ## get pixel coords from board coords 
    # draw the shapes 
    if shape == donut:
        pygame.draw.circle(display, color, (left + half, top+half), half-5) 
        pygame.draw.circle(display, bg_color, (left + half, top+half), quarter-5)
    elif shape == square:
        pygame.draw.rect(display, color, (left + quarter, top+quarter, box_size - half, box_size - half))
    elif shape == diamond:
        pygame.draw.polygon(display, color, ((left+half, top), (left + box_size -1, top+half), \
                                             (left + half, top+ box_size -1), (left, top+half)))
    elif shape == lines: 
        for i in range(0, box_size, 4):
            pygame.draw.line(display, color, (left, top + i), (left +i, top))
            pygame.draw.line(display, color, (left + i, top + box_size - 1), (left + box_size -1, top +i))
    elif shape == oval:
        pygame.draw.ellipse(display, color, (left, top + quarter, box_size, half))
        
## draws boxes being covered/revealed. 'boxes' is a list of two-item lists which have x,y coords of box
def drawBoxCovers(board, boxes, coverage):
    for box in boxes: 
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(display, bg_color, (left, top, box_size, box_size))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only the draw the cover if there is a coverage 
            pygame.draw.rect(display, box_color, (left, top, coverage, box_size))
    pygame.display.update()
    pygame.time.Clock().tick(fps)

# do 'box reveal' animation
def revealBoxesAnimation(board, boxes_to_reveal):
    for coverage in range(box_size, (-reveal_speed)-1, -reveal_speed):
        drawBoxCovers(board, boxes_to_reveal, coverage)

# do 'box cover' animation   
def coverBoxesAnimation(board, boxes_to_cover):
    for coverage in range(0, box_size + reveal_speed, reveal_speed):
        drawBoxCovers(board, boxes_to_cover, coverage)

# draws all the boxes in their covered or revealed state    
def drawBoard(board, revealed):
    for x in range(board_w):
        for y in range(board_h):
            left, top = leftTopCoordsOfBox(x, y)
            if not revealed[x][y]: ## remember this is a list of lists of booleans
                # draw covered box 
                pygame.draw.rect(display, box_color, (left, top, box_size, box_size))
            else:
                # draw revealed icon 
                shape, color = getShapeAndColor(board, x, y)
                drawIcon(shape, color, x, y)
                
def drawHighlightBox(x, y):
    left, top = leftTopCoordsOfBox(x, y)
    pygame.draw.rect(display, highlight_color, (left-5, top-5, box_size + 10, box_size +10), 4)
    
## randomly reveal the boxes 8 at a time
def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(board_w):
        for y in range(board_h):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroups(8, boxes)
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups: 
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)
        
def hasWon(revealedBoxes):
    # returns True if all the boxes have been revealed otherwise False
    for i in revealedBoxes:
        if False in i:
            return False ## return False if any boxes are covered 
    return True 

## my own created helper function 
## display sign that user has won with text and victory music playing 

def gameWon(board):
    font = pygame.font.SysFont('Comic Sans MS', 15)
    text_surf = font.render('Congrats you won!', False, white)
    text_surf_rect = text_surf.get_rect()
    text_surf_rect.center = (240, 570)
    display.blit(text_surf, text_surf_rect)
    pygame.display.update()
    ## load victory music
    pygame.mixer.music.load('beethoven_symph6_pastoral.mp3')
    pygame.mixer.music.play(-1, 0.0)
    pygame.time.wait(10000)
    pygame.mixer.music.stop()
    
def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1= light_bg_color
    color2 = bg_color 
    
    for i in range(5):
        color1, color2 = color2, color1 # swap colors 
        display.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)   
    


if __name__ == '__main__':
    main()