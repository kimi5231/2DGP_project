from pico2d import load_image, clear_canvas, update_canvas, get_events, load_music, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import match_mode


def init():
    global image
    global bgm
    global start_time

    image = load_image('win.png')
    bgm = load_music('win_music.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()
    start_time = get_time()

def finish():
    global image
    global bgm
    del image
    del bgm


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            bgm.stop()
            game_framework.change_mode(match_mode)


def update():
    if get_time() - start_time >= 11.0:
        bgm.stop()
        game_framework.change_mode(match_mode)


def draw():
    clear_canvas()
    image.draw(300, 300, 600, 600)
    update_canvas()


def pause():
    pass


def resume():
    pass