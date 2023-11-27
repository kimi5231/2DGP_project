from pico2d import *

import game_framework
import game_world
import server
from ball import Ball
from background import Background, Player_Court, AI_Court, Player_Court_Out, AI_Court_Out, Net
from blocker import Blocker
from enemy_blocker import Enemy_Blocker
from judge import Judge
from player import Player
from score import Score
from setter import Setter
from spiker import Spiker
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
            server.blocker1.handle_event(event)
            server.blocker2.handle_event(event)


def init():
    server.background = Background()
    game_world.add_object(server.background, 0)

    server.player_court = Player_Court()
    game_world.add_object(server.player_court, 0)
    game_world.add_collision_pair('player_court:ball', server.player_court, None)

    server.ai_court = AI_Court()
    game_world.add_object(server.ai_court, 0)
    game_world.add_collision_pair('ai_court:ball', server.ai_court, None)

    server.player_court_out = Player_Court_Out()
    game_world.add_object(server.player_court_out, 0)
    game_world.add_collision_pair('player_court_out:ball', server.player_court_out, None)

    server.ai_court_out = AI_Court_Out()
    game_world.add_object(server.ai_court_out, 0)
    game_world.add_collision_pair('ai_court_out:ball', server.ai_court_out, None)

    server.net = Net()
    game_world.add_object(server.net, 0)
    game_world.add_collision_pair('net:ball', server.net, None)

    server.player = Player()
    game_world.add_object(server.player, 2)
    game_world.add_collision_pair('player:ball', server.player, None)

    server.setter = Setter(488, 85, 1, 'player')
    game_world.add_object(server.setter, 1)
    game_world.add_collision_pair('setter:ball', server.setter, None)

    server.blocker1 = Blocker(470, 85, 1)
    game_world.add_object(server.blocker1, 2)
    server.blocker2 = Blocker(455, 85, 1)
    game_world.add_object(server.blocker2, 3)
    game_world.add_collision_pair('blocker:ball', server.blocker1, None)
    game_world.add_collision_pair('blocker:ball', server.blocker2, None)

    server.spiker = Spiker()
    game_world.add_object(server.spiker, 2)
    game_world.add_collision_pair('spiker:ball', server.spiker, None)

    server.enemy_setter = Setter(518, 85, -1, 'ai')
    game_world.add_object(server.enemy_setter, 1)
    game_world.add_collision_pair('setter:ball', server.enemy_setter, None)

    server.enemy_blocker1 = Enemy_Blocker(536, 85, -1)
    game_world.add_object(server.enemy_blocker1, 2)
    server.enemy_blocker2 = Enemy_Blocker(551, 85, -1)
    game_world.add_object(server.enemy_blocker2, 3)
    game_world.add_collision_pair('enemy_blocker:ball', server.enemy_blocker1, None)
    game_world.add_collision_pair('enemy_blocker:ball', server.enemy_blocker2, None)

    server.ball = Ball(server.player.x+10, server.player.y+10, 0, 0, 0)
    game_world.add_object(server.ball, 2)
    game_world.add_collision_pair('player:ball', None, server.ball)
    game_world.add_collision_pair('setter:ball', None, server.ball)
    game_world.add_collision_pair('blocker:ball', None, server.ball)
    game_world.add_collision_pair('spiker:ball', None, server.ball)
    game_world.add_collision_pair('enemy_blocker:ball', None, server.ball)

    game_world.add_collision_pair('player_court:ball', None, server.ball)
    game_world.add_collision_pair('ai_court:ball', None, server.ball)
    game_world.add_collision_pair('player_court_out:ball', None, server.ball)
    game_world.add_collision_pair('ai_court_out:ball', None, server.ball)
    game_world.add_collision_pair('net:ball', None, server.ball)

    server.timer = Timer()
    game_world.add_object(server.timer, 3)

    server.score = Score()
    game_world.add_object(server.score, 3)

    server.judge = Judge()
    game_world.add_object(server.judge, 3)

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