from pico2d import load_font

import game_framework
import lose_mode
import server


class Score:
    def __init__(self):
        if server.stage == 1:
            self.player_score, self.ai_score = 11, 11
        elif server.stage == 2:
            self.player_score, self.ai_score = 10, 11
        elif server.stage == 3:
            self.player_score, self.ai_score = 9, 11
        elif server.stage == 4:
            self.player_score, self.ai_score = 8, 11
        elif server.stage == 5:
            self.player_score, self.ai_score = 8, 9
        self.turn = 'player'
        self.font = load_font('ENCR10B.TTF', 30)

    def draw(self):
        self.font.draw(260, 550, f'{self.player_score} : {self.ai_score}', (255, 255, 255))

    def update(self):
        if self.player_score >= 15 and self.player_score - self.ai_score >= 2:
            server.stage += 1
        elif self.ai_score >= 15 and self.ai_score - self.player_score >= 2:
            game_framework.change_mode(lose_mode)