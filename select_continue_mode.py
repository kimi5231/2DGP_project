from pico2d import load_image, load_font, clear_canvas, update_canvas, get_events, get_time, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode
import server
import title_mode


def init():
    global image
    global font
    global sec
    global start_time

    image = load_image('select_continue.png')
    font = load_font('ENCR10B.TTF')
    sec = 9
    start_time = get_time()


def finish():
    global image
    global font
    del image
    del font


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            server.lose_bgm.stop()
            game_framework.change_mode(play_mode)


def update():
    global sec
    global start_time

    if sec == 0:
        server.stage = 1
        server.lose_bgm.stop()
        game_framework.change_mode(title_mode)
    if get_time() - start_time >= 1.0:
        sec -= 1
        start_time = get_time()


def draw():
    clear_canvas()
    image.draw(300, 300, 600, 600)
    font.draw(200, 100, 'Continue Play?', (255, 255, 255))
    font.draw(400, 100, f'{sec}', (255, 255, 255))
    update_canvas()


def pause():
    pass


def resume():
    pass