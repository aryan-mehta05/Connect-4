### Using all these lines of code, try implementing a MENU driven pygame (python) code! ###

# import numpy as np
# import random
# import pygame
# import sys
# import math
# from pygame import mixer


# CLICK = False
#
#
# def display_menu(player_colour, ai_colour, board_colour):
#     while True:
#         mx, my = pygame.mouse.get_pos()
#
        # button_1 = pygame.draw.rect(screen, CYAN, (200, 202, rect_width, rect_height), 0)
        # button_2 = pygame.draw.rect(screen, CYAN, (200, 302, rect_width, rect_height), 0)
        # button_3 = pygame.draw.rect(screen, CYAN, (200, 402, rect_width, rect_height), 0)
        # button_4 = pygame.draw.rect(screen, CYAN, (200, 502, rect_width, rect_height), 0)
        # pygame.draw.rect(screen, BLACK, (205, 207, small_rect_width, small_rect_height), 0)
        # pygame.draw.rect(screen, BLACK, (205, 307, small_rect_width, small_rect_height), 0)
        # pygame.draw.rect(screen, BLACK, (205, 407, small_rect_width, small_rect_height), 0)
        # pygame.draw.rect(screen, BLACK, (205, 507, small_rect_width, small_rect_height), 0)
#         menu = text_menu.render("SELECT THEME", 1, WHITE)
#         bar_1 = menu_font.render("Default", 1, WHITE)
#         bar_2 = menu_font.render("Monotone", 1, WHITE)
#         bar_3 = menu_font.render("Pink Panther", 1, WHITE)
#         quit_bar = menu_font.render("Tom and Jerry", 1, WHITE)
#         # settings = pygame.image.load("Settings.png").convert_alpha()
#         screen.blit(menu, (115, 110))
#         screen.blit(bar_1, (285, 215))
#         screen.blit(bar_2, (260, 315))
#         screen.blit(bar_3, (230, 415))
#         screen.blit(quit_bar, (215, 515))
#         # screen.blit(settings, (640, 10))
#
#         if button_1.collidepoint((mx, my)):
#             if CLICK:
#                 return (YELLOW, RED, BLUE)
#                 # return default(player_colour, ai_colour, board_colour)
#         if button_2.collidepoint((mx, my)):
#             if CLICK:
#                 return monotone(player_colour, ai_colour, board_colour)
#         if button_3.collidepoint((mx, my)):
#             if CLICK:
#                 return pink_panther(player_colour, ai_colour, board_colour)
#         if button_4.collidepoint((mx, my)):
#             if CLICK:
#                 return tom_and_jerry(player_colour, ai_colour, board_colour)
#
#         CLICK = False
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     pygame.quit()
#                     sys.exit()
#             if event.type == MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     CLICK = True
#
#         pygame.display.update()
#         mainClock.tick(60)


# def default(player_colour, ai_colour, board_colour):
#     player_colour = YELLOW
#     ai_colour = RED
#     board_colour = BLUE
#     return (player_colour, ai_colour, board_colour)
#
#     # running = True
#     # while running:
#     #     screen.fill((0, 0, 0))
#     #     for event in pygame.event.get():
#     #         if event.type == QUIT:
#     #             pygame.quit()
#     #             sys.exit()
#     #         if event.type == KEYDOWN:
#     #             if event.key == K_ESCAPE:
#     #                 running = False
#     #     pygame.display.update()
#     #     mainClock.tick(60)
#
#
# def monotone(player_colour, ai_colour, board_colour):
#     running = True
#     while running:
#         screen.fill((0, 0, 0))
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     running = False
#         pygame.display.update()
#         mainClock.tick(60)
#
#
# def pink_panther(player_colour, ai_colour, board_colour):
#     running = True
#     while running:
#         screen.fill((0, 0, 0))
#
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     running = False
#         pygame.display.update()
#         mainClock.tick(60)
#
#
# def tom_and_jerry(player_colour, ai_colour, board_colour):
#     running = True
#     while running:
#         screen.fill((0, 0, 0))
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     running = False
#         pygame.display.update()
#         mainClock.tick(60)


# display_menu(player_colour, ai_colour, board_colour)
# pygame.display.update()
# pygame.time.wait(20000)

print("Hello World!")