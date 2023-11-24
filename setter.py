from pico2d import load_image

import game_framework
import game_world
import play_mode
import server
from behavior_tree import BehaviorTree, Action, Condition, Sequence, Selector

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
        self.end_ready = False
        self.change_idle = False

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * self.frame_len,
                                   self.action * self.action_len,
                                   self.frame_len, self.action_len, sx, sy, 33, 66)


    def update(self):
        self.frame = ((self.frame + self.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % self.frame_num)
        if int(self.frame) == 3:
            self.change_idle = True
        self.bt.run()

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom

        return sx - 25, sy - 55, sx + 25, sy + 55

    def handle_collision(self, group, other):
        if group == 'setter:ball':
            self.action = 3
            self.frame_num = 3
            self.end_ready = False

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def is_ball_over(self, distance):
        if self.distance_less_than(server.ball.x, server.ball.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def toss_ready(self):
        self.action = 1
        self.frame_num = 7
        self.frame_len = 60
        if int(self.frame) == 6:
            self.end_ready = True
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_end_toss_ready(self):
        if self.end_ready:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def toss_wait(self):
        self.action = 2
        self.frame_num = 1
        return BehaviorTree.RUNNING

    def is_back_idle(self):
        if self.change_idle:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def idle(self):
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('공이 근처에 있는가?', self.is_ball_over, 7)
        a1 = Action('토스 준비', self.toss_ready)

        SEQ_ready_toss_ball = Sequence('공을 토스하기 위해 준비', c1, a1)

        c2 = Condition('토스할 준비가 끝났는가?', self.is_end_toss_ready)
        a2 = Action('토스 대기', self.toss_wait)

        SEQ_wait_toss_ball = Sequence('공을 토스하기 위해 대기', c2, a2)

        c3 = Condition('idle 상태로 돌아가야 하는가?', self.is_back_idle)
        a3 = Action('idle', self.idle)

        SEQ_change_idle = Sequence('idle 상태로 변경', c3, a3)

        root = SEL_ready_or_wait_toss_ball = Selector('idle 또는 공을 토스하기 위해 준비 또는 공을 토스하기 위해 대기',
                                                      SEQ_change_idle, SEQ_wait_toss_ball,
                                                      SEQ_ready_toss_ball)

        self.bt = BehaviorTree(root)