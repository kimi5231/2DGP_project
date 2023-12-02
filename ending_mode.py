from pico2d import load_image, load_font, clear_canvas, update_canvas, get_events, get_time, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
import title_mode


def init():
    global image1, image2
    global font
    global bgm
    global start_time

    image1 = load_image('ending1.png')
    image2 = load_image('ending2.png')
    font = load_font('ENCR10B.TTF')
    start_time = get_time()
    bgm = load_music('win_music.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()


def finish():
    global image1
    global image2
    global font
    global bgm
    del image1
    del image2
    del font
    del bgm


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def update():
    global start_time

    if get_time() - start_time >= 11.0:
        bgm.stop()
        game_framework.change_mode(title_mode)


def draw():
    clear_canvas()
    if get_time() - start_time >= 5:
        image2.draw(300, 300, 600, 600)
        font.draw(150, 150, 'YOU GOT THE GOLD MEDAL!!!', (255, 255, 255))
    else:
        image1.draw(300, 300, 600, 600)
        font.draw(200, 150, 'CONGRATULATION!!!', (255, 255, 255))
    update_canvas()


def pause():
    pass


def resume():
    pass