'''
Othello is a 2-player strategy game revolving around capturing as many pieces as possible
at the conclusion of the game. Each player chooses either black or white as their color.
To capture a piece, black (white) must flip the opponent's rival color piece to turn it White
(Black). To flip a piece, the player must place his piece around the opponent's piece
so it is in the middle of their own pieces. For example, if the board shows "BW" then black
can play a piece next to W so it becomes "BWB" and so the W is flipped to become "BBB".

For more information on game rules, please refer to http://www.ultraboardgames.com/othello/game-rules.php
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
    print("\n\n")

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
    w7 = [5, "c", "w"]
    default = [w1, b3, b1, w2, b2, w3, w4, b4, w5, b5, w6, w7]
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

## function to check all the possible legal moves at each game state for White
def Legal(board, colorPlaying, colorAgainst):
    ## check where pieces are on board
    pieces = [[board.index(row), k] for row in board for k, x in enumerate(row) if x == colorPlaying]
    # print(colorPlaying, pieces)
    ## HORIZONTAL LEGAL MOVE CHECK
        # left move available as .-W-B on the board could be .WWWB, .WB
        # right move would be BWW or BW
    rh_legal = findLegal(board, pieces, colorAgainst, row=0, col= 1)
    lh_legal = findLegal(board, pieces, colorAgainst, row=0, col= -1)
    horiz_legal = rh_legal + lh_legal
    ## removing duplicates can only work with set if the elements within the list aren't a list themselves
    ## list turns from dict to list
    horiz_legal = list(set(tuple(l) for l in horiz_legal))
    ## VERTICAL LEGAL MOVE CHECK
        ## check if top or bottom move is available
    uh_legal = findLegal(board, pieces, colorAgainst, row = -1, col = 0)
    bh_legal = findLegal(board, pieces, colorAgainst, row = 1, col = 0)
    vert_legal = uh_legal + bh_legal
    vert_legal = list(set(tuple(l) for l in vert_legal))
    ## DIAGONAL LEGAL MOVE CHECK
        ## check if NW, NE, SE, SW diagonal moves can be made
    se_legal = findLegal(board, pieces, colorAgainst, row = 1, col = 1)
    ne_legal = findLegal(board, pieces, colorAgainst, row = -1, col = 1)
    nw_legal = findLegal(board, pieces, colorAgainst, row = -1, col = -1)
    sw_legal = findLegal(board, pieces, colorAgainst, row = 1, col = -1)
    d_legal = se_legal + ne_legal + nw_legal + sw_legal
    d_legal = list(set(tuple(l) for l in d_legal))
    legal = horiz_legal + vert_legal + d_legal
    return legal

## colorPlaying - checking what color I'm looking for legal moves
## findOpposeColor - the opposite of colorPlaying
## positionLegal - vertup, vertdown, horiz_sides, and 4 diagonals
## check row or col position depending on the positionLegal
def findLegal(board, pieces, colorAgainst, row, col):
    positionLegal = copy.deepcopy(pieces)
    legal = []
    ## Horiz Legals
    try:
        for pos in positionLegal:
            if board[pos[0]+row][pos[1] + col] == colorAgainst:
                if (pos[1] + col == 0) or (pos[1] + col == 7) or (pos[0] + row == 0) or (pos[0] + row == 7):
                    next
                else:
                    pos[0], pos[1] = pos[0]+row, pos[1] + col
                    while board[pos[0]][pos[1]] == colorAgainst:
                        if board[pos[0]+row][pos[1] +col] == " .":
                            entry = [pos[0] + row, pos[1]+col]
                            legal.append(entry)
                            break
                        elif board[pos[0] +row][pos[1] + col] == colorAgainst:
                            pos[0], pos[1] = pos[0] +row, pos[1] +col
                    ## need to add the below conditional in case next avail space is not playable
                    # because already occupied by colorPlaying otherwise while loop will not break
                        else:
                            break
    except IndexError:
        pass
    return legal

## CPU generates move
## playercolor is returned from the startColor() function and will determine if CPU is white or not
def cpuMove(board, color):
    ## if CPU is black
    if color == " B":
        poss_moves = Legal(b, " B", " W")
    else:
        poss_moves = Legal(b, " W", " B")
    ## if there is a possible legal move
    if poss_moves != []:
        cpuMove = random.choice(poss_moves)
        # print("CPU moves to {}{}", cpuMove[0], clist[1])
        board[cpuMove[0]][cpuMove[1]] = color
        return cpuMove
    else:
        print("No possible move. CPU passes turn.")

def flip(board, colorPlaying, colorAgainst, who):
    if who == "cpu":
        # move = list(cpuMove(board, colorPlaying)) ## tuples can't support item assignment
        # print(move)
        move = [2,2]
        ## horizontal flipping
        findOppose(board, colorPlaying, colorAgainst, move, row=0, col=1)
        findOppose(board, colorPlaying, colorAgainst, move, row=0, col=-1)
        ## vertical flipping
        findOppose(board, colorPlaying, colorAgainst, move, row=1, col=0)
        findOppose(board, colorPlaying, colorAgainst, move, row=-1, col=0)
        ## diagonal flipping
        findOppose(board, colorPlaying, colorAgainst, move, row=1, col=1)
        findOppose(board, colorPlaying, colorAgainst, move, row=1, col=-1)
        findOppose(board, colorPlaying, colorAgainst, move, row=-1, col=1)
        findOppose(board, colorPlaying, colorAgainst, move, row=-1, col=-1)

## from location of placed piece, flip indices of all the opposing colors in between
def findOppose(board, colorPlaying, colorAgainst, piece, row, col):
    ## find opposing pieces and turn them into colorPlaying
    valid = False
    try:
        if board[piece[0]+row][piece[1] + col] == colorAgainst:
            if (piece[1] + col == 0) or (piece[1] + col == 7) or (piece[0] + row == 0) or (piece[0] + row == 7):
                next
            else:
                piece[0], piece[1] = piece[0]+row, piece[1] + col
                ## check if there is colorPlaying surrounding these pieces otherwise would flip everything
                while board[piece[0]][piece[1]] != colorPlaying:
                    ## no surrounding colorPlaying piece
                    ## if black, example would be BWW. but need BWWB
                    if board[piece[0]+row][piece[1]+col] == " .":
                        break
                    ## reached boundaries of board
                    elif (piece[1] + col < 0) or (piece[1] + col > 7) or (piece[0] + row < 0) or (piece[0] + row > 7):
                        break
                    elif board[piece[0]][piece[1]] == colorPlaying:
                        valid = True
                        break
                    else:
                        board[piece[0]][piece[1]] = board[piece[0]+row][piece[1]+col]
                ## need to reset position otherwise
                ## flip
                if valid:
                    # print("The row, col:")
                    while board[piece[0]][piece[1]] == colorAgainst:
                        board[piece[0]][piece[1]] = colorPlaying
                        if board[piece[0]+row][piece[1] + col] == colorAgainst:
                            board[piece[0]][piece[1]] = board[piece[0]+row][piece[1]+col]
                        else:
                            break
    except IndexError:
        pass


# startColor()
b = board()
printBoard(b)
defaultState(b)
# print("\n\n")
printBoard(b)
# Legal(b, " B", " W")
# Legal(b, " W", " B")
# move = cpuMove(b, " B")
flip(b, " B", " W", "cpu")
printBoard(b)
