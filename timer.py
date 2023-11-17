from pico2d import load_font, get_time


class Timer:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.font.draw(100, 100, f'(Time: {get_time()})', (255, 255, 255))

    def update(self):
        pass