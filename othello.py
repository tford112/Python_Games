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
from time import sleep

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
    b6 = [6, "f", "b"]

    ##side testing
    w11 = [1, "a", "w"]
    w14 = [1, "d", "b"]
    b12 = [1, "b", "b"]
    w41 = [4, "a", "w"]
    b61 = [6, "a", "b"]
    b71 = [7, "a", "b"]

    w62 = [6, "b", "w"]
    b81 = [8, "a", "b"]
    b72 = [7, "b", "b"]
    default = [w1, b3, b1, w2, b2, w3, w4, b4, w5, b5, w6, w7, b6,
                w11, w14, b12, w41, b61, b71, w62, b81, b72]
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
        return player_start, " B"
    else:
        print("Okay, player is white")
        player_start = False
        return player_start, " W"

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
    ld = letters_dict()
    inv_ld = {k:l for l, k in ld.items()} ## reverses letters_dict so {0: "a", 1:"b", 2:"c"...}
    ## convert the legal moves into board interface so the rows need to be offset by 1 and need col letters
    board_legal = []
    for item in legal:
        if item[1] in inv_ld.keys():
            if item[0] >= 0: ##removing option for "CPU moves to '0, b', which is really 8 and makes no sense"
                item = (int(item[0])+1, inv_ld[item[1]]) ## already converts to proper board interface for CPU
                board_legal.append(item)
    return board_legal

## colorPlaying - checking what color I'm looking for legal moves
## findOpposeColor - the opposite of colorPlaying
## positionLegal - vertup, vertdown, horiz_sides, and 4 diagonals
## check row or col position depending on the positionLegal
def findLegal(board, pieces, colorAgainst, row, col):
    positionLegal = copy.deepcopy(pieces)
    legal = []
    for pos in positionLegal:
        ncol = pos[1] + col
        nrow = pos[0] + row
        try:
            # Moved try-except loop outside since this eliminates the need to
            # check bounds
            if not board[nrow][ncol] == colorAgainst:
                # Case when first nrow or ncol is . or colorPlaying
                continue
            else:
                while board[nrow][ncol] == colorAgainst:
                    # Now all we care are if we hit a ., since the while loop
                    # will terminate if a colorPlaying is encountered and
                    # the try-except catches the boundary condition.
                    ncol += col
                    nrow += row
                    if board[nrow][ncol] == ' .':
                        legal.append([nrow, ncol])
                        break
        except IndexError:
            continue
    return legal

## CPU generates move
## playercolor is returned from the startColor() function and will determine if CPU is white or not
def cpuMove(board, color):
    ## if CPU is black
    if color == " B":
        poss_moves = Legal(board, " B", " W")
    else:
        poss_moves = Legal(board, " W", " B")
    ## if there is a possible legal move
    if poss_moves != []:
        cpuMove = random.choice(poss_moves)
        print("CPU moves to {}, {}".format(cpuMove[0], cpuMove[1]))
        # cpuMove = int(cpuMove[0]), cpuMove[1]
        return cpuMove
    else:
        print("No possible move. CPU passes turn.")
        return 0

def playerMove(board, color):
    if color == " B":
        poss_moves = Legal(board, " B", " W")
    else:
        poss_moves = Legal(board, " W", " B")
    if poss_moves != []:
        ld = letters_dict()
        print("Possible", poss_moves)
        # inv_ld = {k:l for l, k in ld.items()}
    ## check if move is within poss_moves
        execute = 0
        while execute != 1:
            play_move = input("Where do you want to place your piece? Enter a row number then a column letter for coordinates.\n")
            play_move = play_move.replace(" ", "")
            board_move = (int(play_move[0]), play_move[1]) ## format as tuple of row num and col letter
            if board_move not in poss_moves:
                print("Sorry, that is not a possible move")
                continue
            else:
                print("You have moved to {}".format(board_move))
                return board_move
                execute += 1
    else:
        print("No moves left. You pass your turn")
        return 0

def flip(board, colorPlaying, colorAgainst, who="player"):
    ld = letters_dict()
    if who == "cpu":
        move = cpuMove(board, colorPlaying) ## tuples can't support item assignment

    else:
        move = playerMove(board, colorPlaying)

    if move != 0:
        # if move[0] == 0
        move = [move[0]-1, ld[move[1]]]
        # print(move)
        board[move[0]][move[1]] = colorPlaying
        all = allOppose(board, colorPlaying, colorAgainst, move)
        ## now turn the colorAgainst into colorPlaying as they are viable to be "flipped"
        for pos in all:
            board[pos[0]][pos[1]] = colorPlaying
    else:
        ## end game if both participants cannot make a move
        if cpuMove(board, colorPlaying) == playerMove(board, colorPlaying): ## both == 0 which is condition of end
            sys.exit()

def allOppose(board, colorPlaying, colorAgainst, piece):
    ## horizontal flipping
    rh = findOppose(board, colorPlaying, colorAgainst, copy.deepcopy(piece), row=0, col=1)
    lh = findOppose(board, colorPlaying, colorAgainst, copy.deepcopy(piece), row=0, col=-1)
    # ## vertical flipping
    bv = findOppose(board, colorPlaying, colorAgainst, copy.deepcopy(piece), row=1, col=0)
    uv = findOppose(board, colorPlaying, colorAgainst, copy.deepcopy(piece), row=-1, col=0)
    # ## diagonal flipping
    se = findOppose(board, colorPlaying, colorAgainst, copy.deepcopy(piece), row=1, col=1)
    ne = findOppose(board, colorPlaying, colorAgainst, copy.deepcopy(piece), row=1, col=-1)
    sw = findOppose(board, colorPlaying, colorAgainst, copy.deepcopy(piece), row=-1, col=1)
    nw = findOppose(board, colorPlaying, colorAgainst, copy.deepcopy(piece), row=-1, col=-1)
    all = rh + lh + bv + uv + se + sw + nw + ne
    return all

## from location of placed piece, flip indices of all the opposing colors in between
def findOppose(board, colorPlaying, colorAgainst, piece, row, col):
    ## find opposing pieces and turn them into colorPlaying
    valid = False
    opp = []
    ## need a copy of the piece for checking whether valid flip can occur otherwise will
    ## only append the last possible element when actually doing the flip past the "if valid" part
    check_piece = copy.deepcopy(piece)
    try:
        if board[check_piece[0]+row][check_piece[1] + col] == colorAgainst:
            if (check_piece[1] + col < 0) or (check_piece[1] + col > 7) or (check_piece[0] + row < 0) or (check_piece[0] + row > 7):
                next
            else:
                check_piece[0], check_piece[1] = check_piece[0]+row, check_piece[1] + col
            ## check if there is colorPlaying surrounding these pieces otherwise would flip everything
            ## directly touching the piece
                while board[check_piece[0]][check_piece[1]] != colorPlaying:
                    ## no surrounding colorPlaying piece
                    ## if black, example would be BWW. but need BWWB
                    if board[check_piece[0]+row][check_piece[1]+col] == " .":
                        break
                    ## reached boundaries of board
                    elif (check_piece[1] + col < 0) or (check_piece[1] + col > 7) or (check_piece[0] + row < 0) or (check_piece[0] + row > 7):
                        break
                    elif board[check_piece[0]+row][check_piece[1]+col] == colorPlaying:
                        valid = True
                        break
                    else: ## reached another colorAgainst
                        check_piece[0], check_piece[1] = check_piece[0]+row, check_piece[1]+col
            # flip
                if valid:
                    piece[0], piece[1] = piece[0] + row, piece[1] +col
                    while board[piece[0]][piece[1]] == colorAgainst:
                        ## there is an issue of directly changing here as the next findOppose() will
                        ## continue where the board is left off which means other pieces will change incorrectly
                            # board[piece[0]][piece[1]] = colorPlaying
                        opp_piece = piece[0],piece[1]
                        opp.append((piece[0], piece[1]))  ## append to list of all opposing pieces
                        if board[piece[0]+row][piece[1] + col] == colorPlaying:
                            break
                        # if board[piece[0]+row][piece[1] + col] == colorAgainst: ## keep progressing through
                        #     piece[0], piece[1] = piece[0]+row, piece[1]+col
                        else:
                            piece[0], piece[1] = piece[0]+row, piece[1]+col

    except IndexError:
        pass
    return opp

## end game function -- check if there are any moves available
def endGame():
    return True

def play():
    # startColor()
    b = board()
    printBoard(b)
    defaultState(b)
    # print("\n\n")
    printBoard(b)
    while True:
        sleep(1)
        flip(b, " B", " W", "cpu")
        printBoard(b)
        flip(b, " W", " B")
        printBoard(b)
    print("End Game")

play()

# b = board()
# printBoard(b)
# defaultState(b)
# printBoard(b)
# Legal(b, " W", " B")
