from pico2d import *

import game_framework
import game_world
from court import Court
from player import Player
from timer import Timer


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)


def init():
    global running
    global court
    global player

    running = True

    court = Court()
    game_world.add_object(court, 0)

    player = Player()
    game_world.add_object(player, 1)

    timer = Timer()
    game_world.add_object(timer, 1)


def finish():
    game_world.clear()


def update():
    game_world.update()
    delay(0.05)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass