from pico2d import load_image

import server


# setter action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Setter:
    def __init__(self):
        self.x = 450
        self.y = 85
        self.frame = 0
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        self.action_len = 110
        self.image = load_image('setter.png')

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * self.frame_len,
                                   self.action * self.action_len,
                                   self.frame_len, self.action_len, sx, sy, 33, 66)


    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom

        return sx - 25, sy - 55, sx + 25, sy + 55

    def handle_collision(self, group, other):
        if group == 'setter:ball':
            pass

    