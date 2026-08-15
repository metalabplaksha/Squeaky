
import sys
import os
sys.path.append(os.path.abspath("../src/"))
# import src.globe as globe
from src import globe

import pygame
import random
import math

def next_row(num_hop: int) -> list:

    row = [0 for _ in range(0, globe.Island.length + 1)]

    for island_loc in range(0, globe.Island.length + 1):

        if island_loc == 0:
            row[island_loc] += int(bool(globe.Tree.nodes[num_hop - 1]
                                   [island_loc + 1]))

        elif island_loc == globe.Island.length:
            row[island_loc] += int(bool(globe.Tree.nodes[num_hop - 1]
                                   [island_loc - 1]))

        elif 0 < island_loc < globe.Island.length:
            row[island_loc] += int(bool(globe.Tree.nodes[num_hop - 1][island_loc - 1] +
                                        globe.Tree.nodes[num_hop - 1][island_loc + 1]))

    return row


def next_edge(num_hop: int) -> list:
    """returns a matrix with tuple at every island_loc, for previous set of lines, num_hops > 0"""
    edge = [0 for i in range(0, globe.Island.length + 1)]

    for island_loc in range(0, globe.Island.length + 1):

        if island_loc == 0:
            edge[island_loc] = [False,
                                bool(globe.Tree.nodes[num_hop - 1][island_loc + 1])]

        elif island_loc == globe.Island.length:
            edge[island_loc] = [bool(globe.Tree.nodes[num_hop - 1][island_loc - 1]),
                                False]

        elif 0 < island_loc < globe.Island.length:

            edge[island_loc] = [bool(globe.Tree.nodes[num_hop - 1][island_loc - 1]),
                                bool(globe.Tree.nodes[num_hop - 1][island_loc + 1])]

    return edge


def get_cordinates(num_hop: int, island_loc: int) -> tuple[int, int]:

    padding_x = globe.Tree.rel_padding * globe.Tree.size[0]
    padding_y = globe.Tree.rel_padding * globe.Tree.size[1] * 1.75

    k = 3
    H_eff = globe.Tree.size[1] - 2 * padding_y
    N = globe.Squirrel.num_hops

    x = padding_x + island_loc * \
        ((globe.Tree.size[0] - 2 * padding_x) / globe.Island.length)

    y = padding_y + H_eff * num_hop * (math.e ** (k * (num_hop / N - 1)) / N)

    return (x, y)


def draw_nodes(screen_surf: pygame.Surface, nodes: list) -> None:

    num_hops = len(nodes)
    for num_hop in range(0, num_hops):

        for island_loc in range(0, globe.Island.length + 1):

            if nodes[num_hop][island_loc]:
                pygame.draw.circle(screen_surf, globe.Tree.grid_color,
                                   get_cordinates(num_hop, island_loc), radius=1)

    return


def draw_lines(screen_surf: pygame.Surface, nodes: list) -> None:

    num_hops = len(nodes)
    for num_hop in range(0, num_hops):

        for island_loc in range(0, globe.Island.length + 1):

            line_info = globe.Tree.edges[num_hop][island_loc]

            if line_info is not None:

                if line_info[0]:
                    # upper left node draws a line to current

                    # location of top left
                    start_pos = get_cordinates(num_hop - 1, island_loc - 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(screen_surf, globe.Tree.grid_color,
                                     start_pos, end_pos, width=1)

                if line_info[1]:
                    # upper right node draws a line to current location

                    # location of top right
                    start_pos = get_cordinates(num_hop - 1, island_loc + 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(screen_surf, globe.Tree.grid_color,
                                     start_pos, end_pos, width=1)

    return


def draw_choices(screen_surf: pygame.Surface, nodes: list) -> None:

    num_hops = len(nodes)
    for num_hop in range(0, num_hops):

        for island_loc in range(0, globe.Island.length + 1):

            line_info = globe.Tree.choices[num_hop][island_loc]

            if line_info is not None:

                if line_info[0]:
                    # upper left node draws a line to current

                    # location of top left
                    start_pos = get_cordinates(num_hop - 1, island_loc - 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(screen_surf, globe.Tree.path_color,
                                     start_pos, end_pos, width=4)

                if line_info[1]:
                    # upper right node draws a line to current location

                    # location of top right
                    start_pos = get_cordinates(num_hop - 1, island_loc + 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(screen_surf, globe.Tree.path_color,
                                     start_pos, end_pos, width=4)

    return
# --


def run_player() -> None:
    global bool_running

    while 0 < globe.Squirrel.cur_pos < globe.Island.length:

        jump = random.choice([-1, 1])
        # --
        globe.Squirrel.num_hops += 1
        globe.Squirrel.cur_pos += jump

        globe.Tree.choices.append(
            [None for _ in range(0, globe.Island.length + 1)])
        # --

        if jump == -1:
            # inherit from top right parent
            globe.Tree.choices[globe.Squirrel.num_hops][globe.Squirrel.cur_pos] = [
                False, True, "Red"]
            # globe.Tree.choices[globe.Squirrel.num_hops][globe.Squirrel.cur_pos + 2] = [
            #     True, False, "Fluoro-Green"]

        elif jump == 1:
            # inherit from top left parent
            globe.Tree.choices[globe.Squirrel.num_hops][globe.Squirrel.cur_pos] = [
                True, False, "Red"]
            # globe.Tree.choices[globe.Squirrel.num_hops][globe.Squirrel.cur_pos - 2] = [
            #     False, True, "Fluoro-Green"]

        else:
            globe.Tree.choices[globe.Squirrel.num_hops][globe.Squirrel.cur_pos] = None

        globe.Tree.nodes.append([])
        globe.Tree.nodes[globe.Squirrel.num_hops] = next_row(
            globe.Squirrel.num_hops)

        globe.Tree.edges.append([])
        globe.Tree.edges[globe.Squirrel.num_hops] = next_edge(
            globe.Squirrel.num_hops)

        screen.fill(globe.Tree.background_color)
        screen.blit(text, text_pos)
        draw_lines(screen, globe.Tree.edges)
        draw_choices(screen, globe.Tree.choices)
        draw_nodes(screen, globe.Tree.nodes)

        globe.Game.clock.tick(5)
        pygame.display.flip()

    # End the game
    started = False

    return


pygame.init()


def accurate_draw(surface, coordinates):
    # centers the blit-ing to the origin of Surface
    surface_rect = surface.get_rect()
    surface_rect.center = coordinates

    return surface_rect


def text_on_screen(message: str, coordinates: tuple | pygame.Rect, color: tuple, ref_surf: pygame.Surface = None) -> \
        tuple[pygame.Surface, pygame.Rect]:
    """
    message: the message string
    coordinates: coordinates relative to the surface that the text goes on
    """

    # font = pygame.font.Font(globe.Window.font, int(globe.Window.font_size / 2))
    text = globe.Window.font.render(message, True, color)  # True for anti-aliasing

    if ref_surf is None:
        text_pos = accurate_draw(text, coordinates)
    else:
        text_pos = accurate_draw(ref_surf, coordinates)

    return text, text_pos


screen = pygame.display.set_mode(size=globe.Tree.size)
# --
screen.fill(globe.Tree.background_color)
text, text_pos = text_on_screen(
    globe.Tree.tree_message, (globe.Tree.size[0] / 2, globe.Tree.size[1] / 10), globe.Tree.white)

screen.fill(globe.Tree.background_color)
screen.blit(text, text_pos)
# --

# Game Loop, running infinitly untill bool_running is false
bool_running = True
started = True
while bool_running:
    # fetching all events
    for event in pygame.event.get():

        # if quit button is pressed
        if event.type == pygame.QUIT:

            # setting bool_runnning to False
            bool_running = False

    if started:
        run_player()

print("Thanks for Playing the game.")
