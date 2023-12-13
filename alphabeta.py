def is_terminal(board):
    pass


def evaluate(board):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] is not None:
                for dx, dy in directions:
                    if check_five_in_a_row(board, x, y, dx, dy):
                        return 1 if board[x][y] == 'black' else -1
    return 0


def check_five_in_a_row(board, x, y, dx, dy):
    color = board[x][y]
    for i in range(1, 5):
        nx, ny = x + i * dx, y + i * dy
        if not (0 <= nx < len(board) and 0 <= ny < len(board[nx]) and board[nx][ny] == color):
            return False
    return True


def get_children(board):
    # 返回所有可能的下一步棋盘状态
    children = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                for color in ['black', 'white']:
                    new_board = [row.copy() for row in board]
                    new_board[i][j] = color
                    children.append(new_board)
    return children


def get_possible_moves(board):
    # 返回所有可能的下一步棋的坐标
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                moves.append((i, j))
    return moves


def make_move(board, move, color):
    # 在指定的位置放下一个棋子
    new_board = [row.copy() for row in board]
    x, y = move
    new_board[x][y] = color
    return new_board


def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or is_terminal(board):
        return evaluate(board)

    if maximizingPlayer:
        value = -float('inf')
        for child in get_children(board):
            value = max(value, alphabeta(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for child in get_children(board):
            value = min(value, alphabeta(child, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def calculate_ai_move(board, ai_player, depth=5):
    best_move = None
    best_value = -float('inf')

    for move in get_possible_moves(board):
        new_board = make_move(board, move, ai_player)
        value = alphabeta(new_board, depth, -float('inf'),
                          float('inf'), ai_player == 'black')
        if value > best_value:
            best_value = value
            best_move = move

    if best_move is None:
        print('No move found')
        return None
    else:
        print('Found best move: %s' % (best_move,))
        return best_move
