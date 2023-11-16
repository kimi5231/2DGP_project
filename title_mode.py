from pico2d import load_image, clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework


def init():
    global image
    image = load_image('title.png')


def finish():
    global image
    del image


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def update():
    pass

def draw():
    clear_canvas()
    image.draw(500, 300, 1000, 600)
    update_canvas()


def pause():
    pass


def resume():
    pass
