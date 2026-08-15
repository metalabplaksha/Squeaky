# -*- coding: utf-8 -*-

# import pygame_gui
import os

import pygame

# import math
# for math.e, for intelligently handling Squirel.height
# this file includes all the parameters, variables, and initialisers
# Window globals


class Window(object):
    asp_ratio = 2880 / 1442  # w:h, longer height to fit GUI Interactives

    width = 1600  # in px
    height = width * asp_ratio**-1  # in px

    size = (width, height)

    background = (0, 120, 120)  # default background, RGB Plaksha Colour

    title = "Random Walk on a Lonely Island"
    small_title = "Squeaky's Demise"

    start_message = "Welcome! Press spacebar to start."
    end_message = "Press spacebar to play again!"

    probslider_size = (200, 30)
    probslider_pos = (width / 2 - probslider_size[0] / 2, height / 2 + 55)
    probslider_message = "Set probability of jump direction"

    initposslider_size = (200, 30)
    initposslider_pos = (width / 2 - initposslider_size[0] / 2, height / 2 + 140)
    initposslider_message = "Set initial position       "

    icon = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/plaksha.png")
    )
    rel_padding = 0.13
    hor_padding = rel_padding * width

    main_music = os.path.join(
        os.path.dirname(__file__), "../assets/music/rock_around.ogg"
    )
    death_music = os.path.join(
        os.path.dirname(__file__), "../assets/music/pacman_die.ogg"
    )

    fontpath = os.path.join(os.path.dirname(__file__), "../assets/fonts/courier.ttf")
    font_size = 30
    # font = pygame.font.Font(fontpath, int(font_size / 2))
    # ui_manager = pygame_gui.UIManager(size)


# Island globals
class Island(object):
    img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/island-final.png")
    )

    asp_ratio = 2880 / 1442  # w:h

    width = Window.width  # in px
    height = width * asp_ratio**-1  # in px

    size = (width, height)

    img = pygame.transform.scale(img, size)  # rescaling to fit width

    length = 36  # default size of island


# Squirrel globals
class Squirrel(object):
    asp_ratio = 1 / 1  # w:h
    # * (math.e ** (-Island.length / 1000))
    # !! this makes it very necessary to define island properties before squirel
    height = Island.height * (1 / 10)
    width = height * asp_ratio  # in px

    size = (width, height)

    cur_pos = 18  # default starting position of squirel
    init_pos = cur_pos

    rel_height = 0.67  # squirel stands 2 / 3 of island image height, from top

    img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/squirrel.png")
    )
    img = pygame.transform.scale(img, size)
    # reversed image to save time
    rev_img = pygame.transform.flip(img, True, False)

    splash_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/splash.png")
    )
    splash_img = pygame.transform.scale(splash_img, size)  # reversed image to save time

    # set colorkeys
    img.set_colorkey((0, 0, 0))
    rev_img.set_colorkey((0, 0, 0))
    splash_img.set_colorkey((0, 0, 0))

    rel_grid_pos = [
        Window.rel_padding + i * (1 - 2 * Window.rel_padding) / Island.length
        for i in range(0, Island.length + 1)
    ]

    rel_death_y = 5 / 6
    death_y = rel_death_y * Island.height
    squirrel_y = rel_height * Island.height

    num_hops = 0

    # probability of jumping right (and consequently left)
    p_right = 0.5

    # left and right step sizes (why not)
    left_stepsize = 1
    right_stepsize = 1


# Coin globals
class Coin(object):  # Coin_Window actually
    asp_ratio = 1 / 1  # w:h

    height = Island.height * (1 / 4)
    width = height * asp_ratio

    size = (width, height)  # The window size

    rel_pos = (1 - 1.79 / 3, 1.03 / 2)
    abs_pos = (rel_pos[0] * Island.width, rel_pos[1] * Island.height)

    heads_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/heads.png")
    )
    tails_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/tails.png")
    )

    coin_size = (size[0] / (2.5), size[1] / 2.5)
    heads_img = pygame.transform.scale(heads_img, coin_size)
    tails_img = pygame.transform.scale(tails_img, coin_size)


class Tree(object):
    asp_ratio = 1 / 1  # w:h

    height = Island.height * (1 / 4)
    width = height * asp_ratio * 1.25

    size = (width, height)  # The window size

    rel_pos = (1.79 / 3, 0.9 / 2)
    abs_pos = (rel_pos[0] * Island.width, rel_pos[1] * Island.height)

    rel_padding = 1 / 10

    # has 1 where the node is
    nodes = [[0 for _ in range(0, Island.length + 1)]]
    edges = [[None for _ in range(0, Island.length + 1)]]
    choices = [[None for _ in range(0, Island.length + 1)]]

    nodes[Squirrel.num_hops][Squirrel.cur_pos] = 1

    white = (150, 150, 150)
    red = (250, 0, 0)
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    cyan = (153, 255, 255)
    grey = (150, 150, 150)
    pink = (255, 192, 203)
    fluoro_green = (0, 250, 0)
    path_color = fluoro_green
    grid_color = grey
    background_color = (250, 250, 250, 0)

    tree_message = "Probability Path"


# Game globals
class Game(object):
    fps = 30  # fps
    clock = pygame.time.Clock()

    border_width_limit = int(5 * Island.size[0] * Window.rel_padding)
    border_width = int(abs(Squirrel.cur_pos) * border_width_limit / Island.length)
