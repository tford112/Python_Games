import sys
import random
import numpy as np

def generateBoard():
    layout = []
    for row in range(9):
        row = []
        layout.append(row)
        for row_val in range(15):
            ocean_mark = random.randint(0,1)
            if ocean_mark == 0:
                row.append('%3s' % "~") ## necessary to align the ocean marks
            if ocean_mark == 1:
                row.append('%3s' % "`")
    # for row in layout:
    #     print(*row)
    return layout

def printBoard(board, chest_coord1=None, chest_coord2=None, show= False):
    col_counter = 0
    ## unpacking each list (row) in the 'list of lists'
    if show == False:
        for row in board:
            print(col_counter, end = "")
            if "  X" in row:
                chest_index = row.index("  X")
                row[chest_index] = "~"
                print(*row)
            else:
                print(*row)
            col_counter +=1
    else:
        board[chest_coord1][chest_coord2] = "  X"
        for row in board:
            print(col_counter, end = "")
            print(*row)  # unpacking the values from each row of ocean cleanly
            col_counter +=1
    top_letters = "".join("abcdefghijklmno")
    for letter in top_letters:
        print('%4s' % letter, end = "") ## aligning the nums

def letters_dict():
    letters = "a b c d e f g h i j k l m n o".split()
    letters_dict = {}
    for key, val in enumerate(letters):
        letters_dict[val] = key
    return letters_dict

def generate_chest(board):
    # each col is range(15) and each row_val is range(9)
    letters = letters_dict()
    letter = random.choice(list(letters.keys()))
    first_coord = random.randint(0,8)
    second_coord = letters[letter]
    chest = "  X"
    # print(type(x_coord), x_coord, y_coord)
    board[first_coord][second_coord] = chest
    return board, first_coord, second_coord

def choose_sonar():
    print("Where do you want to drop your sonar?")
    #checking whether inputs are appropriate
    try:
        coords = []
        while True:
            p1 = input("Choose a letter\n")
            if p1.isdigit() == False:
                ## in case user accidentally adds a space after letter
                p1 = p1.strip()
                coords.append(p1)
                break
            else:
                print("Sorry! That's not a valid option!")
                continue
        while True:
            p2 = input("Choose a number\n")
            if p2.isdigit():
                coords.append(p2)
                break
            else:
                print("Sorry! That's not a valid option!")
                continue
        return coords
    except ValueError as e:
        print(e)

def drop_sonar(coord_list, board):
    # the board col number is the second element from choose_sonar()
    letters = letters_dict()
    access_board_second = int(letters[coord_list[0]])
    access_board_first = int(coord_list[1])
    # print(access_board_first, access_board_second)
    sonar = "  O"
    board[access_board_first][access_board_second] = sonar
    return board, access_board_first, access_board_second

def calculate_dist(pc1, pc2, chest_coord_1, chest_coord_2):
    # print("\nplayer coords:", pc1, pc2)
    # print("\nchest_coords:", chest_coord_1, chest_coord_2)
    row_num_diff = abs(pc1 - chest_coord_1)
    letter_col_diff = abs(pc2 - chest_coord_2)
    if row_num_diff != 0 and letter_col_diff != 0:
        ## use pythagorean theorem to find distance of third side
        dist = np.sqrt((row_num_diff**2) + (letter_col_diff**2))
        print("\nThe distance between the sonar and chest is", dist)
    elif row_num_diff == 0:
        dist = letter_col_diff
        print("\nThe distance between the sonar and chest is", dist)
    else:
        dist = row_num_diff
        print("\nThe distance between the sonar and chest is", dist)



board = generateBoard()
board, chest_coord_1, chest_coord_2 = generate_chest(board)
printBoard(board)
print("\n")
p_chosen = choose_sonar()
board, pc1, pc2 = drop_sonar(p_chosen, board)
# printBoard(board, chest_coord_1, chest_coord_2, True)
calculate_dist(pc1, pc2,chest_coord_1, chest_coord_2)
# print((board[0][0:3]))

# print("\n",layout[0])
