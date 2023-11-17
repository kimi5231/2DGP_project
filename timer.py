from pico2d import load_font, get_time


class Timer:
    def __init__(self):
        self.sec = 180
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.font.draw(100, 100, 'Timer', (255, 255, 255))
        self.font.draw(100, 90, f'{int((180-get_time())//60)} : {int((180-get_time())%60)}', (255, 255, 255))

    def update(self):
        pass