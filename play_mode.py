from pico2d import *

import game_framework
import game_world
import server
from ball import Ball
from background import Background
from blocker import Blocker
from player import Player
from score import Score
from setter import Setter
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
    server.background = Background()
    game_world.add_object(server.background, 0)

    server.player = Player()
    game_world.add_object(server.player, 1)
    game_world.add_collision_pair('player:ball', server.player, None)

    server.setter = Setter(485, 85)
    game_world.add_object(server.setter, 1)
    game_world.add_collision_pair('setter:ball', server.setter, None)

    server.blocker = Blocker(470, 85)
    game_world.add_object(server.blocker, 1)
    game_world.add_collision_pair('blocker:ball', server.blocker, None)

    server.enemy_setter = Setter(515, 85)
    game_world.add_object(server.enemy_setter, 1)
    game_world.add_collision_pair('setter:ball', server.enemy_setter, None)

    server.ball = Ball(server.setter.x + 25, server.setter.y + 10, 0, 1, 5)
    game_world.add_object(server.ball, 1)
    game_world.add_collision_pair('player:ball', None, server.ball)
    game_world.add_collision_pair('setter:ball', None, server.ball)

    server.timer = Timer()
    game_world.add_object(server.timer, 1)

    server.score = Score()
    game_world.add_object(server.score, 1)


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