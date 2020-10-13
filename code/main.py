import random

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
    Generating children of a node in the search tree. Children created are created according to
    the algorithm implemented in this function. 
    The algorithm is: #TODO
    NOTE: THIS FUNCTION HIGHLY DETERMINES EFFECTIVENESS OF AI'S MOVE. REQUIRES GREAT ATTENTION
    
    :var
        state: current state of the node
        player: the turn the player is playing
        r, c: newest move on the board
    :return
        moves: a list of possible move from the current state of the board
"""


def threat_detect(state, r, c) -> [[int]]:
    # return a series of game ending moves, if possible, benefits player p
    moves = []
    # traverse in 4 directions around the cell: top left + down right, up down, top right + down left, left right
    increment = [[-1, -1, + 1, + 1], [-1, 0, 1, 0], [-1, + 1, + 1, -1], [0, -1, 0, +1]]
    for i in range(0, 4):
        nr = r
        nc = c
        count_consecutive = 0  # count the number of consecutive moves
        player = state[r][c]
        while in_board(nr, nc) and state[nr][nc] == player:
            count_consecutive += 1
            nr += increment[i][0]
            nc += increment[i][1]
        pivot_r1 = nr
        pivot_c1 = nc
        nr = r
        nc = c
        while in_board(nr, nc) and state[nr][nc] == player:
            count_consecutive += 1
            nr += increment[i][2]
            nc += increment[i][3]
        pivot_r2 = nr
        pivot_c2 = nc
        count_consecutive += -1  # account for counting state[r][c] twice

        # threat type urgent, next move if move is possible will end the game
        if count_consecutive == 4 or count_consecutive == 3:
            if in_board(pivot_r1, pivot_c1) and state[pivot_r1][pivot_c1] == 0:  # game ending move found
                moves.append([pivot_r1, pivot_c1])
                return moves
            elif in_board(pivot_r2, pivot_c2) and state[pivot_r2][pivot_c2] == 0:
                moves.append([pivot_r2, pivot_c2])
                return moves
            else:  # blocked at both pivots, move is no longer win cond
                continue
        elif count_consecutive == 2:
            # move in radius of 2 tiles in same direction of the consecutive line of moves
            if in_board(pivot_r1, pivot_c1) and in_board(pivot_r2, pivot_c2) and state[pivot_r1][pivot_c1] == 0 and state[pivot_r2][pivot_c2] == 0:
                if in_board(pivot_r1 + increment[i][0], pivot_c1 + increment[i][1]) and state[pivot_r1 + increment[i][0]][pivot_c1 + increment[i][1]] == player:
                    moves.extend([[pivot_r1, pivot_c1], [pivot_r2, pivot_c2]])
                    if in_board(pivot_r1 + increment[i][0] * 2, pivot_c1 + increment[i][1] * 2):
                        moves.append([pivot_r1 + increment[i][0] * 2, pivot_c1 + increment[i][1] * 2])
                    return moves
                if in_board(pivot_r2 + increment[i][2], pivot_c2 + increment[i][3]) and state[pivot_r2 + increment[i][2]][pivot_c2 + increment[i][3]] == player:
                    moves.extend([[pivot_r1, pivot_c1], [pivot_r2, pivot_c2]])
                    if in_board(pivot_r2 + increment[i][2] * 2, pivot_c2 + increment[i][3] * 2):
                        moves.append([pivot_r2 + increment[i][2] * 2, pivot_c2 + increment[i][3] * 2])
                    return moves
        elif count_consecutive == 1:
            if in_board(pivot_r1, pivot_c1) and in_board(pivot_r2, pivot_c2) and state[pivot_r1][pivot_c1] == 0 and state[pivot_r2][pivot_c2] == 0:
                if in_board(pivot_r1 + increment[i][0] * 2, pivot_c1 + increment[i][1] * 2) and state[pivot_r1 + increment[i][0] * 2][pivot_c1 + increment[i][1] * 2] == player:
                    if in_board(pivot_r1 + increment[i][0], pivot_c1 + increment[i][1]) and state[pivot_r1 + increment[i][0]][pivot_c1 + increment[i][1]] == player:
                        moves.extend([[pivot_r1, pivot_c1], [pivot_r2, pivot_c2]])
                        if in_board(pivot_r1 + increment[i][0] * 3, pivot_c1 + increment[i][1] * 3) and state[pivot_r1 + increment[i][0] * 3][pivot_c1 + increment[i][1] * 3] == player:
                            moves.append([pivot_r1 + increment[i][0] * 3, pivot_c1 + increment[i][1] * 3])
                if in_board(pivot_r2 + increment[i][2] * 2, pivot_c2 + increment[i][3] * 2) and state[pivot_r2 + increment[i][2] * 2][pivot_c2 + increment[i][3] * 2] == player:
                    if in_board(pivot_r2 + increment[i][2], pivot_c2 + increment[i][3]) and state[pivot_r2 + increment[i][2]][pivot_c2 + increment[i][3]] == player:
                        moves.extend([[pivot_r1, pivot_c1], [pivot_r2, pivot_c2]])
                        if in_board(pivot_r2 + increment[i][2] * 3, pivot_c2 + increment[i][3] * 3) and state[pivot_r2 + increment[i][2] * 3][pivot_c2 + increment[i][3] * 3] == player:
                            moves.append([pivot_r2 + increment[i][2] * 3, pivot_c2 + increment[i][3] * 3])

    return moves  # no threat is found


"""
note; 2 lines of 2 unblocked > 1 line of 3 blocked
"""


def generate(state, player):
    # list of moves that player makes a hypothetical moves at state
    moves = []
    track_moves = [[0 for i in range(0, 15)] for j in range(0, 15)]
    dir = [[+1, -1], [+1, 0], [+1, +1], [0, +1]]  # 0 down left, 1 down, 2 down right, 3 right
    opposite_dir = [[-1, +1], [-1, 0], [-1, -1], [0, -1]]  # opposite corresponds to dir
    dir_tracking = [[[0 for i in range(0, 4)] for j in range(0, 15)] for k in range(0, 15)]
    for move in moves_made_during_search:
        r = move[0]
        c = move[1]
        val = state[r][c]
        for i in range(0, 4):
            # reset
            r = move[0]
            c = move[1]
            num_same = 0  # number of consecutive 1 of a kind
            while in_board(r, c) and state[r][c] == val:
                dir_tracking[r][c][i] = 1
                num_same += 1
                r += dir[i][0]
                c += dir[i][1]
            pivot_lower_r = r
            pivot_lower_c = c
            pivot_upper_r = move[0] + opposite_dir[i][0]
            pivot_upper_c = move[1] + opposite_dir[i][1]
            blocked_upper = False
            blocked_lower = False
            if not in_board(pivot_upper_r, pivot_upper_c) or state[pivot_upper_r][pivot_upper_c] == 3 - player:
                blocked_upper = True
            if not in_board(pivot_lower_r, pivot_lower_c) or state[pivot_lower_r][pivot_lower_c] == 3 - player:
                blocked_lower = True

            """
                Possible attack:
                    line of 3 block 1: from a side, 2 options: either block 4 or block 5
                    line of 2 non block: either side, 4 options: block 3 and 4 from either side
                    line of 1 non block: from surrounding, up to 8 options
                    
                Possible defense
                    line of 3 block 1: from only a side, either block 4 or 5
                    line of 2 non block: either side
                    line of 1 block: surrounding blocks
            """

            if num_same == 3 or (num_same == 2 and val == player):  # both attack and defense
                if not blocked_upper:
                    count = 0
                    while in_board(pivot_upper_r, pivot_upper_c) and state[pivot_upper_r][pivot_upper_c] == 0 and count < 2:  # not blocked, only 2 blocks upper
                        if track_moves[pivot_upper_r][pivot_upper_c] == 0:
                            track_moves[pivot_upper_r][pivot_upper_c] = 1
                            moves.append([pivot_upper_r, pivot_upper_c])
                        pivot_upper_r += opposite_dir[i][0]
                        pivot_upper_c += opposite_dir[i][1]
                        count += 1
                if not blocked_lower:
                    count = 0
                    while in_board(pivot_lower_r, pivot_lower_c) and state[pivot_lower_r][pivot_lower_c] == 0 and count < 2:  # not blocked, only 2 blocks upper
                        if track_moves[pivot_lower_r][pivot_lower_c] == 0:
                            track_moves[pivot_lower_r][pivot_lower_c] = 1
                            moves.append([pivot_lower_r, pivot_lower_c])
                        pivot_lower_r += dir[i][0]
                        pivot_lower_c += dir[i][1]
                        count += 1
            elif num_same == 1:  # 1 of a kind, only get surrounding moves
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if in_board(move[0] + j, move[1] + k) and track_moves[move[0] + j][move[1] + k] == 0 and state[move[0] + j][move[1] + k] == 0:
                            track_moves[move[0] + j][move[1] + k] = 1
                            moves.append([move[0] + j, move[1] + k])

            if val == 3 - player and num_same == 2:  # defense
                if in_board(pivot_upper_r, pivot_upper_c) and state[pivot_upper_r][pivot_upper_c] == 0:
                    if track_moves[pivot_upper_r][pivot_upper_c] == 0:
                        track_moves[pivot_upper_r][pivot_upper_c] = 1
                        moves.append([pivot_upper_r, pivot_upper_c])
            if in_board(pivot_lower_r, pivot_lower_c) and state[pivot_lower_r][pivot_lower_c] == 0:
                if track_moves[pivot_lower_r][pivot_lower_c] == 0:
                    track_moves[pivot_lower_r][pivot_lower_c] = 1
                    moves.append([pivot_lower_r, pivot_lower_c])
    return moves


def update_possible_moves(state, player) -> [[int]]:
    # update possible moves for player player
    # strategy:
    # threat: threat is the moves that threaten to win the game if not defended
    # if winning condition exists, only return winning move
    # if threat exists, only return the defensive move to prevent loss condition
    # if not: consider 2 options: attack and defense
    # Attack: see if there's any line of AI move that can makes a ver, horizontal, diagonal line:
    # add a move from either side
    # Defense: same, but this time, with a line of opponents move, defense only viable thru moves that have at least
    # 2 consecutive moves
    moves = []

    # check game ending condition
    game_win_ending = threat_detect(state, last_search_move[player - 1][0], last_search_move[player - 1][1])
    if len(game_win_ending) > 0:  # win game ending condition found
        # player win condition found
        moves.append(game_win_ending[0])
        return moves

    game_lose_ending = threat_detect(state, last_search_move[2 - player][0], last_search_move[2 - player][1])
    if len(game_lose_ending) > 0:  # Opposing player of playing win cond found, lose condition found
        return game_lose_ending  # return these moves as compulsory defensive move to prevent loss, to test which one is the most heuristically beneficial

    # no win cond found, attack!
    # attack on non terminal state
    moves.extend(generate(state, player))

    # no win cond found, defense!
    # defend on non-terminal state

    heuristic_state = heuristic(state)
    for move in moves:
        # apply move, calculate new heuristic, sort moves according to newly calculated heuristic values
        a = 0  # TODO
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
    # eval[i, j]: heuristic point of a row, column, diagonal line with j of a kind and i blocking of opponent move
    eval_points = [[0, 0, 30, 100, 9999, 9999], [0, 0, 10, 30, 100, 9999], [0, 0, 0, 0, 0, 9999]]
    heu_dir = [[+1, -1], [+1, 0], [+1, +1], [0, +1]]  # 0 down left, 1 down, 2 down right, 3 right
    heu_block = [[-1, +1], [-1, 0], [-1, -1], [0, -1]]  # Block corresponds to heu_dir_tracking
    heu_dir_tracking = [[[0 for i in range(0, 4)] for j in range(0, 15)] for k in range(0, 15)]
    heuristic_sum = 0
    list_of_moves = moves_made_during_search + actual_moves
    for move in list_of_moves:
        r = move[0]
        c = move[1]
        player = state[r][c]
        for i in range(0, 4):
            block_r = r + heu_block[i][0]
            block_c = c + heu_block[i][1]
            # only consider if there is no adjacent upper move by same player and block in this direction "i" has not
            # been considered before
            if in_board(block_r, block_c) and state[block_r][block_c] != player and heu_dir_tracking[r][c][i] == 0:
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
    return heuristic_sum


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
    if track_moves_made_during_search[i][j] == 0:
        track_moves_made_during_search[i][j] = 1
        moves_made_during_search.append([i, j])
    last_search_move[k - 1] = [i, j]
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
    track_moves_made_during_search[i][j] = 0
    moves_made_during_search.remove([i, j])
    return state


"""
    Min-value player (opposing player)
"""


def min_value(state) -> int:
    global depth, depth_limit, alpha, beta
    if terminal_reached(state, last_search_move[1][0], last_search_move[1][1]):  # terminal reached by max'move, min lost
        return oo

    # immediately return the heuristic value for current node when depth limit reached
    depth += 1
    if depth >= depth_limit:
        return heuristic(state)

    v = oo
    list_of_possible_moves = update_possible_moves(state, 1)
    for move in list_of_possible_moves:
        if state[move[0]][move[1]] == 0:
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
    if terminal_reached(state, last_search_move[0][0], last_search_move[0][1]):  # terminal reached by min'move, max lost
        return -oo

    depth += 1
    if depth >= depth_limit:
        return heuristic(state)

    v = -oo
    list_of_possible_moves = update_possible_moves(state, 2)
    # print(list_of_possible_moves)
    for move in list_of_possible_moves:
        if state[move[0]][move[1]] == 0:
            # make the move
            i = move[0]
            j = move[1]
            state = make_future_move(state, i, j, 2)
            if depth == 1:
                # move to registered if state is valid
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
    global ai_move_i, ai_move_j, moves_made_during_search
    moves_made_during_search = []
    for move in actual_moves:
        moves_made_during_search.append(move)
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


def update_tracking(r, c):
    actual_moves.append([r, c])
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
    # k = 2, player
    last_search_move[k - 1] = [i, j]
    update_tracking(i, j)
    return True


"""
    Checking terminal condition. The game reaches end condition when a row, column or a diagonal lines of 5 of the
    moves from a same player exists. 

    :var
        state: current state of the board that we want to consider
        last_move_r, last_move_c: last move made on the board
        

    :return
        True if The game has ended 
        False otherwise
"""


def terminal_reached(state, last_move_r, last_move_c) -> bool:
    increment = [[-1, -1, + 1, + 1], [-1, 0, 1, 0], [-1, + 1, + 1, -1], [0, -1, 0, +1]]
    for i in range(0, 4):
        nr = last_move_r
        nc = last_move_c
        count_consecutive = 0  # count the number of consecutive moves
        player = state[last_move_r][last_move_c]
        while in_board(nr, nc) and state[nr][nc] == player:
            count_consecutive += 1
            nr += increment[i][0]
            nc += increment[i][1]
        nr = last_move_r
        nc = last_move_c
        while in_board(nr, nc) and state[nr][nc] == player:
            count_consecutive += 1
            nr += increment[i][2]
            nc += increment[i][3]
        count_consecutive += -1  # account for original moved being counted twice
        if count_consecutive == 5:
            return True
    return False


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
actual_moves = []  # A list of actual moves made in the game
last_search_move = [[0, 0], [0, 0]]  # last move in the search for both player
moves_made_during_search = []  # for heuristic calculation
track_moves_made_during_search = [[0 for i in range(0, 15)] for j in range(0, 15)]  # O(1) access for what move have been made during the search

oo = 1000000
depth = 0
depth_limit = 6
first_layer = True  # Used to extract the actual move that the AI will make
ai_move_i = 0  # AI move
ai_move_j = 0  # AI move
alpha = -oo
beta = oo

i1, j1 = input().split()
i1 = int(i1)
j1 = int(j1)
make_a_move(i1, j1, 1)
turn = 2
while not terminal_reached(board, actual_moves[-1][0], actual_moves[-1][1]):
    print_format(board)
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
