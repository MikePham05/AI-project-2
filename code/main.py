size = 15
board = [[0 for i in range(0, size)] for j in range(0, size)]  # playing board
turn = 1  # player's turn. 1 for human, 2 for AI
last_move = [[], [-1, -1], [-1, -1]]
AI_move = [0, 0]
oo = 1000000000
best_score = -oo
depth_limit = 5
last_future_move = [[], [-1, -1], [-1, -1]]  # used to keep track of future move in calculating new moves
threat_list = [[], [], [], []]
threat_added = []
threat_removed = []


class Threat:
    # inc = [[0, -1, 0, +1], [-1, -1, +1, +1], [-1, 0, +1, 0], [-1, +1, +1, -1]]  # up + down, downleft + upright, right + left, upleft + downright
    def __init__(self, upper_row, upper_col, lower_row, lower_col, blocked, direction, value):
        self.upper_row = upper_row
        self.upper_col = upper_col
        self.lower_row = lower_row
        self.lower_col = lower_col
        self.blocked = blocked
        self.direction = direction
        self.value = value

        
"""Whether square[row][col] is in the board
    
ARGS:
    row, col(int): number of row and column
    
RETURN:
    bool: whether square is in the board
"""
def in_board(row, column) -> bool:
    return 0 <= row <= 14 and 0 <= column <= 14


"""Count number of consecutive values in a line of same move in a certain direction

ARGS:
    r, c(int): row and column of square
    direction(int): 0 -> 3 
 
RETURN: Starting and endling points of line [upper pivot r, upper pivot c, lower pivot r, lower pivot c]
"""
def count_consecutive(r, c, direction) -> [int]:
    res = [-1, -1, -1, -1]
    if not in_board(r, c):
        return res
    inc = [[0, -1, 0, +1], [-1, -1, +1, +1], [-1, 0, +1, 0], [-1, +1, +1, -1]]
    i = direction
    row = r
    column = c
    val = board[row][column]
    while in_board(row, column) and board[row][column] == val:
        row += inc[i][0]
        column += inc[i][1]
    res[0] = row
    res[1] = column
    row = r
    column = c
    while in_board(row, column) and board[row][column] == val:
        row += inc[i][2]
        column += inc[i][3]
    res[2] = row
    res[3] = column
    return res



"""Return when the game is over, 1 player is victorious

ARGS: None

RETURN: val(Bool): Whether the game has ended
"""
def game_ended() -> bool:
    if last_move[turn][0] < 0:  # last move not recorded, game just started
        return False

    row = last_move[3 - turn][0]
    column = last_move[3 - turn][1]
    val = board[row][column]
    # inc = [[-1, 0, +1, 0], [-1, +1, +1, -1], [0, + 1, 0, -1], [+1, +1, -1, -1]]  # up + down, downleft + upright, right + left, upleft + downright
    for i in range(0, 4):
        pivot = count_consecutive(row, column, i)
        if abs(pivot[2] - pivot[0]) >= 6 or abs(pivot[3] - pivot[1]) >= 6:  # in between pivots, there are 5 consecutive
            print(val)
            return val
    return 0



"""Check obvious moves that will have to be played for the best outcome at that position

ARGS: None

RETURN: list [[int]]: Obvious winning move
"""


def check_ending_move() -> [[int]]:
    """
    step 1
    your last_move r1, c1 (AI move)
    * span up, and down: get count of consecutive move with r1, c1
    if count + unblock at 1 end + 4 - count more after that end -> return winning move

    same with step 2, but for opposing player
    * BECAUSE FOR THESE 2 STEPS, IF THEY EXIST, THE MOVE IS ALWAYS FORCED TO BE IN THE UNBLOCKED
    SQUARE WHICH WOULD RESULT IN IMMEDIATE END GAME, WE JUST NEED TO CHECK IF PATTERN EXISTS,
    REGARDLESS THE ACTUAL VALUE OF THE SQUARE
    * NEEDS GENERALIZATION WITH A FUNCTION   
    """
    # GAME-ENDING MOVES
    # step 1: attack 4 blocked 1 or unblocked, yes move that wins the game for player + return that move, no -> next step
    # step 2: defend 4 blocked 1, yes -> only valid move that saved the game + return that move, no -> next step
    # step 3: attack 3 unblocked, yes -> move that wins the game for player + return that move, no -> next step
    # step 4: defend 3 unblocked, yes -> only valid move that saved the game + return that move, no -> next step

    inc = [[0, -1, 0, +1], [-1, -1, +1, +1], [-1, 0, +1, 0], [-1, +1, +1, -1]]  # up + down, downleft + upright, right + left, upleft + downright
    blocked = dict()

    # step 1 first, then step 2 with threat type 4 first
    # step 3, then step 4 with threat type 3 second
    for threat in range(4, 2, -1):
        for i in range(2, 0, -1):  # step 1 (or step 3 first), then step 2 (or step 4) second
            row = last_future_move[i][0]
            column = last_future_move[i][1]
            val = board[row][column]
            for j in range(0, 4):
                blocked.__setitem__("up", "unblocked")
                blocked.__setitem__("down", "unblocked")
                row = last_future_move[i][0]
                column = last_future_move[i][1]
                p = count_consecutive(row, column, j)
                count = max(abs(p[2] - p[0]), abs(p[3] - p[1])) - 1
                if not in_board(p[0], p[1]) or board[p[0]][p[1]] == 3 - i:
                    blocked.__setitem__("up", "blocked")
                if not in_board(p[2], p[3]) or board[p[2]][p[3]] == 3 - i:
                    blocked.__setitem__("down", "blocked")

                # go up to check for winning condition
                if blocked.__getitem__("up") == "unblocked":
                    c = count
                    row = p[0] + inc[j][0]
                    column = p[1] + inc[j][1]
                    while in_board(row, column) and board[row][column] == val:
                        c += 1
                        row += inc[j][0]
                        column += inc[j][1]
                    if threat == 4 and c == 4:  # found winning attack move or point less defense move
                        return [p[0:2]]
                    if threat == 3 and c == 3 and blocked.__getitem__("down") == "unblocked" and board[row][column] == 0:  # found winning attack move
                        if i == 2:  # in attack mode
                            return [p[0:2]]
                        else:  # in defense mode, 3 moves possible
                            return [p[0:2], p[2:4], [row, column]]

                if blocked.__getitem__("down") == "unblocked":
                    c = count
                    row = p[2] + inc[j][2]
                    column = p[3] + inc[j][3]
                    while in_board(row, column) and board[row][column] == val:
                        c += 1
                        row += inc[j][2]
                        column += inc[j][3]
                    if threat == 4 and c == 4:  # found winning move
                        return [p[2:4]]
                    if threat == 3 and c == 3 and blocked.__getitem__("up") == "unblocked" and board[row][column] == 0:
                        if i == 2:  # in attack mode
                            return [p[2:4]]
                        else:  # in defense mode, 3 moves possible
                            return [p[0:2], p[2:4], [row, column]]
    return []  # did not found the winning move


"""Generates hypothetical moves for player player

ARGS: Player(int) current player turn's (0 or 1)

RETURN: result_list([[int]]): List of move to consider to that player at the point of the game
"""


def generate_moves(player) -> [[int]]:
    result_list = []
    # GAME-ENDING MOVES FIRST
    # NON-GAME-ENDING MOVES
    # step 5: consider strategical attack or defenses

    # STEP 1, 2, 3, 4
    ending_moves = check_ending_move()
    if len(ending_moves) > 0:  # ending_move found
        return ending_moves

    # STEP 5
    """
    computational allowance S = 50000000 (5 * 10^7)
    depth of tree 15: 100, 3,3 * 10^6 per depth on average
    
    --> optimal list of moves should have a size of a, where:
        a^1 + a^2 + ... + a^15 = S
    """
    return result_list


""" #TODO
    Return: heuristic evaluation for the current board position
"""


def heuristic():
    return 0


def update_threat(r, c, type):
    inc = [[0, -1, 0, +1], [-1, -1, +1, +1], [-1, 0, +1, 0], [-1, +1, +1, -1]]
    blocked = dict()
    for i in range(0, 4):  # direction
        blocked.__setitem__("up", "unblocked")
        blocked.__setitem__("down", "unblocked")

    """
            for j in range(0, 4):
            blocked.__setitem__("up", "unblocked")
            blocked.__setitem__("down", "unblocked")
            row = last_future_move[i][0]
            column = last_future_move[i][1]
            if j == 2:
                a = 1
            p = count_consecutive(row, column, j)
            count = max(abs(p[2] - p[0]), abs(p[3] - p[1])) - 1
            if not in_board(p[0], p[1]) or board[p[0]][p[1]] == 3 - i:
                blocked.__setitem__("up", "blocked")
            if not in_board(p[2], p[3]) or board[p[2]][p[3]] == 3 - i:
                blocked.__setitem__("down", "blocked")
    """
    return


""" Min_value function, which choose best move adn optimizing search process for pruning

ARGS:   alpha (int): alpha best evalution point for human
        beta (int): beta best evaluation point for computer
        depth (int): depth of current search

RETURN: v (int) best value achivable at current node
"""


def min_value(alpha, beta, depth):
    if depth == depth_limit:  # if reach depth limit, terminate, return heu value
        return heuristic()
    term = game_ended()  # if reach terminal state, terminate
    if term == 1:  # humans win, return -inf
        return -oo
    elif term == 2:  # AI win, return +inf
        return oo

    moves = generate_moves(1)  # generate a list move to consider
    v = +oo
    for move in moves:
        # make a hypothetical move
        r = move[0]
        c = move[1]
        board[r][c] = 1
        last_future_move[1][0] = r
        last_future_move[1][1] = c
        update_threat(r, c, "make move")
        v = min(v, max_value(alpha, beta, depth + 1))
        if v <= alpha:
            return v
        beta = min(beta, v)
        # undo hypothetical move for further calculation
        update_threat(r, c, "undo move")
        board[r][c] = 0
    return v

""" Max_value function, which choose best move adn optimizing search process for pruning

ARGS:   alpha (int): alpha best evalution point for human
        beta (int): beta best evaluation point for computer
        depth (int): depth of current search

RETURN: v (int) best value achivable at current node
"""


def max_value(alpha, beta, depth):
    global AI_move, best_score  # used to extract actual move for AI at depth 0
    if depth == depth_limit:  # if reach depth limit, terminate
        return heuristic()

    term = game_ended()   # if reach terminal state, terminate
    if term == 1:  # humans win, return -inf
        return -oo
    elif term == 2:  # AI win, return +inf
        return oo

    moves = generate_moves(2)  # generate a list of new moves to consider
    v = -oo
    for i in range(0, len(moves)):
        # make a hypothetical move
        r = moves[i][0]
        c = moves[i][1]
        board[r][c] = 2  # AI's hypothetical move
        last_future_move[2][0] = r
        last_future_move[2][1] = c
        update_threat(r, c, "make move")
        v = max(v, min_value(alpha, beta, depth + 1))  # goes further down the tree
        if depth == 0 and v > best_score:  # depth at 0, requires move to return for the AI
            best_score = v
            AI_move = [r, c]
        if v >= beta:
            return v
        alpha = max(alpha, v)
        board[r][c] = 0  # undo AI's hypothetical move
        update_threat(r, c, "undo move")
    return v


""" Running AB prunning algorithm
ARGS: NONE
RETURNS: NONE
"""


def ab_pruning():
    global best_score
    best_score = -oo  # reset best score for new pruning
    max_value(-oo, oo, 0)  # calculating next move
    row = AI_move[0]  # move has been updated
    column = AI_move[1]
    return 0, 0

""" GAME PLAYING OVER THE BOARD. GAME ABORTED WHEN A PLAYER WINS
ARGS: NONE
RETURN NONE
"""


def game_playing():
    global turn, board
    while game_ended() == 0:
        if turn == 1:  # human's turn
            row, column = [int(a) for a in input().split()]
        else:  # AI turn
            row, column = ab_pruning()
        update_threat(row, column, "make move")
        last_move[turn][0] = row
        last_move[turn][1] = column
        last_future_move[turn][0] = row
        last_future_move[turn][1] = column
        board[row][column] = turn
        turn = 3 - turn  # switch turn
    pass


def initialization():
    pass


if __name__ == "__main__":
    for i in range(4, 7):
        board[12][i] = 2
        board[i][i] = 1
    board[12][6] = 0
    board[12][7] = 2
    last_future_move[1] = [4, 4]
    last_future_move[2] = [12, 4]
    print(check_ending_move())
    initialization()
    game_playing()
