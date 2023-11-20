from tkinter import *
import numpy as np

board = np.empty(shape=(5, 6), dtype=str)
board.fill(' ')

is_game_ended: bool = False


def draw_win(x, y, row=False, col=False, diag1=False, diag2=False, is_draw_enable2: bool = False):
    if is_draw_enable2:
        print(x, y)
        global is_game_ended

        if row != -1 or col != -1 or diag1 != -1 or diag2 != -1:
            is_game_ended = True

            if row:
                canvas.create_line(y * 100, x * 100 + 50, y * 100 + 400, x * 100 + 50, fill="#ff5c5c", width=3)

            if col:
                canvas.create_line(y * 100 + 50, x * 100, y * 100 + 50, x * 100 + 400, fill="#ff5c5c", width=3)

            if diag1:
                canvas.create_line(y * 100, x * 100, y * 100 + 400, x * 100 + 400, fill="#ff5c5c", width=3)

            if diag2:
                canvas.create_line(y * 100 - 300, x * 100 + 400, y * 100 + 100, x * 100, fill="#ff5c5c", width=3)


def check_game_state(is_draw_enable: bool = False):
    for i in range(2):
        for j in range(3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                if board[i][j] == 'r':
                    draw_win(i, j, diag1=True, is_draw_enable2=is_draw_enable)
                    return 1
                if board[i][j] == 'y':
                    draw_win(i, j, diag1=True, is_draw_enable2=is_draw_enable)
                    return -1

    for i in range(2):
        for j in range(3, 6):
            if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3]:
                if board[i][j] == 'r':
                    draw_win(i, j, diag2=True, is_draw_enable2=is_draw_enable)
                    return 1
                if board[i][j] == 'y':
                    draw_win(i, j, diag2=True, is_draw_enable2=is_draw_enable)
                    return -1

    for i in range(5):
        for j in range(3):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3]:
                if board[i][j] == 'r':
                    draw_win(i, j, row=True, is_draw_enable2=is_draw_enable)
                    return 1
                if board[i][j] == 'y':
                    draw_win(i, j, row=True, is_draw_enable2=is_draw_enable)
                    return -1

    for i in range(2):
        for j in range(6):
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]:
                if board[i][j] == 'r':
                    draw_win(i, j, col=True, is_draw_enable2=is_draw_enable)
                    return 1
                if board[i][j] == 'y':
                    draw_win(i, j, col=True, is_draw_enable2=is_draw_enable)
                    return -1

    for i in range(5):
        for j in range(6):
            if board[i][j] == ' ':
                return 4

    return 0


def draw_red(x: int, y: int):
    offset = 10

    if board[x][y] == ' ':
        board[x][y] = 'r'

        canvas.create_oval(y * 100 + offset, x * 100 + offset, y * 100 + 100 - offset, x * 100 + 100 - offset,
                           fill="#dc96ff", outline="#dc96ff")

        print(check_game_state(is_draw_enable=True))


def draw_yellow(event):
    offset = 10
    y = int(event.x / 100)

    for x in range(4, -1, -1):
        if board[x][y] == ' ':
            board[x][y] = 'y'

            canvas.create_oval(y * 100 + offset, x * 100 + offset, y * 100 + 100 - offset, x * 100 + 100 - offset,
                               fill="yellow", outline="yellow")

            print(check_game_state(is_draw_enable=True))

            break


turn: bool = False


def minimax(alpha=-1_000_000, beta=1_000_000, maximizing_player=True) -> int:
    game_state = check_game_state()

    if game_state != 4:
        return game_state

    prune: bool = False

    if maximizing_player:  # X turn
        max_score = -1_000_000
        for i in range(5):
            for j in range(5, -1, -1):
                if board[i][j] == ' ' and not prune:
                    board[i][j] = 'x'
                    score = minimax(alpha, beta, False)
                    board[i][j] = ' '
                    max_score = max(score, max_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        prune = True
                    break
        return max_score

    else:  # O turn
        min_score = 1_000_000
        for i in range(5):
            for j in range(5, -1, -1):
                if board[i][j] == ' ' and not prune:
                    board[i][j] = 'o'
                    score = minimax(alpha, beta, True)
                    board[i][j] = ' '
                    min_score = min(score, min_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        prune = True
                    break
        return min_score


def draw_by_turn(event):
    global turn, is_game_ended

    if not is_game_ended:
        if not turn:
            draw_yellow(event)
            turn = True
            return

        score = 0
        best_move = (-1, -1)
        best_score = 1_000_000
        for i in range(5):
            for j in range(5, -1, -1):
                if board[i][j] == ' ':
                    board[i][j] = 'r'
                    score = minimax()
                    board[i][j] = ' '
                    if best_score > score:
                        best_score = score
                        best_move = (i, j)
                    break

        draw_red(best_move[0], best_move[1])
        turn = False


window = Tk()

canvas = Canvas(window, width=600, height=500)
canvas.place(x=0, y=0)
canvas.config(bg="#6d81b0")

for ii in range(1, 7):
    canvas.create_line(ii * 100, 0, ii * 100, 500, fill="white", width=3)

window.bind('<Button-1>', draw_by_turn)

window.title('Tic Tac Toe')
window.geometry("600x500")
window.resizable(False, False)
window.mainloop()
