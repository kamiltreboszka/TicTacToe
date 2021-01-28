# Gra TicTacToe

import pygame
import sys
import numpy as np

pygame.init()

winner = None
draw = None

# ROZMIAR GRY
WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = WIDTH//BOARD_COLUMNS
CIRCLE_RADIUS = SQUARE_SIZE//2 - SQUARE_SIZE//6
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE//4

# RGB COLORS
BG_COLOR = (28, 178, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
pygame.display.set_caption('Tic-Tac-Toe')
screen.fill(BG_COLOR)

# TABLICA GRY
board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))


# RYSOWANIE PLANSZY GRY
def draw_lines():
    # 1 LINIA POZIOMA
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    # 2 LINIA POZIOMA
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # 3 LINIA POZIOMA
    pygame.draw.line(screen, LINE_COLOR, (0, 3 * SQUARE_SIZE), (WIDTH, 3 * SQUARE_SIZE), LINE_WIDTH)

    # 1 LINIA PIONOWA
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 2 LINIA PIONOWA
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


# RYSOWANIE FIGUR
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE//2), int(row * SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)


# ZAZNACZENIE KWADRATU NA PLANSZY
def mark_square(row, col, player):
    board[row][col] = player


# DOSTEPNE KWADRATY NA PLANSZY
def available_square(row, col):
    return board[row][col] == 0


# SPRAWDZENIE CZY PLANSZA JEST PEŁNA
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                return False

    return True


# SPRAWDZENIE STATUSU GRY
def draw_status():
    reset_message = ""
    global draw
    if winner is None:
        if player == 2:
            message = "X's Turn"
        elif player == 1:
            message = "O's Turn"
    else:
        if player == 1:
            message = "X's WON "
            reset_message = "Press R to reset game"
        elif player == 2:
            message = "O's WON "
            reset_message = "Press R to reset game"

    if draw:
        message = "Game DRAW!"
        reset_message = "Press R to reset game"

    font = pygame.font.Font(None, 30)
    text = font.render(message, 1, (66, 66, 66))
    r_text = font.render(reset_message, 1, (66, 66, 66))
    screen.fill((23, 145, 135), (0, 600, 600, 100))
    text_rect = text.get_rect(center=(WIDTH / 2, 700 - 50))
    text_rect1 = r_text.get_rect(center=(WIDTH / 2, 700 - 20))
    screen.blit(text, text_rect)
    screen.blit(r_text, text_rect1)
    pygame.display.update()


# SPRAWDZENIE CZY KTOŚ WYGRAŁ
def check_win(player):
    global winner, draw
    #sprwdzenie pionowego zwyciestwa
    for col in range(BOARD_COLUMNS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            winner = player
            return True

    #sprawdzenie poziomego zwyciestwa
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            winner = player
            return True

    #sprawdzenie zwyciestwa ukośnego rosnacego
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        winner = player
        return True

    #sprawdzenie zwyciestwa ukosnego malejacego
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        winner = player
        return True

    if (all([all(row) for row in board]) and winner is None):
        draw = True

    draw_status()
    return False


# RYSOWANIE LINI ZWYCIEZCY
def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE//2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)


# RYSOWANIE LINI ZWYCIEZCY
def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE//2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)


# RYSOWANIE UKOŚNEJ LINI ZWYCIEZCY (ROSNĄCEJ)
def draw_asc_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, HEIGHT-15), (WIDTH-15, 15), 15)


# RYSOWANIE UKOŚNEJ LINI ZWYCIEZCY (MALEJĄCEJ)
def draw_desc_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)


# RESTART GRY
def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    player = 2
    global draw, winner
    draw = None
    winner = None
    message = " "
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            board[row][col] = 0


draw_lines()

player = 2
game_over = False

# MAINLOOP
while True:
    draw_status()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            print(clicked_row)
            print(clicked_col)

            if available_square( clicked_row, clicked_col):
                mark_square( clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False

    pygame.display.update()