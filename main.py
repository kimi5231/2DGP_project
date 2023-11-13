from pico2d import *
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


def update():
    clear_canvas()
    court.draw()
    player.draw()
    update_canvas()


open_canvas(1000, 600)
running = True
court = Court()
player = Player()

while running:
    update()
    player.move()
    handle_events()
    delay(0.05)

close_canvas()