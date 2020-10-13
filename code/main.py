import random


def update_tracking(r, c):
    actual_moves.append([r, c])
    update_possible_moves(r, c, "add")
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
    global board
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


def update_possible_moves(r, c, method) -> [[int]]:
    # strategy: generate possible moves of all surrounding tiles of actual moves
    for i in range(-1, 2):
        for j in range(-1, 2):
            if in_board(r + i, c + j):
                nr = r + i
                nc = c + j
                if method == "add":
                    if track_possible_moves[nr][nc] == 0:
                        possible_moves.append([nr, nc])
                    track_possible_moves[nr][nc] += 1
                else:
                    track_possible_moves[nr][nc] += -1
                    if track_possible_moves[nr][nc] == 0:
                        possible_moves.remove([nr, nc])
    return


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
    # eval[i, j]: heuristic point of a row, column, diagonal line with j of a kind and i blocking of opponent move
    eval_points = [[0, 0, 30, 100, 9999, 9999], [0, 0, 10, 30, 100, 9999], [0, 0, 0, 0, 0, 9999]]
    heu_dir = [[+1, -1], [+1, 0], [+1, +1], [0, +1]]  # 0 down left, 1 down, 2 down right, 3 right
    heu_block = [[-1, +1], [-1, 0], [-1, -1], [0, -1]]  # Block corresponds to heu_dir_tracking
    heu_dir_tracking = [[[0 for i in range(0, 4)] for j in range(0, 15)] for k in range(0, 15)]
    heuristic_sum = 0
    # print_format(state)
    list_of_moves = moves_made_during_search + actual_moves
    for move in list_of_moves:
        r = move[0]
        c = move[1]
        player = state[r][c]
        for i in range(0, 4):
            block_r = r + heu_block[i][0]
            block_c = c + heu_block[i][1]
            # only consider if there is no adjacent upper move by same player and block in this direction "i" has not been considered before
            if state[block_r][block_c] != player and heu_dir_tracking[r][c][i] == 0:
                heu_dir_tracking[r][c][i] = 1
                nr = r
                nc = c
                num_block = 0
                num_same = 0
                if (not in_board(block_r, block_c)) or (state[block_r][block_c] == 3 - player):
                    num_block += 1  # there's block
                while in_board(nr, nc) and state[nr][nc] == player:
                    heu_dir_tracking[nr][nc][i] = 1
                    nr = nr + heu_dir[i][0]
                    nc = nc + heu_dir[i][1]
                    num_same += 1
                if (not in_board(nr, nc)) or (state[nr][nc] == 3 - player):
                    num_block += 1  # there's block
                if player == 2:  # AI player
                    heuristic_sum = heuristic_sum + eval_points[num_block][num_same]
                else:  # opposing player
                    heuristic_sum = heuristic_sum - eval_points[num_block][num_same]
    if heuristic_sum < -9000:
        print_format(state)
    return heuristic_sum


def update_search_tracking(r, c, method):
    if method == "add":
        a = 0
    elif method == "remove":
        a = 0
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
    moves_made_during_search.append([i, j])
    track_moves_made_during_search[i][j] = 1
    update_possible_moves(i, j, "add")
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
    moves_made_during_search.remove([i, j])
    track_moves_made_during_search[i][j] = 0
    update_possible_moves(i, j, "remove")
    return state


"""
    Min-value player (opposing player)
"""


def min_value(state) -> int:
    global depth, depth_limit, alpha, beta
    # immediately return the heuristic value for current node when depth limit reached
    depth += 1
    if depth >= depth_limit:
        return heuristic(state)

    v = oo
    for move in possible_moves:
        if (board[move[0]][move[1]] == 0) and (track_moves_made_during_search[move[0]][move[1]] == 0):
            i = move[0]
            j = move[1]
            state = make_future_move(state, i, j, 1)
            v = min(v, max_value(state))
            state = undo_future_move(state, i, j)
            depth += -1
            if v <= alpha:
                return v
            beta = min(beta, v)
    return v


"""
    Max-value player (the AI)
"""


def max_value(state) -> int:
    global depth, depth_limit, ai_move_i, ai_move_j, alpha, beta
    # immediately return the heuristic value for current node when depth limit reached
    depth += 1
    if depth >= depth_limit:
        return heuristic(state)

    v = -oo
    for move in possible_moves:
        if (board[move[0]][move[1]] == 0) and (track_moves_made_during_search[move[0]][move[1]] == 0):
            # make the move
            i = move[0]
            j = move[1]
            state = make_future_move(state, i, j, 2)
            if depth == 1:
                min_v = min_value(state)
                if v < min_v:
                    v = min_v
                    ai_move_i = i
                    ai_move_j = j
            else:
                v = max(v, min_value(state))
            # undo move
            depth += -1
            state = undo_future_move(state, i, j)
            if v >= beta:
                return v
            alpha = max(alpha, v)
    return v


def ab_pruning(state) -> int:
    global ai_move_i, ai_move_j
    print(max_value(state))
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
possible_moves = []  # A list of possible moves at each minimax traversal
actual_moves = []  # A list of actual moves made in the game
track_possible_moves = [[0 for i in range(0, 15)] for j in range(0, 15)]   # O(1) access for tracking elements in possible_moves
moves_made_during_search = []  # for heuristic calculation
track_moves_made_during_search = [[0 for i in range(0, 15)] for j in range(0, 15)]

oo = 1000000
depth = 0
depth_limit = 5
first_layer = True  # Used to extract the actual move that the AI will make
ai_move_i = 0  # AI move
ai_move_j = 0  # AI move
alpha = -oo
beta = oo

print_format(board)

turn = 1
count = 0
while not terminal_reached():
    # print(possible_tracking)
    # print_format(board)
    if turn == 1:
        i1, j1 = input().split()
        i1 = int(i1)
        j1 = int(j1)
        if make_a_move(i1, j1, 1):
            turn = 2
    else:
        if ai_move():
            alpha = -oo
            beta = oo
            depth = 0  # reset depth
            turn = 1

print_format(board)
