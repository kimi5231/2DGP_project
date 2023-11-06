from pico2d import load_image


class Court:
    def __init__(self):
        self.image = load_image('court.png')
        self.net_image = load_image('net.png')

    def draw(self):
        pass