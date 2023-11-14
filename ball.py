from pico2d import load_image


class Ball:
    def __init__(self, x, y, dir, speed):
        self.x, self.y, self.dir, self.speed = x, y, dir, speed
        self.image = load_image('ball.png')