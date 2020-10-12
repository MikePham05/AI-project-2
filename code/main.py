import random


def update_tracking(r, c):
    global tracking
    tracking.append([r, c])
    for i in range(-1, 2):
        for j in range(-1, 2):
            if in_board(r + i, c + j):
                nr = r + i
                nc = c + j
                if possible_tracking_state[nr][nc] == 0:
                    possible_tracking_state[nr][nc] = 1
                    possible_tracking.append([nr, nc])
    return


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


def make_a_move(i, j, k) -> bool:
    global board, tracking
    if board[i][j] != 0:
        print("illegal move!, move not registered")
        return False
    board[i][j] = k
    update_tracking(i, j)
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


def generating_moves() -> [[int]]:
    global tracking, possible_tracking, search_tracking, possible_search_state
    # strategy: generate possible moves of all surrounding tiles of actual moves
    # moves = []  # list of moves to consider
    if depth == 1:
        moves = possible_tracking
        search_tracking = possible_tracking
        possible_search_state = possible_tracking_state
    else:
        moves = possible_search_state
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
    # evaluation points for 1, 2, 3, 4 in a rows (4 is winning state!)
    # eval[i, j]: heuristic point of a row, column, diagonal line with i of a kind and j blocking of opponent move
    eval_points = [[0, 32, 64, 9999, 9999], [0, 16, 32, 64, 9999], [0, 0, 0, 0, 9999]]

    return random.randint(0, 10)


def update_search_tracking(r, c, method):
    global new_added_to_search_tracking
    if method == "add":
        for i in range(-1, 2):
            for j in range(-1, 2):
                if in_board(r + i, c + j):
                    nr = r + i
                    nc = c + j
                    if possible_search_state[nr][nc] == 0:
                        possible_search_state[nr][nc] = 1
                        search_tracking.append([nr, nc])
                        new_added_to_search_tracking += 1
    elif method == "remove":
        while new_added_to_search_tracking > 0:
            new_added_to_search_tracking += -1
            search_tracking.pop()
    return


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
    update_search_tracking(i, j, "add")
    return state


"""
    Undo a move. This function is intended for generating states in a search tree only
    :return 
        True if move undo successful
        False otherwise (tile already empty)
"""


def undo_future_move(state, i, j) -> bool:
    if state[i][j] == 0:
        return state
    state[i][j] = 0
    update_search_tracking(i, j, "remove")
    return state


"""
    Min-value player (opposing player)
"""


def min_value(state, alpha, beta) -> int:
    global depth, depth_limit
    # immediately return the heuristic value for current node when depth limit reached
    depth += 1
    if depth == depth_limit:
        return heuristic(state)

    possible_moves = generating_moves()
    # print(depth, search_tracking)

    v = oo
    for move in possible_moves:
        if state[move[0]][move[1]] == 0:
            i = move[0]
            j = move[1]
            state = make_future_move(state, i, j, 1)
            # print("min move made at: ", i, " ", j)
            v = min(v, max_value(state, alpha, beta))
            state = undo_future_move(state, i, j)
            depth += -1
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

    possible_moves = generating_moves()
    # print(depth, search_tracking)

    v = -oo
    for move in possible_moves:
        if state[move[0]][move[1]] == 0:
            # make the move
            i = move[0]
            j = move[1]
            state = make_future_move(state, i, j, 2)
            # print("max move made at: ", i, " ", j)
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
            state = undo_future_move(state, i, j)
            if v >= beta:
                return v
            alpha = max(alpha, v)
    return v


def ab_pruning(state) -> int:
    global ai_move_i, ai_move_j
    max_value(state, -oo, oo)
    return ai_move_i, ai_move_j


"""
    AI player make a move
    :return null
"""


def ai_move():
    global board
    state = [[0 for i in range(0, 15)] for j in range(0, 15)]
    for i in range(0, 15):
        for j in range(0, 15):
            state[i][j] = board[i][j]
    move_i, move_j = ab_pruning(state)
    print("AI made a move at", move_i, move_j)
    return make_a_move(move_i, move_j, 2)


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

# A list used to check what tile on the board has been filled, used for generating new possible states in search tree,
# and keep track of moves even if they are only generated for random search
tracking = []
possible_tracking = []
possible_tracking_state = [[0 for i in range(0, 15)] for j in range(0, 15)]
search_tracking = []
possible_search_state = [[0 for i in range(0, 15)] for j in range(0, 15)]
new_added_to_search_tracking = 0

oo = 1000000
depth = 0
depth_limit = 4
first_layer = True  # Used to extract the actual move that the AI will make
ai_move_i = 0  # AI move
ai_move_j = 0  # AI move

# print_format(board)

turn = 1
count = 0
while not terminal_reached():
    # print(possible_tracking)
    if turn == 1:
        i1, j1 = input().split()
        i1 = int(i1)
        j1 = int(j1)
        if make_a_move(i1, j1, 1):
            turn = 2
    else:
        if ai_move():
            depth = 0  # reset depth
            turn = 1

print_format(board)
