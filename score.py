from pico2d import load_font


class Score:
    def __init__(self):
        self.player_score = 0
        self.ai_score = 0
        self.font = load_font('ENCR10B.TTF', 30)

    def draw(self):
        self.font.draw(260, 550, f'{self.player_score} : {self.ai_score}', (255, 255, 255))

    def update(self):
        pass