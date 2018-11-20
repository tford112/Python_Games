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

def translate_coords(coord_list):
    ld = letters_dict()
    for item in coord_list:
        item[1] = ld[item[1]]
    return coord_list

def default_state(board):
    w1 = [4, "d", "w"]
    b1 = [4, "e", "b"]
    w2 = [5, "e", "w"]
    b2 = [5, "d", "b"]
    default = [w1, b1, w2, b2]
    clist = translate_coords(default)
    for coord_pos in clist:
        if "w" in coord_pos:
            ## offset by 1 as the column indices are starting from 0 to 7
            ## but the display shows 1-8
            board[coord_pos[0]-1][coord_pos[1]] = " W"
        else:
            board[coord_pos[0]-1][coord_pos[1]] = " B"
    return board


b = board()
printBoard(b)
default_state(b)
print("\n\n")
printBoard(b)
