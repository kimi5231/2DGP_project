from pico2d import *

import game_world
from court import Court
from player import Player


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)


def create_world():
    global running
    global court
    global player

    running = True

    court = Court()
    game_world.add_object(court, 0)

    player = Player()
    game_world.add_object(player, 1)


def update():
    clear_canvas()
    court.draw()
    player.draw()
    update_canvas()


open_canvas(1000, 600)

while running:
    update()
    player.update()
    handle_events()
    delay(0.05)

close_canvas()