from pico2d import load_image, draw_rectangle, get_time

import random
import game_framework
import server
from behavior_tree import BehaviorTree, Action, Condition, Sequence, Selector

# setter toss speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
TOSS_SPEED_KMPH = 20.0 # Km / Hour
TOSS_SPEED_MPM = (TOSS_SPEED_KMPH * 1000.0 / 60.0)
TOSS_SPEED_MPS = (TOSS_SPEED_MPM / 60.0)
TOSS_SPEED_PPS = (TOSS_SPEED_MPS * PIXEL_PER_METER)

# setter feint speed
FEINT_SPEED_KMPH = 10.0 # Km / Hour
FEINT_SPEED_MPM = (FEINT_SPEED_KMPH * 1000.0 / 60.0)
FEINT_SPEED_MPS = (FEINT_SPEED_MPM / 60.0)
FEINT_SPEED_PPS = (FEINT_SPEED_MPS * PIXEL_PER_METER)

# setter action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Enemy_Setter:
    def __init__(self, x, y, dir):
        self.x, self.y, self.dir = x, y, dir
        self.frame = 0
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        self.action_len = 110
        self.image_110 = load_image('setter_h110.png')
        self.image_180 = load_image('setter_h180.png')
        self.build_behavior_tree()
        self.state = 'Idle'
        self.receive_success = False

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom

        if self.action_len == 110:
            self.image_110.clip_composite_draw(int(self.frame) * self.frame_len,
                                               self.action * self.action_len,
                                               self.frame_len, self.action_len, 0, 'h', sx, sy, 33, 66)
        elif self.action_len == 180:
            self.image_180.clip_composite_draw(int(self.frame) * self.frame_len,
                                     self.action * self.action_len,
                                     self.frame_len, self.action_len, 0, 'h', sx, sy + 20, 36, 86)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = ((self.frame + self.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                      % self.frame_num)
        self.bt.run()

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom

        if self.state == 'toss wait' or self.state == 'toss ready' or self.state == 'feint wait':
            return sx - 10, sy + 10, sx + 10, sy + 20
        else:
            return 0, 0, 0, 0

    def handle_collision(self, group, other):
        if group == 'setter:ball':
            if self.state == 'toss wait' or self.state == 'toss ready':
                num = random.randint(1, 5)
                if num == 1:
                    server.enemy_blocker1.state = 'time difference attack'
                elif num == 2:
                    server.enemy_blocker2.state = 'time difference attack'
                else:
                    server.spiker.state = 'attack ready'
                self.action = 3
                self.frame_num = 3
                self.frame_len = 60
                self.action_len = 110
                self.state = 'toss hit'
                server.ball.speed_y = TOSS_SPEED_PPS
                server.ball.speed_x = 0
                server.ball.dir = 0
                server.ball.start_time = get_time()
            elif self.state == 'feint wait':
                self.action = 0
                self.frame_num = 9
                self.frame_len = 60
                self.action_len = 180
                self.state = 'feint hit'
                server.ball.speed_y = -FEINT_SPEED_PPS
                server.ball.speed_x = FEINT_SPEED_PPS
                server.ball.x -= 20
                server.ball.y = 180
                server.ball.dir = -1
                server.ball.start_time = get_time()

    def is_cur_state_Idle(self):
        if self.state == 'Idle':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def Idle(self):
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        self.action_len = 110
        return BehaviorTree.RUNNING

    def is_receive_success(self):
        if self.receive_success:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def toss_ready(self):
        self.action = 1
        self.frame_num = 7
        self.frame_len = 60
        self.action_len = 110
        if int(self.frame) == 6:
            num = random.randint(1, 5)
            if num == 1:
                self.state = 'feint wait'
            else:
                self.state = 'toss wait'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_cur_state_toss_wait(self):
        if self.state == 'toss wait':
            self.receive_success = False
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def toss_wait(self):
        self.action = 2
        self.frame_num = 1
        self.frame_len = 60
        self.action_len = 110
        return BehaviorTree.RUNNING

    def is_cur_state_toss_hit(self):
        if self.state == 'toss hit':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def toss_hit(self):
        self.action = 3
        self.frame_num = 4
        self.frame_len = 60
        self.action_len = 110
        if int(self.frame) == 3:
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_cur_state_feint_wait(self):
        if self.state == 'feint wait':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def feint_wait(self):
        self.action = 2
        self.frame_num = 1
        self.frame_len = 60
        self.action_len = 110
        return BehaviorTree.RUNNING

    def is_cur_state_feint_hit(self):
        if self.state == 'feint hit':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def feint_hit(self):
        self.action = 0
        self.frame_num = 9
        self.frame_len = 60
        self.action_len = 180
        if int(self.frame) == 8:
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('현재 상태가 Idle 인가?', self.is_cur_state_Idle)
        a1 = Action('Idle', self.Idle)

        SEQ_keep_Idle_state = Sequence('Idle 상태 유지', c1, a1)

        c2 = Condition('리시브가 성공했는가?', self.is_receive_success)
        a2 = Action('toss ready', self.toss_ready)

        SEQ_change_toss_ready_state = Sequence('toss ready 상태로 변경', c2, a2)

        c3 = Condition('현재 상태가 toss wait 인가?', self.is_cur_state_toss_wait)
        a3 = Action('toss wait', self.toss_wait)

        SEQ_keep_toss_wait_state = Sequence('toss wait 상태 유지', c3, a3)

        c4 = Condition('현재 상태가 toss hit 인가?', self.is_cur_state_toss_hit)
        a4 = Action('toss hit', self.toss_hit)

        SEQ_chang_toss_hit_state = Sequence('toss hit 상태로 변경', c4, a4)

        SEL_toss = Selector('toss', SEQ_chang_toss_hit_state, SEQ_keep_toss_wait_state,
                                                SEQ_change_toss_ready_state)

        c5 = Condition('현재 상태가 feint wait 인가?', self.is_cur_state_feint_wait)
        a5 = Action('feint wait', self.feint_wait)

        SEQ_keep_feint_wait_state = Sequence('feint wait 상태 유지', c5, a5)

        c6 = Condition('현재 상태가 feint hit 인가?', self.is_cur_state_feint_hit)
        a6 = Action('feint hit', self.feint_hit)

        SEQ_chang_feint_hit_state = Sequence('feint hit 상태로 변경', c6, a6)

        SEL_feint = Selector('feint', SEQ_chang_feint_hit_state, SEQ_keep_feint_wait_state)

        root = SEL_feint_toss_or_Idle = Selector('feint or toss or Idle',
                                                 SEL_feint, SEL_toss, SEQ_keep_Idle_state)

        self.bt = BehaviorTree(root)