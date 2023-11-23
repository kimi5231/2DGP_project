from pico2d import load_image


class Court:
    def __init__(self):
        self.image = load_image('background.png')
        self.court_image = load_image('court.png')
        self.net_image = load_image('net.png')

    def draw(self):
        self.image.draw(500, 300, 1000, 600)
        self.court_image.draw(500, 51, 600, 10)
        self.net_image.draw(500, 130, 30, 150)

    def update(self):
        pass