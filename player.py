from pico2d import load_image


class Player:
    def __init__(self):
        self.x = 300
        self.y = 100
        self.frame = 0
        self.image = load_image('move.png')

    def draw(self):
        self.image.clip_draw(self.frame * 50, 0, 50, 100, self.x, self.y)