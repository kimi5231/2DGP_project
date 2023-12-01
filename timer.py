from pico2d import load_font, get_time

import server


class Timer:
    def __init__(self):
        self.sec = 150
        self.font = load_font('ENCR10B.TTF', 16)
        self.start_time = get_time()

    def draw(self):
        self.font.draw(400, 530, 'Timer', (255, 255, 255))
        self.font.draw(395, 515, f'{int(self.sec//60)} : {int(self.sec%60)}', (255, 255, 255))

    def update(self):
        if self.sec == 0:
            server.score.time_over()
        if get_time() - self.start_time >= 1.0 and self.sec > 0:
            self.sec -= 1
            self.start_time = get_time()