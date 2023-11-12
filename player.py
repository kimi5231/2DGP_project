from pico2d import load_image


class Player:
    def __init__(self):
        self.image = load_image('move.png')

    def draw(self):
        self.image.draw(500, 300)