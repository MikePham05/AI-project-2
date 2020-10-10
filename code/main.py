import random

"""
    This function makes a move at board[i, j] for player k

    Var:
        i, j: values of row and column for the move
        k: 1 for player 1, 2 for player 2
        board: current state of the board

    Return:
        True if the move was successful
        False otherwise
"""


def make_a_move(board, i, j, k) -> bool:
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
    Generating children of a node in the search tree. Children created are created according to
    the algorithm implemented in this function. 
    The algorithm is: #TODO
    NOTE: THIS FUNCTION HIGHLY DETERMINES EFFECTIVENESS OF AI'S MOVE. REQUIRES GREAT ATTENTION
    
    :var
        state: current state of the node
        
    :return
        moves: a list of possible move from the current state of the board
"""


def generating_moves(state) -> [[int]]:
    # TODO
    # dummy generating for testing now
    pi = random.randint(0, 13)  # pivot i
    pj = random.randint(0, 13)  # pivot j
    print(pi, pj)
    moves = [[pi, pj]]
    return moves


""""
    Return a heuristic value that evaluate how beneficial a current state of the board to each player.
    Value higher than 0 indicates a state that is more beneficial to player 2, the AI, while value lower 
    than 0 indicates a state more beneficial to player 1, the player. The bigger the absolute value of the 
    heuristic is, the better the state to that player
    
    NOTE: 
        THIS FUNCTION HIGHLY DETERMINES EFFECTIVENESS OF AI'S MOVE. REQUIRES GREAT ATTENTION
        HEURISTIC VALUE IS GREATLY AFFECTED BY EVAL_POINTS AS THE ARRAY SOLELY DETERMINES HOW
        HEURISTIC IS CALCULATED
        
    :var
        state: current state of the node
    
    :return
        h: heuristic value of the node
"""


def heuristic(state) -> int:
    # TODO
    return 0


"""
    Returns a "future" board after player k has made move at state[i][j]. Function is used in
    generating search tree only
    
    :var
        i, j: tile position of the move
        k: player who made the move (1 for opposing player, 2 for the AI)
        
    :return
        state: state of the board after the move
"""


def make_future_move(state, i, j, k) -> [[int]]:
    state[i][j] = k
    return state


"""
    Undo a move. This function is intended for generating states in a search tree only
    :return 
        True if move undo successful
        False otherwise (tile already empty)
"""


def undo_future_move(state, i, j) -> bool:
    if state[i][j] == 0:
        return False
    state[i][j] = 0
    return True


"""
    Min-value player (opposing player)
"""


def min_value(state, alpha, beta) -> int:
    global depth, depth_limit
    # immediately return the heuristic value for current node when depth limit reached
    depth += 1
    if depth == depth_limit:
        return heuristic(state)

    possible_moves = generating_moves(board)
    v = oo
    for move in possible_moves:
        i = move[0]
        j = move[1]
        make_future_move(state, i, j, 1)
        v = min(v, max_value(state, alpha, beta))
        undo_future_move(state, i, j)
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


"""
    Max-value player (the AI)
"""


def max_value(state, alpha, beta) -> int:
    global depth, depth_limit, ai_move_i, ai_move_j
    # immediately return the heuristic value for current node when depth limit reached
    depth += 1
    if depth == depth_limit:
        return heuristic(state)

    possible_moves = generating_moves(board)
    v = -oo
    for move in possible_moves:
        # make the move
        i = move[0]
        j = move[1]
        make_future_move(state, i, j, 2)
        # need to extract the move if traversing at top node
        if depth == 1:
            min_v = min_value(state, alpha, beta)
            if v < min_v:
                v = min_v
                ai_move_i = i
                ai_move_j = j
        else:
            v = max(v, min_value(state, alpha, beta))
        # undo move
        depth += -1
        undo_future_move(state, i, j)
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def ab_pruning(state) -> int:
    global ai_move_i, ai_move_j
    max_value(board, -oo, oo)
    return ai_move_i, ai_move_j


"""
    AI player make a move
    :return null
"""


def ai_move():
    global board
    state = board
    move_i, move_j = ab_pruning(state)
    make_a_move(board, move_i, move_j, 2)
    print("AI made a move at", move_i, move_j)
    return


"""
    Print board formatted for debugging process.

    NOTE: state is always a 15 * 15 board
"""


def print_format(state):
    for i in range(0, 15):
        for j in range(0, 15):
            print(state[i][j], end=' ')
        print('')
    pass


# Playing board
board = [[0 for i in range(0, 15)] for j in range(0, 15)]

# increments to check for terminal state
increments = [[[-2, 0], [-1, 0], [1, 0], [2, 0]], [[0, -2], [0, -1], [0, 1], [0, 2]],
              [[-2, -2], [-1, -1], [1, 1], [2, 2]], [[-2, 2], [-1, 1], [1, -1], [2, -2]]]

# evaluation points for 1, 2, 3, 4 in a rows (4 is winning state!)
eval_points = [1, 3, 6, 9999]

oo = 1000000
depth = 0
depth_limit = 2
first_layer = True  # Used to extract the actual move that the AI will make
ai_move_i = 0  # AI move
ai_move_j = 0  # AI move

# print_format(board)

turn = 1
count = 0
while count < 5:
    count += 1
    if turn == 1:
        i1, j1 = input().split()
        i1 = int(i1)
        j1 = int(j1)
        make_a_move(board, i1, j1, 1)
        turn = 2
    else:
        ai_move()
        turn = 1

print_format(board)
