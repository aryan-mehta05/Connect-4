# ---------------------------------------------------------------------------------------------------------------------
#                                    -----|>     Name: ARYAN NIMESH MEHTA
#                                    -----|>     Reg No: 19BCE0536
#                                    -----|>     Slot: B2 / TB2
#                                    -----|>     Faculty: K. S. Sendhil Kumar
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
#                                                DATE AND TIME OF PRODUCTION:

#     Day 1: 22/05/2020
#         Sitting 1: (10:00 - 14:30) - Developed the command line version of the 2 player game
#         Sitting 2: (16:00 - 18:00) - Debugged the command line version code and modularized it

#     Day 2: 23/05/2020
#         Sitting 1: (01:00 - 10:30) - Implemented the AI program for the game
#         Sitting 2: (16:00 - 20:30) - Made the AI more efficient by implementing algorithms

#     Day 3: 24/05/2020
#         Sitting 1: (00:30 - 03:30) - Implemented graphics for the main game loop
#         Sitting 2: (11:30 - 14:30) - Implemented the pre-game graphics for introductory screens
#         Sitting 3: (17:00 - 20:00) - Implemented the post game graphics for terminating screens
#         Sitting 4: (23:00 - 23:59) - Added sound for the game and started final debugging

#     Day 4: 25/05/2020
#         Sitting 1: (00:00 - 03:00) - Finished with final debugging and program modularization
#         Sitting 2: (14:00 - 17:00) - Finished commenting and finalized preparation for program export
# ---------------------------------------------------------------------------------------------------------------------


# Libraries to be imported for running this project
import numpy as np
import random
import pygame
import sys
import math
from pygame import mixer

mainClock = pygame.time.Clock()

# Colour palette: All the colours used in the game
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

# Manually sorting out the colours in a theme pattern such that:
# The p1_tray corresponds to the colour of the player 1 piece
# The ai_tray corresponds to the colour of the AI piece
# The board_tray corresponds to the colour of the board
# The theme_tray corresponds to the name of the theme
#
# So, if index 0 is chosen for the following lists, the the selected theme is "default", as named in the theme_tray,
# and the colours will be:
#     player = RED (p1_tray[0])
#     AI = YELLOW (ai_tray[0])
#     board = BLUE (board_tray[0])
#
# if index is, for example 4, then the selected theme is "Bluescale" and the colours are:
#     player = CYAN (p1_tray[4])
#     AI = BLUE (ai_tray[4])
#     board = NAVY_BLUE (board_tray[4])
p1_tray = [RED, WHITE, PINK, TOM_BLUE, CYAN, WHITE, YELLOW, WHITE]
ai_tray = [YELLOW, LIGHT_GREY, WHITE, JERRY_BROWN, BLUE, PINK, LIGHT_YELLOW, LIGHT_GREEN]
board_tray = [BLUE, DARK_GREY, NAVY_BLUE, LIGHT_GREY, NAVY_BLUE, RED, WHITE, GREEN]
theme_tray = ["   Default   ", "  Mono-tone  ", "Pink Panther", "Tom and Jerry", "  Bluescale  ", " Red - scale ",
              " Yellowscale ", " Green-scale "]

DIFFICULTY_LEVEL = 1  # Corresponds to the depth at which the tree is searched, (height of the tree)

ROW_COUNT = 6  # Fixed (default) row count on a Connect 4 board (no. of rows)
COLUMN_COUNT = 7  # Fixed (default) column count on a Connect 4 board (no. of columns)

PLAYER = 0  # Value assigned to player, to determine the turn
AI = 1  # Value assigned to AI, to determine the turn

PLAYER_PIECE = 1  # The piece value of player
AI_PIECE = 2  # The piece value of AI

# Length of minimum combination required to win a board. (Comment on WINDOW_LENGTH)
# We have to connect '4' pieces in a row, column or diagonal to win, hence 4. (Comment on WINDOW_LENGTH)
WINDOW_LENGTH = 4
EMPTY = 0  # Variable to check if corresponding place on board is empty or not (Hence, piece value if EMPTY)


# Function to create and return a board where all positions are initialized to 0, since they're all empty at the start.
# Created using the numpy function np.zeros
def create_board():  # frame = board
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# If a piece is dropped at a particular position, then that position becomes the piece
# This function implements that logic
def drop_piece(board, row, col, piece):  # frame = board
    board[row][col] = piece


# This function checks whether the desired position to drop a piece in is valid or not
def is_valid_location(board, col):  # frame = board
    return board[ROW_COUNT-1][col] == 0


# Once a piece is dropped, its position (or piece) value becomes 1 (if player) or 2 (if AI)
# and that row becomes occupied in that specific column
# Hence, getting the next available row in that column to drop a piece becomes the key factor
# This function helps to determine that. It returns the row in that column if it is EMPTY
def get_next_open_row(board, col):  # frame = board
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# Prints the board on the console
def print_board(board):  # frame = board
    print(np.flip(board, 0))


# This function checks for all the winning combinations of 4 possible after every move.
# If such a pattern (sequence) is True, this function returns the status and the piece value of the winning piece.
def winning_move(board, piece):  # frame = board
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
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == \
                    piece:
                return True

    # Check negatively sloped diagonals for win
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == \
                    piece:
                return True


# Function exclusive for AI: Does the math for the score_position function
# This function evaluates the window and checks for the best moves possible.
# This is achieved by assigning a score to every possible combination that may help the AI win
# This should be done such that, the preference falls to the position that returns the maximum score.
# For example, there are 7 playable positions for the AI, this function evaluates the move that returns the max score.
# This score then passes to the score_position function which works on making that move occur by the AI.
# This function uses the greedy algorithm to assign the highest score to the best move
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:  # If there's a possibility of a 4 piece combination
        score += 100  # The maximum score is awarded to the AI, hence this is the move of greatest preference.
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:  # Possibility of a 3 piece combination
        score += 5  # It gets the second-most priority (5 Points)
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:  # Possibility of a 2 piece combination
        score += 2  # Gets the fourth-most priority (2 Points)

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:  # Opponent getting a 3 piece combination
        score -= 4  # Gets the third most priority.
    # This move gets a higher priority than a 2 piece combination because it is important for the AI to prioritize
    # blocking the opponent's 3 piece combination, because if it won't, the player will win in th next move
    # Hence, a smart AI should be able to block the opponent's winning combinations as well.

    return score


# Function exclusive for AI: Provides the score for every move playable in AI's next chance
# This function gets all the possible moves that the AI can play next
# It uses the evaluate_window function to compare and see which one of the moves gets assigned the maximum score
# This move is the selected by the pick_best_move function after passing on the score from here
def score_position(board, piece):
    score = 0

    # Score centre column: Making centre column moves will give the AI more possible combinations to win
    centre_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    centre_count = centre_array.count(piece)
    score += centre_count * 3

    # Score Horizontal: Checks for horizontal combinations to see if it is the best move
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical: Checks for vertical combinations to see if it is the best move
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonals: Checks for positive diagonal combinations to see if it is the best move
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonals: Checks for negative diagonal combinations to see if it is the best move
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


# Function exclusive for AI: Checks if the next move is the last move of the game
# There are 3 possibilities where the next move may be the last move of the game, i.e. if:
#     (i)   Player wins and AI loses
#     (ii)  AI wins and Player loses
#     (iii) It is the last empty position to play in and the game is a tie
# This function only returns a boolean True if either of these conditions is True for is_terminal_node
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# Function exclusive for AI: Implements the "MINIMAX ALGORITHM" and "ALPHA-BETA PRUNING ALGORITHM"

# The Alpha Beta pruning makes the minimax algorithm more efficient and effective
# It helps reduce the unnecessary moves (branches) in the tree and hence reduces the number of iterative moves the...
# AI has to check, hence reducing its thinking time (i.e. time taken to traverse through the entire tree)
# It can also be said as the time taken to decide and make the best move

# The minimax algorithm is called so because the AI could either be the 'MINI'mizing or the 'MAX'imizing player.
# It is a recursive function that keeps on repeating the same number of times as the depth
# i.e. if the depth = 4, the minimax iterates up to a height of 4 in the tree and checks 4 levels deep
# and with each iteration, the status of the AI changes from maximizing to minimizing
# so that it can check both conditions equally
# With that, it returns the best playable column and the score (value)
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):  # If AI wins, it receives a huge positive value (score)
                return None, 100000000000000000000  # <-- It receives this score
            elif winning_move(board, PLAYER_PIECE):  # If AI loses, it receives a huge negative value (score)
                return None, -100000000000000000000  # <-- It receives this score
            else:  # Game is over, no more valid moves, hence no change in score
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, AI_PIECE)  # Only returns that score

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Minimizing Player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


# Function exclusive for AI: Returns a list of valid playable positions
# This function checks if a location on the board is valid using the is_valid_location function for every column
# If it is valid, it appends the column number of the valid location in the valid_locations list
# It passes this list to the pick_best_move function when called so that picking the best move can be facilitated
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


# Function exclusive for AI: Picks the move with the maximum score for the AI
# get_valid_locations, get_next_open_row, drop_piece and score_position functions are used in this function
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)  # ALl the valid locations (columns) are provided
    best_score = -10000
    best_col = random.choice(valid_locations)  # The provided columns are chosen from at random
    for col in valid_locations:
        row = get_next_open_row(board, col)  # The open row for that column is found
        temp_board = board.copy()  # Board is copied so that no alterations to the actual board are made
        drop_piece(temp_board, row, col, piece)  # A piece is dropped there temporarily. The player won't see this.
        # It is like mental maths for the AI. It plays these moves mentally to see which of those moves is the best.
        score = score_position(temp_board, piece)  # Score for that move is temporarily assigned
        if score > best_score:  # Comparison occurs for the best move to be found and then the best column is returned.
            best_score = score
            best_col = col

    return best_col


# Board graphics drawn using this function
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BOARD_COLOUR, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2),
                                               int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, PLAYER_COLOUR, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                           height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, AI_COLOUR, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                       height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


# Animation for the dropping piece is provided by this function
def animate_move(board, row, col, piece):
    x_position = int(col*SQUARESIZE + SQUARESIZE/2)
    yposition = int(SQUARESIZE/2)
    colour = PLAYER_COLOUR
    if piece == 2:
        colour = AI_COLOUR
    y_speed = 1
    while yposition < (height-row*SQUARESIZE-SQUARESIZE/2):
        y_speed += .05
        yposition += y_speed
        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
        draw_board(board)
        pygame.draw.circle(screen, colour, (x_position, int(yposition)), RADIUS)
        pygame.display.update()

    return True


# Checking if the game is a tie.
# It can only be a tie when all the locations on the board have been filled, and the last move wasn't the winning move.
# The simplest way to check this condition is if at least one of the columns is empty in the topmost row (6th)
# If any of those spots is empty, then it's yet not a tie. Hence, False is returned in this case.
# If all the spots are filled, then it's a tie. Hence, True is returned.
def tie_game(board):
    count = 0
    for c in range(COLUMN_COUNT):
        if board[ROW_COUNT-1][c] == 0:
            count += 1
    if count < 1:
        return True
    else:
        return False


# The fading transition effect form one frame to other is added using this function
def fade(wide, high, colour, speed):  # wide = width, high = height
    fading = pygame.Surface((wide, high))
    fading.fill(colour)
    for alpha in range(0, 300):
        fading.set_alpha(alpha)
        screen.blit(fading, (0, 0))
        pygame.display.update()
        pygame.time.delay(speed)


# The main playing function of the AI in the main game loop
def ai_plays(board):
    ai_prompt = player_prompt_font.render("AI's Turn:", 1, AI_COLOUR)
    screen.blit(ai_prompt, (5, 5))
    pygame.display.update()
    col, minimax_score = minimax(board, DIFFICULTY_LEVEL, -math.inf, math.inf, True)

    if is_valid_location(board, col):
        pygame.time.wait(500)
        row = get_next_open_row(board, col)
        piece_2_sound = mixer.Sound('Coins_falling.wav')
        piece_2_sound.play()
        animate_move(board, row, col, AI_PIECE)
        drop_piece(board, row, col, AI_PIECE)

        if winning_move(board, AI_PIECE):
            you_lose = win_font.render("You lose!", 1, AI_COLOUR)
            screen.blit(you_lose, (170, 10))
            return True


# The main playing function of the player in the main game loop
def player_plays(board):
    position_x = event.pos[0]
    col = int(math.floor(position_x / SQUARESIZE))

    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        piece_1_sound = mixer.Sound('Coins_falling.wav')
        piece_1_sound.play()
        animate_move(board, row, col, PLAYER_PIECE)
        drop_piece(board, row, col, PLAYER_PIECE)

        if winning_move(board, PLAYER_PIECE):
            you_win = win_font.render("You win!", 1, PLAYER_COLOUR)
            screen.blit(you_win, (178, 10))
            return True


# The game over condition:
# For whatever reasons, if the game is over the final exit screens with the exit soundtrack are played.
def condition_game_over():
    applause = mixer.Sound('Applause.wav')
    applause.play()
    pygame.time.wait(4000)
    mixer.music.load('Exit.mp3')
    mixer.music.play()
    # mixer.music.load('Cradles_exit.mp3')
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


# The first welcome screen when the game begins is displayed using this function
def welcome_screen(fade_time, delay):
    mixer.music.load('intro_kina.mp3')
    mixer.music.play()
    # mixer.music.load('Cradles_intro.mp3')
    # mixer.music.play()
    fade(width, height, LIGHT_RED, fade_time)
    greeting_1 = welcome_text_1.render("Welcome to", 1, BLACK, WHITE)
    greeting_2 = welcome_text_2.render("CONNECT 4", 1, BLACK, WHITE)
    version = player_vs_ai.render("(Player v/s AI)", 1, WHITE, NAVY_BLUE)
    screen.blit(greeting_1, (135, 140))
    screen.blit(greeting_2, (10, 260))
    screen.blit(version, (120, 430))
    pygame.display.update()
    pygame.time.wait(delay)
    fade(width, height, BLACK, 1)


# The second info screen when the game begins is displayed using this function
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


# The third let's play screen when the game begins is displayed using this function
def lets_play(fade_time, delay):
    fade(width, height, LIGHT_RED, 1)
    display_lets_play = lets_play_font.render(" Let's Play! ", 1, BLACK, WHITE)
    selected_theme = final_text_font.render("Selected theme:", 1, WHITE, DARK_GREY)
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


# The 8 themes are selected from randomly using the random.randint method
colour_selector = random.randint(0, 7)
PLAYER_COLOUR = p1_tray[colour_selector]  # Player's colour assigned throughout that game using this random integer
AI_COLOUR = ai_tray[colour_selector]  # AI's colour assigned throughout that game using this random integer
BOARD_COLOUR = board_tray[colour_selector]  # Board's colour assigned throughout that game using this random integer
TEXT = theme_tray[colour_selector]  # Name of the theme picked for that game using this random integer

frame = create_board()  # Frame = board (only so that passing on 'board' does not overshadow the original board)
print_board(frame)
game_over = False

pygame.init()

SQUARESIZE = 100

small_rect_width = (5 * SQUARESIZE) - 10  # Used for graphics (non-game)
small_rect_height = SQUARESIZE - 34  # Used for graphics (non-game)
rect_width = 5 * SQUARESIZE  # Used for graphics (non-game)
rect_height = SQUARESIZE - 24  # Used for graphics (non-game)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

init_x = int(width/2 - ((len(TEXT)/2) * 45) + 115)  # Variable used to centre align the theme name text in its frame

size = (width, height)  # of the game screen

RADIUS = int(SQUARESIZE/2 - 5)

# The font palette for every displayed text
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

screen = pygame.display.set_mode(size)  # Turns on the game screen
# welcome_screen(10, 5000)  # Screen 1: Welcome screen is called
# info_page(5, 5000)  # Screen 2: Info page to print the details of the programmer is called
# lets_play(5, 5000)  # Screen 3: "Let's Play!" screen is called
draw_board(frame)
pygame.display.update()

turn = random.randint(PLAYER, AI)  # Decides who gets to play first, Player or AI

# mixer.music.load('Background.mp3')  # Extra song
# mixer.music.play(-1)

mixer.music.load('game_kina.mp3')  # Background music for while game is ongoing
mixer.music.play(-1)  # Makes the background track loop over and over until the game ends and exiting starts

# AI version of the game: main game loop
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the top right 'X' is clicked to exit the game
            sys.exit()

        if event.type == pygame.MOUSEMOTION:  # If mouse motion is detected
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                label = player_prompt_font.render("Player 1's Turn:", 1, PLAYER_COLOUR)
                screen.blit(label, (5, 5))
                pygame.draw.circle(screen, PLAYER_COLOUR, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, AI_COLOUR, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is clicked
            # print(event.pos)
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            # Ask for Player 1 Input
            if turn == PLAYER:
                game_over = player_plays(frame)
                turn += 1
                turn = turn % 2
                print_board(frame)
                draw_board(frame)

            # AI to Play
    if turn == AI and not game_over:
        game_over = ai_plays(frame)
        print_board(frame)
        draw_board(frame)
        turn += 1
        turn = turn % 2

    if tie_game(frame):
        label = win_font.render("It is a tie!", 1, WHITE)
        screen.blit(label, (75, 10))
        pygame.display.update()
        game_over = True

    if game_over:
        condition_game_over()

# -----------------------------------<||>-  ----- <|  END OF PROGRAM  |> -----  -<||>----------------------------------
