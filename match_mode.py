from pico2d import load_image, load_font, clear_canvas, update_canvas, get_events, delay, load_music, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
import play_mode
import server


def init():
    global image_Korea, image_ai, image_background
    global font
    global Korea_x, Korea_y
    global ai_x, ai_y
    global font_x, font_y
    global bgm
    global start_time

    image_background = load_image('match_background.jpg')
    font = load_font('ENCR10B.TTF', 30)
    Korea_x, Korea_y = -500, 400
    ai_x, ai_y = 1100, 400
    font_x, font_y = 280, -500

    image_Korea = load_image('Korea.png')
    if server.stage == 1:
        image_ai = load_image('Cuba.png')
    elif server.stage == 2:
        image_ai = load_image('China.png')
    elif server.stage == 3:
        image_ai = load_image('Japan.png')
    elif server.stage == 4:
        image_ai = load_image('URS.png')
    elif server.stage == 5:
        image_ai = load_image('USA.png')

    bgm = load_music('match_music.mp3')
    bgm.set_volume(32)
    bgm.play(1)

    start_time = get_time()

def finish():
    global image_Korea, image_ai, image_background
    global font
    global bgm

    del image_Korea
    del image_ai
    del image_background
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
    global Korea_x, Korea_y, ai_x, ai_y, font_x, font_y

    if Korea_x < 150 and ai_x > 450:
        Korea_x += 5
        ai_x -= 5
    if font_y < 400:
        font_y += 5
    if Korea_x >= 150 and ai_x <= 450 and font_y >= 400:
        if get_time() - start_time >= 11.0:
            bgm.stop()
            game_framework.change_mode(play_mode)
    delay(0.01)


def draw():
    clear_canvas()
    image_background.draw(300, 300, 600, 600)
    image_Korea.draw(Korea_x, Korea_y, 200, 100)
    font.draw(Korea_x - 50, Korea_y - 100, 'Korea', (255, 255, 255))
    image_ai.draw(ai_x, ai_y, 200, 100)
    if server.stage == 1:
        font.draw(ai_x - 40, ai_y - 100, 'CUBA', (255, 255, 255))
    elif server.stage == 2:
        font.draw(ai_x - 50, ai_y - 100, 'China', (255, 255, 255))
    elif server.stage == 3:
        font.draw(ai_x - 50, ai_y - 100, 'Japan', (255, 255, 255))
    elif server.stage == 4:
        font.draw(ai_x - 30, ai_y - 100, 'URS', (255, 255, 255))
    elif server.stage == 5:
        font.draw(ai_x - 30, ai_y - 100, 'USA', (255, 255, 255))
    font.draw(font_x, font_y, 'VS', (255, 255, 255))
    update_canvas()


def pause():
    pass


def resume():
    pass