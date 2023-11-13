from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_SPACE

PLAYER_H = 110
MOVE_W = 50
MOVE_N = 5
DRIVE_W = 70
DRIVE_READY_N = 4
DRIVE_WAIT_N = 1
DRIVE_HIT_N = 3


class Player:
    def __init__(self):
        self.x = 300
        self.y = 105
        self.dir = 0
        self.speed = 10
        self.frame = 0
        self.action = 0
        self.frame_num = MOVE_N
        self.frame_len = MOVE_W
        self.action_len = PLAYER_H
        self.image = load_image('player.png')

    def draw(self):
        self.frame = (self.frame + 1) % self.frame_num
        self.image.clip_draw(self.frame * self.frame_len,
                             self.action * self.action_len,
                             self.frame_len, self.action_len, self.x, self.y)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.action = 0
                self.frame_num = MOVE_N
                self.frame_len = MOVE_W
                self.dir = 1
            elif event.key == SDLK_LEFT:
                self.action = 0
                self.frame_num = MOVE_N
                self.frame_len = MOVE_W
                self.dir = -1
            elif event.key == SDLK_SPACE:
                self.action = 2
                self.frame_num = DRIVE_WAIT_N
                self.frame_len = DRIVE_W
        elif event.type == SDL_KEYUP:
            self.dir = 0
            self.frame = 0

    def move(self):
        self.x += self.dir * self.speed

    def drive_serve(self):
        pass