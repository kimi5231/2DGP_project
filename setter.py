from pico2d import load_image

import game_framework
import play_mode
import server
from behavior_tree import BehaviorTree, Action, Condition, Sequence

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm

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
        self.build_behavior_tree()

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * self.frame_len,
                                   self.action * self.action_len,
                                   self.frame_len, self.action_len, sx, sy, 33, 66)


    def update(self):
        self.frame = ((self.frame + self.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % self.frame_num)
        self.bt.run()

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom

        return sx - 25, sy - 55, sx + 25, sy + 55

    def handle_collision(self, group, other):
        if group == 'setter:ball':
            pass

    def distance_less_than(self, y1, y2, r):
        distance2 = y1 - y2
        return (PIXEL_PER_METER * distance2) < (PIXEL_PER_METER * r)

    def is_ball_over(self, distance):
        if self.distance_less_than(server.ball.y, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def toss(self):
        self.action = 1
        self.frame_num = 10
        self.frame_len = 60

    def build_behavior_tree(self):
        c1 = Condition('공이 근처에 있는가?', self.is_ball_over, 7)
        a1 = Action('토스', self.toss)

        root = SEQ_toss_ball = Sequence('공을 토스', c1, a1)

        self.bt = BehaviorTree(root)