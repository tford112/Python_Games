'''
Othello is a 2-player strategy game revolving around capturing as many pieces as possible
at the conclusion of the game. Each player chooses either black or white as their color.
To capture a piece, black (white) must flip the opponent's rival color piece to turn it White
(Black). To flip a piece, the player must place his piece around the opponent's piece
so it is in the middle of their own pieces. For example, if the board shows "BW" then black
can play a piece next to W so it becomes "BWB" and so the W is flipped to become "BBB".

For more information on game rules, please refer to
'''
import random
import sys
import copy

def board():
    ## board access the row first and then the column
    layout = []
    for row in range(8):
        row = []
        for i in range(8):
            row.append(" .")
        layout.append(row)
    return layout

def printBoard(board):
    col_counter = 1
    for row in board:
        print(col_counter, end = "")
        print(*row)
        col_counter += 1
    bottom_letters = "".join("abcdefgh")
    for letter in bottom_letters:
        print("%3s" % letter, end = "" )

def letters_dict():
    letters = "a b c d e f g h".split()
    lett_dict = {}
    for k,l in enumerate(letters):
        lett_dict[l] = k
    return lett_dict

def translateCoords(coord_list):
    ld = letters_dict()
    for item in coord_list:
        item[1] = ld[item[1]]
    return coord_list

def defaultState(board):
    w1 = [4, "d", "w"]
    b3 = [4, "f", "b"]
    b1 = [4, "e", "b"]
    w2 = [5, "e", "w"]
    b2 = [5, "d", "b"]
    w3 = [4, "h", "w"]
    w4 = [4, "a", "w"]
    b4 = [4, "b", "b"]
    ## vertical testing
    w5 = [3, "d", "w"]
    w6 = [2, "d", "w"]
    b5 = [3, "e", "b"]

    default = [w1, b3, b1, w2, b2, w3, w4, b4, w5, b5, w6]
    clist = translateCoords(default)
    for coord_pos in clist:
        if "w" in coord_pos:
            ## offset by 1 as the column indices are starting from 0 to 7
            ## but the display shows 1-8
            board[coord_pos[0]-1][coord_pos[1]] = " W"
        else:
            board[coord_pos[0]-1][coord_pos[1]] = " B"
    return board

## choosing color to start game
def startColor():
    p1 = input("Pick a color-black or white. Remember, black goes first\n")
    player_start = True
    if p1.lower().startswith("b"):
        print("Okay, player is black.")
        return player_start
    else:
        print("Okay, player is white")
        player_start = False
        return player_start

## CPU generates legal move in game

def cpuMove(board, playerColor):
    ## playercolor is returned from the startColor() function and will determine if CPU is white or not
    ## player is Black so CPU is white
    # if playerColor == True:
        # find out which move to play from list of legal moves
    pass

## function to check all the possible legal moves at each game state for White
def whiteLegal(board):
    ## check horizontal legal moves
    horiz_legal = []
    vert_legal = []
    horiz_blacks = [[board.index(row), k] for row in board for k, x in enumerate(row) if x == " B"]
    rh = copy.deepcopy(horiz_blacks)
    lh = copy.deepcopy(horiz_blacks)
    uh = copy.deepcopy(horiz_blacks)
    bh = copy.deepcopy(horiz_blacks)
    print("\n\n")
    print("Blacks:", horiz_blacks)
    ## HORIZONTAL LEGAL MOVE CHECK
        # left move available as .-W-B on the board
        ## could be .WWWB, .WB
    for pos in lh:
        # print(black_pos, "\n")
        try:
            if board[pos[0]][pos[1] - 1] == " W":
                if pos[1] - 1 == 0:
                    next
                else:
                    pos[1] -= 1
                    while board[pos[0]][pos[1]] == " W":
                        if board[pos[0]][pos[1]-1] == " .":
                            entry = [pos[0],pos[1]-1]
                            if entry not in horiz_legal:
                                horiz_legal.append(entry)
                            ### NEED TO BREAK OUT OF WHILE LOOPS NO MATTER WHAT
                            break
                        if board[pos[0]][pos[1]-1] == " W":
                            pos[1] -= 1
        except IndexError:
            pass
        # right move available as B-W-. on the board
        ## could be BWW., BWWW., BW.
    for pos in rh:
        try:
            if board[pos[0]][pos[1] + 1] == " W":
                if pos[1] + 1 == 7:
                    next
                else:
                    pos[1] += 1
                    while board[pos[0]][pos[1]] == " W":
                        if board[pos[0]][pos[1]+1] == " .":
                            entry = [pos[0],pos[1]+1]
                            if entry not in horiz_legal:
                                horiz_legal.append(entry)
                            break
                        if board[pos[0]][pos[1] + 1] == " W":
                            pos[1] += 1
        except IndexError:
            pass
    print("Horiz_Legal: ", horiz_legal)
    ## VERTICAL LEGAL MOVE CHECK
        ## check if top or bottom move is available
    for pos in uh:
        try:
            ## checking if row above in same col index has white
            ## remember, the indices for the rows are offset by 1 so (3,3) shows up on board
            ## as (4,3)
            if board[pos[0]-1][pos[1]] == " W":
                # print([pos[0],pos[1]])
                if pos[0] - 1 == 0:
                    next
                else:
                    pos[0] -= 1
                    while board[pos[0]][pos[1]] == " W":
                        if board[pos[0]-1][pos[1]] == " .":
                            entry = [pos[0]-1,pos[1]]
                            if entry not in horiz_legal:
                                vert_legal.append(entry)
                            break
                        if board[pos[0]-1][pos[1]] == " W":
                            pos[0] -= 1
        except IndexError:
            pass
    for pos in bh:
        try:
            ## checking if row below in same col index has white
            if board[pos[0]+1][pos[1]] == " W":
                # print([pos[0],pos[1]])
                if pos[0] + 1 == 7:
                    next
                else:
                    pos[0] += 1
                    while board[pos[0]][pos[1]] == " W":
                        if board[pos[0]+1][pos[1]] == " .":
                            entry = [pos[0]+1,pos[1]]
                            if entry not in horiz_legal:
                                vert_legal.append(entry)
                            break
                        if board[pos[0]+1][pos[1]] == " W":
                            pos[0] += 1
        except IndexError:
            pass
    print("Vert_Legal:", vert_legal)

# startColor()
b = board()
printBoard(b)
defaultState(b)
print("\n\n")
printBoard(b)
whiteLegal(b)
