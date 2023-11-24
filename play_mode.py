from pico2d import *

import game_framework
import game_world
import server
from ball import Ball
from court import Court
from player import Player
from score import Score
from timer import Timer


camera_x, camara_y = 300, 300


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.player.handle_event(event)


def init():
    # global running
    # global court
    # global player
    #
    # running = True
    #
    # court = Court()
    # game_world.add_object(court, 0)
    #
    # player = Player()
    # game_world.add_object(player, 1)
    #
    # timer = Timer()
    # game_world.add_object(timer, 1)
    #
    # score = Score()
    # game_world.add_object(score, 1)
    #
    # game_world.add_collision_pair('player:ball', player, None)

    server.background = Court()
    game_world.add_object(server.background, 0)

    server.player = Player()
    game_world.add_object(server.player, 1)
    game_world.add_collision_pair('player:ball', server.player, None)

    # server.ball = Ball()
    # game_world.add_object(server.ball, 1)
    # game_world.add_collision_pair('boy:ball', None, server.ball)


def finish():
    game_world.clear()


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass