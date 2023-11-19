from pico2d import load_image, load_font, clear_canvas, update_canvas, get_events, delay
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
import play_mode


def init():
    global image_J
    global image_C
    global font
    global Jx, Jy, Cx, Cy, Fx, Fy

    image_J = load_image('Japan.jpg')
    image_C = load_image('Cuba.jpg')
    font = load_font('ENCR10B.TTF', 30)
    Jx, Jy = -100, 400
    Cx, Cy = 700, 400
    Fx, Fy = 300, -100


def finish():
    global image_J
    global image_C
    global font

    del image_J
    del image_C
    del font


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def update():
    global Jx, Jy, Cx, Cy, Fx, Fy
    if Jx < 150 and Cx > 450:
        Jx += 10
        Cx -= 10
    if Fy < 400:
        Fy += 10
    if Jx >= 150 and Cx <= 450 and Fy >= 400:
        delay(1.0)
        game_framework.change_mode(play_mode)
    delay(0.01)


def draw():
    clear_canvas()
    image_J.draw(Jx, Jy, 200, 100)
    image_C.draw(Cx, Cy, 200, 100)
    font.draw(Jx, Jy-100, 'JAPAN', (255, 255, 255))
    font.draw(Cx, Cy-100, 'CUBA', (255, 255, 255))
    font.draw(Fx, Fy, 'VS', (255, 255, 255))
    update_canvas()


def pause():
    pass


def resume():
    pass