from pico2d import load_image


class Ball:
    def __init__(self, x, y, dirX, dirY, speed):
        self.x, self.y, self.dirX, self.dirY, self.speed = x, y, dirX, dirY, speed
        self.image = load_image('ball.png')

    def draw(self):
        self.image.draw(self.x, self.y, 30, 30)

    def update(self):
        self.x += self.dirX * self.speed
        self.y += self.dirY * self.speed