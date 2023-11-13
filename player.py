from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP

MOVE_W = 50
MOVE_H = 100
DRIVE_W = 70
DRIVE_H = 110

class Player:
    def __init__(self):
        self.x = 300
        self.y = 105
        self.dir = 0
        self.speed = 10
        self.frame = 0
        self.action = 0
        self.frame_num = 5
        self.frame_len = MOVE_W
        self.action_len = MOVE_H
        self.image = load_image('player.png')

    def draw(self):
        self.image.clip_draw(self.frame * self.frame_len,
                             self.action * self.action_len,
                             self.frame_len, self.action_len, self.x, self.y)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir = 1
            elif event.key == SDLK_LEFT:
                self.dir = -1
        elif event.type == SDL_KEYUP:
            self.dir = 0
            self.frame = 0

    def move(self):
        self.x += self.dir * self.speed
        self.frame = (self.frame + 1) % self.frame_num