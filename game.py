import numpy as np
import pygame, sys, math
import tkinter as tk
from tkinter import messagebox

BOARD_ROWS = 6
BOARD_COLS = 7
GAME_OVER = False
turn = 0

PLAYERS = {
    1: "RED",
    2: "YELLOW"
}

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = BOARD_COLS * SQUARESIZE
HEIGHT = (BOARD_ROWS + 1) * SQUARESIZE

SIZE = (WIDTH, HEIGHT)

#COLORS
BLUE = (3, 42, 100)
RED = (228, 60, 60)
GREEN = (0, 255, 0)
YELLOW = (232, 176, 27)
BLACK = (30, 30, 30)
WHITE = (0, 0, 0)

def create_board():
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    return board

def drop_in_player(board, row, col, player):
    board[row, col] = player
    draw_board(board)
    pygame.display.update()

def is_valid_location(board, col):
    if col > -1 and col < 7: 
        return board[0, col] == 0
    else: 
        return False

def get_next_empty_row(board, col):
    for row in range(BOARD_ROWS):
        if board[BOARD_ROWS -1 - row, col] == 0:
            return BOARD_ROWS -1 - row

def check_win(board, row, col, player):
    #check Vertical
    win = 0
    for i in range(BOARD_COLS):
        if board[row, i] == player:
            win += 1
            if win >= 4:
                return True
        else:
            win = 0
    #check Horizontal
    if (BOARD_ROWS - row) > 3:
        for j in range(BOARD_ROWS):
            if board[BOARD_ROWS - 1 - j, col] == player:
                win += 1
                if win >= 4:
                    return True 
            else:
                win = 0
    
    # Check positively sloped diaganols
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

	# Check negatively sloped diaganols
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

    return False

def calc_block(c, r):
    return (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE)

def calc_circle(c, r):
    return (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2))

def draw_board(board):
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS):
            pygame.draw.rect(screen, BLUE, calc_block(c, r))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, calc_circle(c, r), RADIUS)
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, calc_circle(c, r), RADIUS)
            if board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, calc_circle(c, r), RADIUS)
    pygame.display.update()

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def reset():
    global board
    board = create_board()
    turn = 0
    draw_board(board)

board = create_board()
print(board)

pygame.init()
screen = pygame.display.set_mode(SIZE)

draw_board(board)

pygame.display.set_caption("Connect 4 Game by TheRiolDeal")
message_box("WELCOME", "Welcome to my game! \nClick Ok to Play \nHit R to restart whenever you want. \nEnjoy!:D")

clock = pygame.time.Clock()
# pick a font you have and set its size
myfont = pygame.font.SysFont("Comic Sans MS", 30)
# apply it to text on a label
label = myfont.render("COLUMN FULL!", 1, (255, 255, 255))

while not GAME_OVER:
    clock.tick(50)
    player = (turn % 2) + 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_r]:
                reset()

        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            if player == 1:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            selection = int(math.floor(posx / SQUARESIZE))
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            if player == 2:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            draw_board(board)

            if is_valid_location(board, selection):
                row = get_next_empty_row(board, selection)
                drop_in_player(board, row, selection, player)

                if check_win(board, row, selection, player):
                    pygame.time.wait(300)
                    message_box('GAME OVER', f'{PLAYERS[player]} Player won!!')
                    print(f"Player {player} won!!")
                    reset()
                turn += 1
            else:
                screen.blit(label, (0, 0))
                print("Column FULL!  Select another column!")
            print(board)
            draw_board(board)
            pygame.display.update()
            
