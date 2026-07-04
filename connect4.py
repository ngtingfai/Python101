import sys
from copy import deepcopy

ROWS, COLS = 6, 7
AI_PIECE, HUMAN_PIECE = 'O', 'X'
EMPTY = ' '
DEPTH = 6


def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    print('\n' + '-' * 29)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('-' * 29)
    print('  1   2   3   4   5   6   7')


def drop_piece(board, col, piece):
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY:
            board[row][col] = piece
            return row
    return -1


def get_valid_cols(board):
    return [c for c in range(COLS) if board[0][c] == EMPTY]


def is_terminal(board):
    return check_win(board, AI_PIECE) or check_win(board, HUMAN_PIECE) or not get_valid_cols(board)


def check_win(board, piece):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != piece:
                continue
            if c + 3 < COLS and all(board[r][c + i] == piece for i in range(4)):
                return True
            if r + 3 < ROWS and all(board[r + i][c] == piece for i in range(4)):
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == piece for i in range(4)):
                return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == piece for i in range(4)):
                return True
    return False


def score_window(window):
    score = 0
    ai = window.count(AI_PIECE)
    human = window.count(HUMAN_PIECE)
    empty = window.count(EMPTY)

    if ai == 4:
        score += 1000
    elif ai == 3 and empty == 1:
        score += 50
    elif ai == 2 and empty == 2:
        score += 10

    if human == 4:
        score -= 1000
    elif human == 3 and empty == 1:
        score -= 60
    elif human == 2 and empty == 2:
        score -= 10

    return score


def evaluate(board):
    score = 0

    for r in range(ROWS):
        for c in range(COLS - 3):
            score += score_window([board[r][c + i] for i in range(4)])

    for r in range(ROWS - 3):
        for c in range(COLS):
            score += score_window([board[r + i][c] for i in range(4)])

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            score += score_window([board[r + i][c + i] for i in range(4)])

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            score += score_window([board[r - i][c + i] for i in range(4)])

    center = [board[r][COLS // 2] for r in range(ROWS)]
    score += center.count(AI_PIECE) * 3
    score -= center.count(HUMAN_PIECE) * 3

    return score


def minimax(board, depth, alpha, beta, maximizing):
    if is_terminal(board):
        if check_win(board, AI_PIECE):
            return 100000
        elif check_win(board, HUMAN_PIECE):
            return -100000
        else:
            return 0

    if depth == 0:
        return evaluate(board)

    cols = get_valid_cols(board)
    if maximizing:
        value = -float('inf')
        for col in cols:
            b = deepcopy(board)
            drop_piece(b, col, AI_PIECE)
            value = max(value, minimax(b, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for col in cols:
            b = deepcopy(board)
            drop_piece(b, col, HUMAN_PIECE)
            value = min(value, minimax(b, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def get_ai_move(board):
    cols = get_valid_cols(board)
    best_col = cols[0]
    best_score = -float('inf')

    for col in cols:
        b = deepcopy(board)
        drop_piece(b, col, AI_PIECE)
        score = minimax(b, DEPTH - 1, -float('inf'), float('inf'), False)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def play():
    board = create_board()

    while True:
        print_board(board)

        col = -1
        while col == -1:
            try:
                c = int(input(f"Player ({HUMAN_PIECE}), choose a column (1-7): ")) - 1
                if c < 0 or c > 6:
                    print("Column must be between 1 and 7.")
                    continue
                r = drop_piece(board, c, HUMAN_PIECE)
                if r == -1:
                    print("Column is full. Pick another.")
                    continue
                col = c
            except ValueError:
                print("Enter a number between 1 and 7.")

        if check_win(board, HUMAN_PIECE):
            print_board(board)
            print("You win!")
            break

        if not get_valid_cols(board):
            print_board(board)
            print("It's a tie!")
            break

        print("\nComputer is thinking...")
        ai_col = get_ai_move(board)
        drop_piece(board, ai_col, AI_PIECE)

        if check_win(board, AI_PIECE):
            print_board(board)
            print("Computer wins!")
            break

        if not get_valid_cols(board):
            print_board(board)
            print("It's a tie!")
            break


if __name__ == '__main__':
    play()
