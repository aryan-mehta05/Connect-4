import numpy as np
import random
import pygame
import sys
import math
from pygame import mixer

mainClock = pygame.time.Clock()

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
CYAN = (91, 222, 248)
LIGHT_GREY = (122, 122, 122)
DARK_GREY = (40, 40, 40)
PINK = (255, 105, 180)
NAVY_BLUE = (0, 0, 77)
TOM_BLUE = (102, 153, 204)
JERRY_BROWN = (194, 127, 48)
LIGHT_GREEN = (122, 235, 122)
LIGHT_RED = (255, 210, 210)
LIGHT_YELLOW = (255, 255, 200)
GREEN = (0, 150, 0)
PURPLE = (180, 0, 180)

p1_tray = [RED, WHITE, PINK, TOM_BLUE, CYAN, WHITE, YELLOW, WHITE]
ai_tray = [YELLOW, LIGHT_GREY, WHITE, JERRY_BROWN, BLUE, PINK, LIGHT_YELLOW, LIGHT_GREEN]
board_tray = [BLUE, DARK_GREY, NAVY_BLUE, LIGHT_GREY, NAVY_BLUE, RED, WHITE, GREEN]
theme_tray = ["   Default   ", "  Mono-tone  ", "Pink Panther", "Tom and Jerry", "  Bluescale  ", " Red - scale ", " Yellowscale ", " Green-scale "]

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals for win
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1: # Replace with PLAYER_PIECE
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2: # Replace with AI_PIECE
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def animate_move(board, row, col, piece):
    xposition = int(col*SQUARESIZE + SQUARESIZE/2)
    yposition = int(SQUARESIZE/2)
    colour = RED
    if piece == 2:
        colour = YELLOW
    yspeed = 1
    while yposition < (height-row*SQUARESIZE-SQUARESIZE/2):
        yspeed += .05
        yposition += yspeed
        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
        draw_board(board)
        pygame.draw.circle(screen, colour, (xposition, int(yposition)), RADIUS)
        pygame.display.update()

    return True


def tie_game(board):
    count = 0
    for c in range(COLUMN_COUNT):
        if board[ROW_COUNT-1][c] == 0:
            count += 1
    if count < 1:
        return True
    else:
        return False


def fade(width, height, colour, speed):
    fade = pygame.Surface((width, height))
    fade.fill(colour)
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(speed)


def player_1_plays():
    posx = event.pos[0]
    col = int(math.floor(posx / SQUARESIZE))

    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        piece_1_sound = mixer.Sound('Coins_falling.wav')
        piece_1_sound.play()
        animate_move(board, row, col, 1)
        drop_piece(board, row, col, 1)

        if winning_move(board, 1):
            win_message = win_font.render("Player 1 wins!", 1, RED)
            screen.blit(win_message, (40, 10))
            return True


def player_2_plays():
    posx = event.pos[0]
    col = int(math.floor(posx / SQUARESIZE))

    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        piece_2_sound = mixer.Sound('Coins_falling.wav')
        piece_2_sound.play()
        animate_move(board, row, col, 2)
        drop_piece(board, row, col, 2)

        if winning_move(board, 2):
            win_message = win_font.render("Player 2 wins!", 1, YELLOW)
            screen.blit(win_message, (40, 10))
            return True


def condition_game_over(width, height):
    applause = mixer.Sound('Applause.wav')
    applause.play()
    pygame.time.wait(4000)
    # mixer.music.load('Outro.mp3')
    # mixer.music.play()
    # mixer.music.load('Cradles_outro.mp3')
    # mixer.music.play()
    fade(width, height, WHITE, 5)
    thank_you_text = thank_you_font_1.render("Thank you", 1, BLACK, LIGHT_RED)
    message = thank_you_font_2.render("for playing!", 1, BLACK, LIGHT_RED)
    screen.blit(thank_you_text, (122, 200))
    screen.blit(message, (30, 300))
    pygame.display.update()
    pygame.time.wait(5000)
    fade(width, height, LIGHT_RED, 5)
    pygame.draw.rect(screen, BLACK, (100, 232, rect_width, rect_height), 3)
    pygame.draw.rect(screen, BLACK, (100, 332, rect_width, rect_height), 3)
    pygame.draw.rect(screen, BLACK, (100, 432, rect_width, rect_height), 3)
    pygame.draw.rect(screen, BLACK, (100, 532, rect_width, rect_height), 3)
    pygame.draw.rect(screen, CYAN, (105, 237, small_rect_width, small_rect_height), 0)
    pygame.draw.rect(screen, CYAN, (105, 337, small_rect_width, small_rect_height), 0)
    pygame.draw.rect(screen, CYAN, (105, 437, small_rect_width, small_rect_height), 0)
    pygame.draw.rect(screen, CYAN, (105, 537, small_rect_width, small_rect_height), 0)
    dsa_display = final_font.render("Data Structures and Algorithms", 1, BLACK)
    j_comp_project = j_comp.render("J - Component (Project)", 1, RED, WHITE)
    name = final_text_font.render("Name: Aryan Mehta", 1, WHITE)
    reg_no = final_text_font.render("Reg No: 19BCE0536", 1, WHITE)
    slot = final_text_font.render("Slot: B2 / TB2", 1, WHITE)
    faculty = sendhil_font.render("Faculty: K. S. Sendhil Kumar", 1, WHITE)
    screen.blit(dsa_display, (22, 65))
    screen.blit(j_comp_project, (145, 115))
    screen.blit(name, (140, 240))
    screen.blit(reg_no, (135, 340))
    screen.blit(slot, (205, 440))
    screen.blit(faculty, (125, 550))
    pygame.display.update()
    pygame.time.wait(12000)
    fade(width, height, WHITE, 6)


def welcome_screen(fade_time, delay):
    mixer.music.load('intro_kina.mp3')
    mixer.music.play()
    # mixer.music.load('Cradles_intro.mp3')
    # mixer.music.play()
    fade(width, height, LIGHT_RED, fade_time)
    greeting_1 = welcome_text_1.render("Welcome to", 1, BLACK, WHITE)
    greeting_2 = welcome_text_2.render("CONNECT 4", 1, BLACK, WHITE)
    version = player_vs_ai.render("(2 Player version)", 1, WHITE, NAVY_BLUE)
    screen.blit(greeting_1, (135, 140))
    screen.blit(greeting_2, (10, 260))
    screen.blit(version, (60, 430))
    pygame.display.update()
    pygame.time.wait(delay)
    fade(width, height, BLACK, 1)


def info_page(fade_time, delay):
    fade(width, height, BLACK, fade_time)
    subtitle_1 = subtitle_1_font.render("Program designed by:", 1, PINK)
    subtitle_2 = subtitle_2_font.render("Aryan Nimesh Mehta", 1, WHITE, NAVY_BLUE)
    subtitle_3 = subtitle_3_font.render("Reg No: 19BCE0536", 1, WHITE, NAVY_BLUE)
    screen.blit(subtitle_1, (210, 260))
    screen.blit(subtitle_2, (30, 300))
    screen.blit(subtitle_3, (70, 375))
    pygame.display.update()
    pygame.time.wait(delay)
    fade(width, height, WHITE, fade_time)


def lets_play(fade_time, delay):
    fade(width, height, LIGHT_RED, 1)
    display_lets_play = lets_play_font.render(" Let's Play! ", 1, BLACK, WHITE)
    selected_theme =  final_text_font.render("Selected theme:", 1, WHITE, DARK_GREY)
    theme = theme_font.render(TEXT, 1, PURPLE)
    pygame.draw.circle(screen, PLAYER_COLOUR, (int(2 * SQUARESIZE + SQUARESIZE/2), int(5 * SQUARESIZE)), RADIUS)
    pygame.draw.circle(screen, AI_COLOUR, (int(3 * SQUARESIZE + SQUARESIZE / 2), int(5 * SQUARESIZE)), RADIUS)
    pygame.draw.circle(screen, BOARD_COLOUR, (int(4 * SQUARESIZE + SQUARESIZE / 2), int(5 * SQUARESIZE)), RADIUS)
    screen.blit(display_lets_play, (95, 100))
    screen.blit(selected_theme, (178, 380))
    screen.blit(theme, (init_x, 560))
    pygame.display.update()
    pygame.time.delay(delay)
    fade(width, height, WHITE, fade_time)


colour_selector = random.randint(0, 7)
PLAYER_COLOUR = p1_tray[colour_selector]
AI_COLOUR = ai_tray[colour_selector]
BOARD_COLOUR = board_tray[colour_selector]
TEXT = theme_tray[colour_selector]

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

small_rect_width = (5 * SQUARESIZE) - 10
small_rect_height = SQUARESIZE - 34
rect_width = 5 * SQUARESIZE
rect_height = SQUARESIZE - 24
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

init_x = int(width/2 - ((len(TEXT)/2) * 45) + 115)

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

win_font = pygame.font.SysFont("monospace", 75)
player_prompt_font = pygame.font.SysFont("cambria", 24)
lets_play_font = thank_you_font_1 = pygame.font.SysFont("monotypecorsiva", 120)
thank_you_font_2 = pygame.font.SysFont("broadway", 105)
welcome_text_1 = pygame.font.SysFont("monotypecorsiva", 100)
welcome_text_2 = pygame.font.SysFont("broadway", 115)
player_vs_ai = pygame.font.SysFont("bauhaus93", 75)
subtitle_1_font = pygame.font.SysFont("monotypecorsiva", 36)
subtitle_2_font = pygame.font.SysFont("broadway", 55)
subtitle_3_font = pygame.font.SysFont("broadway", 55)
final_font = pygame.font.SysFont("broadway", 38)
j_comp = pygame.font.SysFont("monotypecorsiva", 50)
final_text_font = pygame.font.SysFont("bauhaus93", 48)
sendhil_font = pygame.font.SysFont("bauhaus93", 36)
theme_font = pygame.font.SysFont("monospace", 45)

screen = pygame.display.set_mode(size)
welcome_screen(10, 5000)
info_page(5, 5000)
lets_play(5, 5000)
draw_board(board)
pygame.display.update()

# mixer.music.load('Background.mp3')
# mixer.music.play(-1)

mixer.music.load('game_kina.mp3')
mixer.music.play(-1)

# 2 Player version of the game
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                label = player_prompt_font.render("Player 1's Turn:", 1, WHITE)
                screen.blit(label, (5, 5))
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                label = player_prompt_font.render("Player 2's Turn:", 1, WHITE)
                screen.blit(label, (5, 5))
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            # Ask for Player 1 Input
            if turn == 0:
                game_over = player_1_plays()

            # Ask for Player 2 Input
            else:
                game_over = player_2_plays()

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if tie_game(board):
                label = win_font.render("It is a tie!", 1, WHITE)
                screen.blit(label, (75, 10))
                pygame.display.update()
                game_over = True

            if game_over:
                condition_game_over(width, height)
