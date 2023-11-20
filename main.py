import time
from tkinter import *
import numpy as np

squares = np.empty(shape=(3, 3), dtype=str)
squares.fill(' ')

turn: bool = False
is_game_ended: bool = False


def draw_win(row=-1, col=-1, diag1=-1, diag2=-1, is_draw_enable2: bool = False):
    if is_draw_enable2:
        global is_game_ended
        offset = 10

        if row != -1 or col != -1 or diag1 != -1 or diag2 != -1:
            is_game_ended = True

        if row != -1:
            canvas.create_line(offset, row * 100 + 50, 300 - offset, row * 100 + 50, fill="#ff5c5c", width=3)

        if col != -1:
            canvas.create_line(col * 100 + 50, offset, col * 100 + 50, 300 - offset, fill="#ff5c5c", width=3)

        if diag1 != -1:
            canvas.create_line(offset, offset, 300 - offset, 300 - offset, fill="#ff5c5c", width=3)

        if diag2 != -1:
            canvas.create_line(300 - offset, offset, offset, 300 - offset, fill="#ff5c5c", width=3)


def get_game_state(is_draw_enable: bool = False) -> int:  # X wins: -1, O wins: 1, Tie: 0, Game not finished: 4
    for i in range(3):
        if squares[i][0] == squares[i][1] == squares[i][2]:
            if squares[i][0] == 'x':
                draw_win(row=i, is_draw_enable2=is_draw_enable)
                return 1
            if squares[i][0] == 'o':
                draw_win(row=i, is_draw_enable2=is_draw_enable)
                return -1

    for j in range(3):
        if squares[0][j] == squares[1][j] == squares[2][j]:
            if squares[0][j] == 'x':
                draw_win(col=j, is_draw_enable2=is_draw_enable)
                return 1
            if squares[0][j] == 'o':
                draw_win(col=j, is_draw_enable2=is_draw_enable)
                return -1

    if squares[0][0] == squares[1][1] == squares[2][2]:
        if squares[0][0] == 'x':
            draw_win(diag1=0, is_draw_enable2=is_draw_enable)
            return 1
        if squares[0][0] == 'o':
            draw_win(diag1=0, is_draw_enable2=is_draw_enable)
            return -1

    if squares[0][2] == squares[1][1] == squares[2][0]:
        if squares[0][2] == 'x':
            draw_win(diag2=0, is_draw_enable2=is_draw_enable)
            return 1
        if squares[0][2] == 'o':
            draw_win(diag2=0, is_draw_enable2=is_draw_enable)
            return -1

    for i in range(3):
        for j in range(3):
            if squares[i][j] == ' ':
                return 4

    return 0


def minimax(alpha=-1_000_000, beta=1_000_000, maximizing_player=True) -> int:
    game_state = get_game_state()
    if game_state != 4:
        return game_state

    prune: bool = False

    if maximizing_player:  # X turn
        max_score = -1_000_000
        for i in range(3):
            for j in range(3):
                if squares[i][j] == ' ' and not prune:
                    squares[i][j] = 'x'
                    score = minimax(alpha, beta, False)
                    squares[i][j] = ' '
                    max_score = max(score, max_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        prune = True
        return max_score

    else:  # O turn
        min_score = 1_000_000
        for i in range(3):
            for j in range(3):
                if squares[i][j] == ' ' and not prune:
                    squares[i][j] = 'o'
                    score = minimax(alpha, beta, True)
                    squares[i][j] = ' '
                    min_score = min(score, min_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        prune = True
        return min_score


def draw_x(event):
    global turn
    offset = 20
    x, y = int(event.x / 100), int(event.y / 100)

    if squares[y][x] == ' ':
        squares[y][x] = 'x'

        canvas.create_line(x * 100 + offset, y * 100 + offset, x * 100 + 100 - offset, y * 100 + 100 - offset,
                           fill="yellow", width=5)
        canvas.create_line(x * 100 + offset, y * 100 + 100 - offset, x * 100 + 100 - offset, y * 100 + offset,
                           fill="yellow", width=5)

        get_game_state(True)

        turn = True
        draw_by_turn(event)


def draw_o(x, y):
    global squares
    offset = 20

    squares[x][y] = 'o'

    canvas.create_oval(y * 100 + offset, x * 100 + offset, y * 100 + 100 - offset, x * 100 + 100 - offset,
                       outline="#dc96ff", width=5)

    get_game_state(True)


def draw_by_turn(event):
    global is_game_ended

    if not is_game_ended:
        global turn

        if turn:  # O turn
            best_score = 1_000_000
            turn = False
            best_move = None

            for i in range(3):
                for j in range(3):
                    if squares[i][j] == ' ':
                        squares[i][j] = 'o'
                        score = minimax()
                        squares[i][j] = ' '
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)

            if best_move:
                draw_o(best_move[0], best_move[1])

            return

        # X turn
        draw_x(event)


window = Tk()

canvas = Canvas(window, width=300, height=300)
canvas.place(x=0, y=0)

canvas.config(bg="#6d81b0")
canvas.create_line(100, 0, 100, 300, fill="white", width=3)
canvas.create_line(200, 0, 200, 300, fill="white", width=3)
canvas.create_line(0, 100, 300, 100, fill="white", width=3)
canvas.create_line(0, 200, 300, 200, fill="white", width=3)

window.bind('<Button 1>', draw_by_turn)

window.title('Tic Tac Toe')
window.geometry("300x300")
window.resizable(False, False)
window.mainloop()
