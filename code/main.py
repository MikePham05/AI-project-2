# evaluation points for 1, 2, 3, 4 in a rows (4 is winning state!)
from random import random

eval_points = [1, 3, 6, 9999]

"""
    This function makes a move at board[i, j] for player k

    Var:
        i, j: values of row and column for the move
        k: 1 for player 1, 2 for player 2

    Return:
        True if the move was successful
        False otherwise
"""


def make_a_move(i, j, k) -> bool:
    global board
    if board[i][j] != 0:
        return False
    board[i][j] = k
    return True


"""
    Check if i, j is in playing board:
    Var:
        i, j,: row and column value of the board
    :return
        True if the box is in the playing board
        False otherwise
"""


def in_board(i, j) -> bool:
    if (i < 0) or (i > 14) or (j < 0) or (j > 14):
        return False
    return True


"""
    Checking terminal condition. The game reaches end condition when a row, column or a diagonal lines of 5 of the
    moves from a same player exists. 
    
    Return: 
        True if The game has ended 
        False otherwise
"""


def terminal_reached() -> bool:
    global board
    valid = True
    for i in range(0, 15):
        for j in range(0, 15):
            if board[i][j] != 0:
                val = board[i][j]
                for k in range(0, 4):
                    for l in range(0, 4):
                        adj_i = i + increments[k][l][0]
                        adj_j = j + increments[k][l][1]
                        if (not in_board(adj_i, adj_j)) or (board[adj_i][adj_j] != val):
                            valid = False
                            continue
                    if not valid:
                        valid = True
                        continue
                    print("player", val, "wins")
                    return True
    return False


"""
    AI player make a move
"""


def ai_move():
    # dummy heuristic for now
    i = int(random() % 15)
    j = int(random() % 15)
    make_a_move(i, j, 2)
    return


# Playing board
board = [[0 for i in range(0, 15)] for j in range(0, 15)]

# increments to check for terminal state
increments = [[[-2, 0], [-1, 0], [1, 0], [2, 0]], [[0, -2], [0, -1], [0, 1], [0, 2]],
              [[-2, -2], [-1, -1], [1, 1], [2, 2]], [[-2, 2], [-1, 1], [1, -1], [2, -2]]]

print(board)

turn = 1
while not terminal_reached():
    if turn == 1:
        i1, j1 = input().split()
        i1 = int(i1)
        j1 = int(j1)
        print(i1, j1)
        make_a_move(i1, j1, 1)
        turn = 2
    else:
        ai_move()
        turn = 1



