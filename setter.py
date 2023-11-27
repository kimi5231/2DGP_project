from pico2d import load_image

import game_framework
import game_world
import play_mode
import server
from behavior_tree import BehaviorTree, Action, Condition, Sequence, Selector

# setter toss speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
TOSS_SPEED_KMPH = 10.0 # Km / Hour
TOSS_SPEED_MPM = (TOSS_SPEED_KMPH * 1000.0 / 60.0)
TOSS_SPEED_MPS = (TOSS_SPEED_MPM / 60.0)
TOSS_SPEED_PPS = (TOSS_SPEED_MPS * PIXEL_PER_METER)

# setter action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Setter:
    def __init__(self, x, y, dir, team):
        self.x, self.y, self.dir, self.team = x, y, dir, team
        self.frame = 0
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        self.action_len = 110
        self.image = load_image('setter.png')
        self.build_behavior_tree()
        self.state = 'Idle'

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * self.frame_len,
                                       self.action * self.action_len,
                                        self.frame_len, self.action_len, sx, sy, 33, 66)
        else:
            self.image.clip_composite_draw(int(self.frame) * self.frame_len,
                                           self.action * self.action_len,
                                           self.frame_len, self.action_len, 0, 'h', sx, sy, 33, 66)

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
            self.action = 3
            self.frame_num = 3
            self.frame_len = 60
            self.state = 'Idle'
            server.ball.speed_y = TOSS_SPEED_PPS
            server.ball.speed_x = 0
            server.ball.dir = 0

    def is_cur_state_Idle(self):
        if self.state == 'Idle':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def Idle(self):
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        return BehaviorTree.RUNNING

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def is_ball_nearby(self, distance):
        if (self.distance_less_than(server.ball.x, server.ball.y, self.x, self.y, distance)
                and server.ball.y > self.y and server.score.turn == self.team):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def toss_ready(self):
        self.action = 1
        self.frame_num = 7
        self.frame_len = 60
        self.state = 'toss ready'
        if int(self.frame) == 6:
            self.state = 'toss wait'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_cur_state_toss_wait(self):
        if self.state == 'toss wait':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def toss_wait(self):
        self.action = 2
        self.frame_num = 1
        self.frame_len = 60
        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('현재 상태가 Idle 인가?', self.is_cur_state_Idle)
        a1 = Action('Idle', self.Idle)

        SEQ_keep_Idle_state = Sequence('Idle 상태 유지', c1, a1)

        c2 = Condition('공이 근처에 있는가?', self.is_ball_nearby, 7)
        a2 = Action('toss ready', self.toss_ready)

        SEQ_change_toss_ready_state = Sequence('toss ready 상태로 변경', c2, a2)

        c3 = Condition('현재 상태가 toss wait 인가?', self.is_cur_state_toss_wait)
        a3 = Action('toss wait', self.toss_wait)

        SEQ_keep_toss_wait_state = Sequence('toss wait 상태 유지', c3, a3)

        root = SEL_toss_wait_or_toss_ready_or_Idle = Selector('toss wait or toss ready or Idle',
                                                              SEQ_keep_toss_wait_state,
                                                              SEQ_change_toss_ready_state,
                                                              SEQ_keep_Idle_state)

        self.bt = BehaviorTree(root)