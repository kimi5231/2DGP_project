from pico2d import load_image, load_font, clear_canvas, update_canvas, get_events, delay
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
import title_mode


def init():
    global image

    image = load_image('lose.jpg')


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
    delay(1.0)
    game_framework.change_mode(title_mode)


def draw():
    clear_canvas()
    image.draw(300, 300, 600, 600)
    update_canvas()


def pause():
    pass


def resume():
    pass