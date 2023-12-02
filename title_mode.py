from pico2d import load_image, clear_canvas, update_canvas, get_events, load_font, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import match_mode


def init():
    global image
    global font
    global bgm
    image = load_image('title.png')
    font = load_font('ENCR10B.TTF', 30)
    bgm = load_music('title_music.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

def finish():
    global image
    global font
    global bgm
    del image
    del font
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
    pass

def draw():
    clear_canvas()
    image.draw(300, 300, 600, 600)
    font.draw(200, 200, 'Push Space', (255, 255, 255))
    update_canvas()


def pause():
    pass


def resume():
    pass