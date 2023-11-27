from pico2d import load_image

import game_framework


# judge action speed
TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Judge:
    def __init__(self):
        self.x, self.y = 300, 300
        self.frame = 0
        self. action = 0
        self.frame_len = 300
        self.action_len = 200
        self.frame_num = 3
        self.state = 'draw'
        self.team = 'player'
        self.image = load_image('judge.png')

    def draw(self):
        if self.state == 'draw':
            if self.team == 'player':
                self.image.clip_draw(int(self.frame) * self.frame_len,
                                           self.action * self.action_len,
                                            self.frame_len, self.action_len, self.x - 50, self.y - 50,
                                            200, 100)
            else:
                self.image.clip_composite_draw(int(self.frame) * self.frame_len,
                                               self.action * self.action_len,
                                               self.frame_len, self.action_len, 0, 'h', self.x + 50, self.y - 50,
                                               200, 100)

    def update(self):
        if int(self.frame) == 2:
            self.state = 'hide'
        self.frame = ((self.frame + self.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % self.frame_num)