from pico2d import load_image, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import game_world

# ball gravity speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
Gravity_SPEED_KMPH = 36.0 # Km / Hour
Gravity_SPEED_MPM = (Gravity_SPEED_KMPH * 1000.0 / 60.0)
Gravity_SPEED_MPS = (Gravity_SPEED_MPM / 60.0)
Gravity_SPEED_PPS = (Gravity_SPEED_MPS * PIXEL_PER_METER)


class Ball:
    def __init__(self, x, y, dir, speed_x, speed_y):
        self.x, self.y, self.dir, self.speed_x, self.speed_y = x, y, dir, speed_x, speed_y
        self.image = load_image('ball.png')

    def draw(self):
        self.image.draw(self.x, self.y, 22, 22)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 11, self.y - 11, self.x + 11, self.y + 11

    def handle_collision(self, group, other):
        if group == 'player:ball':
            self.dir = 1
        elif group == 'setter:ball':
            self.dir = 0
        elif group == 'blocker:ball':
            self.dir = 1
        elif group == 'spiker:ball':
            self.dir = -1
        elif group == 'enemy_blocker:ball':
            self.dir = -1