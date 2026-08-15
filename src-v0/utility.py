# This file contains global functions, classes
from __future__ import annotations

import math
import random

import pygame
import pygame_gui

import globe


def init_game():
    global screen_surf
    global ui_manager

    pygame.init()
    # font = pygame.font.Font(globe.Window.fontpath, int(globe.Window.font_size / 2))
    ui_manager = pygame_gui.UIManager(globe.Window.size)

    # before set_mode line, as advised in Doc
    pygame.display.set_icon(globe.Window.icon)

    screen_surf = pygame.display.set_mode(
        size=globe.Window.size,
        # flags=pygame.RESIZABLE,
        display=0,
    )
    # [display window should be sizeable](https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode)
    print("hi, this is malhar here")

    pygame.display.set_caption(globe.Window.title, globe.Window.small_title)


def text_on_screen(
    message: str,
    coordinates: tuple | pygame.Rect,
    color: tuple,
    ref_surf: pygame.Surface = None,
    font_size: int = None,
) -> tuple[pygame.Surface, pygame.Rect]:
    """
    message: the message string
    coordinates: coordinates relative to the surface that the text goes on
    """

    if font_size == None:
        font = pygame.font.Font(globe.Window.fontpath, int(globe.Window.font_size / 1))

    else:
        font = pygame.font.Font(globe.Window.fontpath, int(font_size))

    text = font.render(message, True, color)  # True for anti-aliasing

    if ref_surf is None:
        text_pos = accurate_draw(text, coordinates)
    else:
        text_pos = accurate_draw(ref_surf, coordinates)

    return text, text_pos


def death_player(
    screen_surf, background_surf, coin_surf, tree_surf, squirrel_surf, bg_size
):
    # Stop Music

    pygame.mixer.music.stop()
    pygame.mixer.music.load(globe.Window.death_music, namehint="mp3")
    pygame.mixer.music.play(loops=1, start=0.0, fade_ms=1)

    last_squirrel_surf = squirrel_surf
    death_y = globe.Squirrel.squirrel_y
    smoothness = 20
    while death_y < globe.Squirrel.death_y:
        death_y += (globe.Squirrel.death_y - globe.Squirrel.squirrel_y) / smoothness

        background_surf.blit(globe.Island.img.convert(), (0, 0))
        background_surf.blit(
            last_squirrel_surf,
            accurate_draw(last_squirrel_surf, (squirrel_location(), death_y)),
        )

        screen_surf.blit(pygame.transform.scale(background_surf, bg_size), (0, 0))
        pygame.display.flip()  # flips the blit on to the next frame, updates the frame

    last_squirrel_surf.blit(globe.Squirrel.splash_img.convert_alpha(), (0, 0))
    # Text on screen
    text, text_pos = text_on_screen(
        globe.Window.end_message,
        # background.get_rect().center,
        [sum(x) for x in zip(background_surf.get_rect().center, (0, -60))],
        (255, 255, 255, 1),
        font_size=globe.Window.font_size * 2,
    )
    text_s1, text_pos_s1 = text_on_screen(
        globe.Window.probslider_message,
        [sum(x) for x in zip(background_surf.get_rect().center, (0, 20))],
        (255, 255, 255, 1),
        font_size=globe.Window.font_size / 1,
    )
    text_s2, text_pos_s2 = text_on_screen(
        globe.Window.initposslider_message,
        [sum(x) for x in zip(background_surf.get_rect().center, (0, 120))],
        (255, 255, 255, 1),
        font_size=globe.Window.font_size / 1,
    )
    font = pygame.font.Font(globe.Window.fontpath, int(globe.Window.font_size / 2))
    # live p values
    xpos1 = screen_surf.get_rect().center[0] + 120
    xpos2 = screen_surf.get_rect().center[0] - 270
    yposp = screen_surf.get_rect().center[1] + 65
    text_surface_probr = font.render(
        f"Prob(right) = {round(globe.Squirrel.p_right, 2)}", True, (255, 255, 255)
    )
    text_surface_probl = font.render(
        f"Prob(left) = {round(1-globe.Squirrel.p_right, 2)}", True, (255, 255, 255)
    )
    # live initpos values
    font1 = pygame.font.Font(globe.Window.fontpath, int(globe.Window.font_size / 1.5))
    xpos = screen_surf.get_rect().center[0] + 130
    ypos = screen_surf.get_rect().center[1] + 110
    text_surface_initpos = font1.render(
        f"{globe.Squirrel.init_pos}", True, (255, 255, 255)
    )

    background_surf.blit(text, text_pos)
    background_surf.blit(
        last_squirrel_surf,
        accurate_draw(last_squirrel_surf, (squirrel_location(), death_y)),
    )
    background_surf.blit(text_s1, text_pos_s1)
    background_surf.blit(text_s2, text_pos_s2)

    screen_surf.blit(pygame.transform.scale(background_surf, bg_size), (0, 0))
    screen_surf.fill((0, 0, 0), (xpos1, yposp, 165, 13))
    screen_surf.fill((0, 0, 0), (xpos2, yposp, 155, 13))
    screen_surf.blit(text_surface_probr, (xpos1, yposp))
    screen_surf.blit(text_surface_probl, (xpos2, yposp))
    screen_surf.fill((0, 0, 0), (xpos, ypos, 20, 12))
    screen_surf.blit(text_surface_initpos, (xpos, ypos))
    globe.Game.clock.tick(globe.Game.fps)  # I am not sure what this does
    pygame.display.flip()  # flips the blit on to the next frame, updates the frame


def player(
    screen_surf, background_surf, coin_surf, tree_surf, squirrel_surf, bg_size
) -> tuple[bool, bool, bool]:
    death = False
    started = True
    success = False

    if globe.Squirrel.cur_pos == 0 or globe.Squirrel.cur_pos == globe.Island.length:
        death = True
        started = False
        success = False

        death_player(
            screen_surf, background_surf, coin_surf, tree_surf, squirrel_surf, bg_size
        )

        globe.Squirrel.cur_pos = globe.Squirrel.init_pos
        globe.Squirrel.num_hops = 0

        globe.Tree.nodes = [[0 for _ in range(0, globe.Island.length + 1)]]
        globe.Tree.edges = [[None for _ in range(0, globe.Island.length + 1)]]
        globe.Tree.choices = [[None for _ in range(0, globe.Island.length + 1)]]

        globe.Tree.nodes[globe.Squirrel.num_hops][globe.Squirrel.cur_pos] = 1

    else:
        jump = random.choices(
            [-1 * globe.Squirrel.left_stepsize, 1 * globe.Squirrel.right_stepsize],
            weights=[1 - globe.Squirrel.p_right, globe.Squirrel.p_right],
            k=1,
        )[0]

        globe.Squirrel.num_hops += 1
        globe.Squirrel.cur_pos += jump

        globe.Tree.choices.append([None for _ in range(0, globe.Island.length + 1)])

        if jump == -1 * globe.Squirrel.left_stepsize:
            # Tails or Left Jump
            coin_toss(screen_surf, background_surf, coin_surf, bg_size, -1)
            # I am not sure what this does
            globe.Game.clock.tick(globe.Game.fps)

            squirrel_surf = squirrel_draw(squirrel_surf, -1)
            coin_surf = coin_window(coin_surf, "TAILS", -1)
            globe.Tree.choices[globe.Squirrel.num_hops][globe.Squirrel.cur_pos] = [
                False,
                True,
                "Red",
            ]

        elif jump == 1 * globe.Squirrel.right_stepsize:
            # Heads or Right Jump
            coin_toss(screen_surf, background_surf, coin_surf, bg_size, 1)
            # I am not sure what this does
            globe.Game.clock.tick(globe.Game.fps)

            squirrel_surf = squirrel_draw(squirrel_surf, 1)
            coin_surf = coin_window(coin_surf, "HEADS", 1)
            globe.Tree.choices[globe.Squirrel.num_hops][globe.Squirrel.cur_pos] = [
                True,
                False,
                "Red",
            ]

        else:
            raise "Error with Random Choice from list [-1, 1]"

        globe.Tree.nodes.append([])
        globe.Tree.nodes[globe.Squirrel.num_hops] = next_row(globe.Squirrel.num_hops)

        globe.Tree.edges.append([])
        globe.Tree.edges[globe.Squirrel.num_hops] = next_edge(globe.Squirrel.num_hops)

        tree_surf.fill((250, 250, 250, 0))

        tree_pos = accurate_draw(tree_surf, globe.Tree.abs_pos)
        tree_text, tree_pos = text_on_screen(
            message=globe.Tree.tree_message,
            coordinates=tree_pos.center,
            color=(250, 250, 250),
            ref_surf=tree_surf,
            font_size=globe.Window.font_size / 1.5,
        )

        tree_surf.blit(
            tree_text,
            accurate_draw(
                tree_text, (globe.Tree.width / 2, globe.Tree.height * 9 / 10)
            ),
        )

        draw_lines(tree_surf, globe.Tree.edges)
        draw_choices(tree_surf, globe.Tree.choices)
        draw_nodes(tree_surf, globe.Tree.nodes)

        # globe.Squirrel.cur_pos += 1
        update_background(
            screen_surf, background_surf, coin_surf, tree_surf, squirrel_surf, bg_size
        )
        # I am not sure what this does
        globe.Game.clock.tick(globe.Game.fps)

        success = True

    return success, death, started


def squirrel_draw(squirrel_surf, mode):
    squirrel_surf.fill((0, 0, 0, 0))
    if mode == -1:
        squirrel_surf.blit(globe.Squirrel.img.convert(), (0, 0))
    elif mode == 1:
        squirrel_surf.blit(globe.Squirrel.rev_img.convert(), (0, 0))

    return squirrel_surf


def coin_toss(screen_surf, background, coin_surf, bg_size, mode):
    smoothness = math.pi * (1 - math.exp(-globe.Game.fps / 300)) / 2
    angle = 0 + smoothness

    if mode == -1:
        img = globe.Coin.tails_img.convert_alpha()
    else:
        img = globe.Coin.heads_img.convert_alpha()
    empty = pygame.Color(0, 0, 0, 0)
    while angle < math.pi / 2 + smoothness:
        # pygame.draw.circle(coin_surf, (250, 250, 250, 1),
        #                    coin_surf.get_rect().center, globe.Coin.size[0] / 2)  # HARD CODING SOME STUFF
        coin_surf.fill(empty)
        angle += smoothness

        x_width = globe.Coin.coin_size[0] * math.sin(angle)

        temp_img = pygame.transform.scale(img, (x_width, globe.Coin.coin_size[1]))
        coin_surf.blit(
            temp_img,
            accurate_draw(
                temp_img,
                (coin_surf.get_rect().centerx, coin_surf.get_rect().centery * 2 / 3),
            ),
        )

        background.blit(coin_surf, accurate_draw(coin_surf, globe.Coin.abs_pos))
        screen_surf.blit(pygame.transform.scale(background, bg_size), (0, 0))
        globe.Game.clock.tick()
        pygame.display.flip()  # flips the blit on to the next frame, updates the frame


def coin_window(coin_surf, message, mode):
    coin_surf.fill((0, 0, 0, 0))
    # pygame.draw.circle(coin_surf, (250, 250, 250, 0),
    #                    coin_surf.get_rect().center, globe.Coin.size[0] / 2)  # HARD CODING SOME STUFF

    if mode == -1:
        coin_surf.blit(
            globe.Coin.tails_img.convert_alpha(),
            (
                accurate_draw(
                    globe.Coin.tails_img,
                    (
                        coin_surf.get_rect().centerx,
                        coin_surf.get_rect().centery * 2 / 3,
                    ),
                )
            ),
        )
    elif mode == 1:
        coin_surf.blit(
            globe.Coin.heads_img.convert_alpha(),
            (
                accurate_draw(
                    globe.Coin.tails_img,
                    (
                        coin_surf.get_rect().centerx,
                        coin_surf.get_rect().centery * 2 / 3,
                    ),
                )
            ),
        )

    coin_text, _ = text_on_screen(
        message=message,
        coordinates=coin_surf.get_rect().center,
        color=(250, 250, 250, 1),
        ref_surf=coin_surf,
    )
    coin_surf.blit(
        coin_text,
        accurate_draw(coin_text, (globe.Coin.width / 2, globe.Coin.height * 4 / 6)),
    )

    return coin_surf


def accurate_draw(surface, coordinates):
    # centers the blit-ing to the origin of Surface
    surface_rect = surface.get_rect()
    surface_rect.center = coordinates

    return surface_rect


def squirrel_location():
    return globe.Squirrel.rel_grid_pos[globe.Squirrel.cur_pos] * globe.Island.width


def return_surface(
    size: tuple, init_color: tuple | None, mode: str = None, shape: str = None
) -> pygame.Surface:
    # a pygame object, to be modified with pygame methods
    surface = pygame.Surface(size)

    if mode == "convert":
        # converting to single pixel format to drastically speed up rendering times.
        surface = surface.convert()

    elif mode == "convert_alpha":
        surface = surface.convert_alpha()

    if init_color is not None:
        if shape is None:
            surface.fill(init_color)
        else:
            if shape == "circle":
                # print("A circle")
                pygame.draw.circle(
                    surface, init_color, surface.get_rect().center, size[0] / 2
                )

    return surface


def game_loop():
    # utility globals
    # init_pos = globe.Squirrel.cur_pos
    bg_size = screen_surf.get_size()

    (
        background,
        coin_surf,
        tree_surf,
        squirrel_surf,
        prob_slider,
        initpos_slider,
    ) = background_load(screen_surf)

    started = False
    dead = False
    bool_running = True
    while bool_running:
        # This is important for programs that want to share the system with other applications.
        # pygame.event.pump()  # to allow pygame to handle internal actions, calls the event queue
        # current_event = pygame.event.wait()  # fetches one event

        time_delta = globe.Game.clock.tick(60) / 1000.0

        for current_event in pygame.event.get():
            if current_event.type == pygame.QUIT:
                # checking for quit
                bool_running = False
                return
            elif started and current_event.type == pygame.KEYDOWN:
                if current_event.key == pygame.K_ESCAPE:
                    print("ESCAPE")
                    started = False
                    dead = True
                    pygame.mixer.music.stop()
                    globe.Squirrel.num_hops = 0
                    globe.Tree.nodes = [[0 for _ in range(0, globe.Island.length + 1)]]
                    globe.Tree.edges = [
                        [None for _ in range(0, globe.Island.length + 1)]
                    ]
                    globe.Tree.choices = [
                        [None for _ in range(0, globe.Island.length + 1)]
                    ]
                    globe.Tree.nodes[globe.Squirrel.num_hops][
                        globe.Squirrel.cur_pos
                    ] = 1

                    # return to initial screen

                    # screen_surf.blit(pygame.transform.scale(background, bg_size), (0, 0))
                    # background.blit(globe.Island.img.convert(), (0, 0))
                    prob_slider.kill()  # Assuming prob_slider is a pygame_gui element, remove it from the UI
                    initpos_slider.kill()  # Remove other GUI elements similarly

                    (
                        background,
                        coin_surf,
                        tree_surf,
                        squirrel_surf,
                        prob_slider,
                        initpos_slider,
                    ) = background_load(screen_surf)

                    # bool_running = False
                    # return

            elif not started and current_event.type == pygame.KEYDOWN:
                if current_event.key == pygame.K_SPACE:
                    # If space-bar pressed
                    started = True
                    dead = False

                    pygame.mixer.music.load(globe.Window.main_music, namehint="mp3")
                    # fades into 100 volume in 5ms
                    # pygame.mixer.music.play(loops=-1, start=3.3, fade_ms=5)
                    pygame.mixer.music.play(loops=-1, start=20, fade_ms=5)

            elif current_event.type == pygame.VIDEORESIZE:
                # in the running frame it is updated later on:
                bg_size = current_event.dict["size"]
            if current_event.type == pygame.USEREVENT:
                if current_event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    # Update parameter values when a slider is moved
                    font = pygame.font.Font(
                        globe.Window.fontpath, int(globe.Window.font_size / 2)
                    )

                    if current_event.ui_element == prob_slider:
                        value = current_event.ui_element.get_current_value()
                        print(f"Probability Slider moved to {value}")
                        globe.Squirrel.p_right = value

                        xpos1 = background.get_rect().center[0] + 120
                        xpos2 = background.get_rect().center[0] - 270
                        ypos = background.get_rect().center[1] + 65
                        screen_surf.fill((0, 0, 0), (xpos1, ypos, 165, 13))
                        screen_surf.fill((0, 0, 0), (xpos2, ypos, 155, 13))
                        text_surface_probr = font.render(
                            f"Prob(right) = {round(value, 2)}", True, (255, 255, 255)
                        )
                        text_surface_probl = font.render(
                            f"Prob(left) = {round(1-value, 2)}", True, (255, 255, 255)
                        )
                        screen_surf.blit(text_surface_probr, (xpos1, ypos))
                        screen_surf.blit(text_surface_probl, (xpos2, ypos))

                    if current_event.ui_element == initpos_slider:
                        value = current_event.ui_element.get_current_value()
                        print(f"InitPos Slider moved to {value}")
                        globe.Squirrel.init_pos = value
                        globe.Tree.nodes[globe.Squirrel.num_hops][
                            globe.Squirrel.cur_pos
                        ] = 0
                        globe.Squirrel.cur_pos = value
                        globe.Tree.nodes[globe.Squirrel.num_hops][
                            globe.Squirrel.cur_pos
                        ] = 1

                        font1 = pygame.font.Font(
                            globe.Window.fontpath, int(globe.Window.font_size / 1.5)
                        )
                        xpos = background.get_rect().center[0] + 130
                        ypos = background.get_rect().center[1] + 110
                        screen_surf.fill((0, 0, 0), (xpos, ypos, 25, 15))
                        text_surface_initpos = font1.render(
                            f"{globe.Squirrel.cur_pos}", True, (255, 255, 255)
                        )
                        screen_surf.blit(text_surface_initpos, (xpos, ypos))

            ui_manager.process_events(current_event)

        if not dead and started:
            # if game already started
            success, dead, started = player(
                screen_surf, background, coin_surf, tree_surf, squirrel_surf, bg_size
            )
            if success:
                # if everything inside player went OK
                update_background(
                    screen_surf,
                    background,
                    coin_surf,
                    tree_surf,
                    squirrel_surf,
                    bg_size,
                )

        # for UI elements => sliders buttons etc
        ui_manager.update(time_delta)
        if dead or not started:
            ui_manager.draw_ui(screen_surf)
        globe.Game.clock.tick(globe.Game.fps)  # I am not sure what this does
        pygame.display.flip()  # updating the frame


def background_load(
    screen_surf,
) -> tuple[pygame.Surface, pygame.Surface, pygame.Surface, pygame.Surface]:
    # Called only once, at the beginning of game_loop()
    bg_size = screen_surf.get_size()
    # The background object
    background = return_surface(
        size=bg_size, init_color=globe.Window.background, mode="convert"
    )

    # Text object on screen
    text, text_pos = text_on_screen(
        globe.Window.start_message,
        # background.get_rect().center,
        [sum(x) for x in zip(background.get_rect().center, (0, -100))],
        (255, 255, 255, 1),
        font_size=globe.Window.font_size * 2,
    )

    # Text for probability slider
    text_s1, text_pos_s1 = text_on_screen(
        globe.Window.probslider_message,
        [sum(x) for x in zip(background.get_rect().center, (0, 20))],
        (255, 255, 255, 1),
        font_size=globe.Window.font_size / 1,
    )

    # Text for initpos slider
    text_s2, text_pos_s2 = text_on_screen(
        globe.Window.initposslider_message,
        [sum(x) for x in zip(background.get_rect().center, (0, 120))],
        (255, 255, 255, 1),
        font_size=globe.Window.font_size / 1,
    )

    # live p values
    font = pygame.font.Font(globe.Window.fontpath, int(globe.Window.font_size / 2))
    xpos1 = background.get_rect().center[0] + 120
    xpos2 = background.get_rect().center[0] - 270
    yposp = background.get_rect().center[1] + 65
    text_surface_probr = font.render(
        f"Prob(right) = {round(globe.Squirrel.p_right, 2)}", True, (255, 255, 255)
    )
    text_surface_probl = font.render(
        f"Prob(left) = {round(1-globe.Squirrel.p_right, 2)}", True, (255, 255, 255)
    )

    # live initpos values
    font1 = pygame.font.Font(globe.Window.fontpath, int(globe.Window.font_size / 1.5))
    xpos = background.get_rect().center[0] + 130
    ypos = background.get_rect().center[1] + 110
    text_surface_initpos = font1.render(
        f"{globe.Squirrel.cur_pos}", True, (255, 255, 255)
    )

    # Squirrel Surface
    squirrel_surf = return_surface(
        size=globe.Squirrel.size, init_color=(0, 0, 0, 0), mode="convert_alpha"
    )
    squirrel_surf.blit(globe.Squirrel.img.convert_alpha(), (0, 0))

    # Coin Window Surface
    coin_surf = return_surface(
        size=globe.Coin.size, init_color=(0, 0, 0), mode="convert_alpha", shape="circle"
    )
    coin_surf.blit(
        globe.Coin.heads_img.convert_alpha(),
        accurate_draw(globe.Coin.heads_img, coin_surf.get_rect().center),
    )

    pygame.draw.rect(coin_surf, (250, 250, 250, 0.5), coin_surf.get_rect(), width=3)
    coin_pos = accurate_draw(coin_surf, globe.Coin.abs_pos)
    # Coin Text on screen
    coin_text, coin_pos = text_on_screen(
        message="-----",
        coordinates=coin_pos.center,
        color=(250, 250, 250, 1),
        ref_surf=coin_surf,
    )
    coin_surf.blit(
        coin_text,
        accurate_draw(coin_text, (globe.Coin.width / 2, globe.Coin.height * 3 / 6)),
    )

    # Tree Window Surface
    tree_surf = return_surface(
        size=globe.Tree.size,
        init_color=globe.Tree.background_color,
        mode="convert_alpha",
    )
    pygame.draw.rect(tree_surf, (250, 250, 250, 0.5), tree_surf.get_rect(), width=3)
    tree_pos = accurate_draw(tree_surf, globe.Tree.abs_pos)
    tree_text, tree_pos = text_on_screen(
        message=globe.Tree.tree_message,
        coordinates=tree_pos.center,
        color=(250, 250, 250),
        ref_surf=tree_surf,
        font_size=globe.Window.font_size / 1.5,
    )
    tree_surf.fill(globe.Tree.background_color)
    tree_surf.blit(
        tree_text,
        accurate_draw(tree_text, (globe.Tree.width / 2, globe.Tree.height * 9 / 10)),
    )

    prob_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(
            globe.Window.probslider_pos, globe.Window.probslider_size
        ),
        start_value=globe.Squirrel.p_right,
        value_range=(0.0, 1.0),
        manager=ui_manager,
    )
    initpos_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(
            globe.Window.initposslider_pos, globe.Window.initposslider_size
        ),
        start_value=globe.Squirrel.cur_pos,
        value_range=(0, globe.Island.length),
        manager=ui_manager,
    )

    # ------------
    background.blit(text, text_pos)
    background.blit(text_s1, text_pos_s1)
    background.blit(text_s2, text_pos_s2)
    # background.blit(text_surface_probr, text_pos_surface_probr)
    # background.blit(text_surface_probl, text_pos_surface_probl)
    screen_surf.blit(pygame.transform.scale(background, bg_size), (0, 0))

    screen_surf.fill((0, 0, 0), (xpos1, yposp, 165, 13))
    screen_surf.fill((0, 0, 0), (xpos2, yposp, 155, 13))
    screen_surf.blit(text_surface_probr, (xpos1, yposp))
    screen_surf.blit(text_surface_probl, (xpos2, yposp))
    screen_surf.fill((0, 0, 0), (xpos, ypos, 25, 15))
    screen_surf.blit(text_surface_initpos, (xpos, ypos))

    globe.Game.clock.tick(globe.Game.fps)  # I am not sure what this does
    pygame.display.flip()  # updating the frame

    return (
        background,
        coin_surf,
        tree_surf,
        squirrel_surf,
        prob_slider,
        initpos_slider,
    )


def update_background(
    screen_surf,
    background: pygame.Surface,
    coin_surf,
    tree_surf,
    squirrel_surf,
    bg_size,
):
    # updates the background object
    background.blit(globe.Island.img.convert(), (0, 0))
    # pygame.draw.rect(background, (0, 0, 0, 1), background.get_rect(), width=int(1 + abs(
    #    globe.Squirrel.cur_pos - globe.Island.length / 2) * 0.2 * globe.Game.border_width_limit / globe.Island.length))

    background.blit(coin_surf, accurate_draw(coin_surf, globe.Coin.abs_pos))
    background.blit(tree_surf, accurate_draw(tree_surf, globe.Tree.abs_pos))
    background.blit(
        squirrel_surf,
        accurate_draw(squirrel_surf, (squirrel_location(), globe.Squirrel.squirrel_y)),
    )

    # Blit-ing everything to the screen
    screen_surf.blit(pygame.transform.scale(background, bg_size), (0, 0))
    globe.Game.clock.tick(globe.Game.fps)  # I am not sure what this does
    pygame.display.flip()  # flips the blit on to the next frame, updates the frame
    # blit-ing, which is where you copy the pixels belonging to said object onto the destination object


def next_row(num_hop: int) -> list:
    row = [0 for _ in range(0, globe.Island.length + 1)]

    for island_loc in range(0, globe.Island.length + 1):
        if island_loc == 0:
            row[island_loc] += int(bool(globe.Tree.nodes[num_hop - 1][island_loc + 1]))

        elif island_loc == globe.Island.length:
            row[island_loc] += int(bool(globe.Tree.nodes[num_hop - 1][island_loc - 1]))

        elif 0 < island_loc < globe.Island.length:
            row[island_loc] += int(
                bool(
                    globe.Tree.nodes[num_hop - 1][island_loc - 1]
                    + globe.Tree.nodes[num_hop - 1][island_loc + 1]
                )
            )

    return row


def next_edge(num_hop: int) -> list:
    """returns a matrix with tuple at every island_loc, for previous set of lines, num_hops > 0"""
    edge = [0 for i in range(0, globe.Island.length + 1)]

    for island_loc in range(0, globe.Island.length + 1):
        if island_loc == 0:
            edge[island_loc] = [
                False,
                bool(globe.Tree.nodes[num_hop - 1][island_loc + 1]),
            ]

        elif island_loc == globe.Island.length:
            edge[island_loc] = [
                bool(globe.Tree.nodes[num_hop - 1][island_loc - 1]),
                False,
            ]

        elif 0 < island_loc < globe.Island.length:
            edge[island_loc] = [
                bool(globe.Tree.nodes[num_hop - 1][island_loc - 1]),
                bool(globe.Tree.nodes[num_hop - 1][island_loc + 1]),
            ]

    return edge


def get_cordinates(num_hop: int, island_loc: int) -> tuple[int, int]:
    padding_x = globe.Tree.rel_padding * globe.Tree.size[0]
    padding_y = globe.Tree.rel_padding * globe.Tree.size[1] * 1.75

    k = 3
    H_eff = globe.Tree.size[1] - 2 * padding_y
    N = globe.Squirrel.num_hops

    x = padding_x + island_loc * (
        (globe.Tree.size[0] - 2 * padding_x) / globe.Island.length
    )

    y = padding_y + H_eff * num_hop * (math.e ** (k * (num_hop / N - 1)) / N)

    return (x, y)


def draw_nodes(screen_surf: pygame.Surface, nodes: list) -> None:
    num_hops = len(nodes)
    for num_hop in range(0, num_hops):
        for island_loc in range(0, globe.Island.length + 1):
            if nodes[num_hop][island_loc]:
                pygame.draw.circle(
                    screen_surf,
                    globe.Tree.grid_color,
                    get_cordinates(num_hop, island_loc),
                    radius=1,
                )

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

                    pygame.draw.line(
                        screen_surf, globe.Tree.grid_color, start_pos, end_pos, width=1
                    )

                if line_info[1]:
                    # upper right node draws a line to current location

                    # location of top right
                    start_pos = get_cordinates(num_hop - 1, island_loc + 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(
                        screen_surf, globe.Tree.grid_color, start_pos, end_pos, width=1
                    )

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

                    pygame.draw.line(
                        screen_surf, globe.Tree.path_color, start_pos, end_pos, width=4
                    )

                if line_info[1]:
                    # upper right node draws a line to current location

                    # location of top right
                    start_pos = get_cordinates(num_hop - 1, island_loc + 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(
                        screen_surf, globe.Tree.path_color, start_pos, end_pos, width=4
                    )

    return
