from pico2d import load_font

import server


class Score:
    def __init__(self):
        self.player_score = 0
        self.ai_score = 0
        self.turn = 'player'
        self.font = load_font('ENCR10B.TTF', 30)

    def draw(self):
        self.font.draw(260, 550, f'{self.player_score} : {self.ai_score}', (255, 255, 255))

    def update(self):
        self.end_set()

    def update_score(self):
        if self.turn == 'player':
            self.player_score += 1
        elif self.turn == 'ai':
            self.ai_score += 1

    def end_set(self):
        if self.player_score >= 15 and self.player_score - self.ai_score >= 2:
            server.stage += 1
        elif self.ai_score >= 15 and self.ai_score - self.player_score >= 2:
            pass