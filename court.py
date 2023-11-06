from pico2d import load_image


class Court:
    def __init__(self):
        self.image = load_image('court.png')
        self.net_image = load_image('net.png')

    def draw(self):
        self.image.draw(500, 300)
        self.net_image.draw(500, 230)