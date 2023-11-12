from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP


class Player:
    def __init__(self):
        self.x = 300
        self.y = 100
        self.dir = 1
        self.speed = 10
        self.frame = 0
        self.image = load_image('move.png')

    def draw(self):
        self.image.clip_draw(self.frame * 50, 0, 50, 100, self.x, self.y)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir = 1
                self.x += self.dir * self.speed
                self.frame = (self.frame + 1) % 5
            elif event.key == SDLK_LEFT:
                self.dir = -1
                self.x += self.dir * self.speed
                self.frame = (self.frame + 1) % 5
        # elif event.type == SDL_KEYUP:
        #    self.frame = 0