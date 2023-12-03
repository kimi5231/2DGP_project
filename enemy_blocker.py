from pico2d import load_image, get_time, draw_rectangle

import game_framework
import server
from behavior_tree import BehaviorTree, Condition, Action, Sequence, Selector
from player import TimeDifferenceAttackBlockerReady, AttackReady

# blocker move speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
MOVE_SPEED_KMPH = 10.0 # Km / Hour
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

# blocker blocking speed
BLOCKING_SPEED_KMPH = 10.0 # Km / Hour
BLOCKING_SPEED_MPM = (BLOCKING_SPEED_KMPH * 1000.0 / 60.0)
BLOCKING_SPEED_MPS = (BLOCKING_SPEED_MPM / 60.0)
BLOCKING_SPEED_PPS = (BLOCKING_SPEED_MPS * PIXEL_PER_METER)

# blocker action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Enemy_Blocker:
    def __init__(self, x, y, dir):
        self.x, self.y, self.dir = x, y, dir
        self.original_x = x
        self.frame = 0
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        self.action_len = 110
        self.image_110 = load_image('blocker_h110.png')
        self.image_180 = load_image('blocker_h180.png')
        self.image_210 = load_image('blocker_h210.png')
        self.build_behavior_tree()
        self.state = 'Idle'

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
        else:
            self.image_210.clip_composite_draw(int(self.frame) * self.frame_len,
                                               self.action * self.action_len,
                                               self.frame_len, self.action_len, 0, 'h', sx, sy + 20, 50, 100)
        #draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = ((self.frame + self.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % self.frame_num)
        self.bt.run()

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom

        if self.state == 'blocking hit':
            return sx - 10, sy + 50, sx, sy + 70
        else:
            return 0, 0, 0, 0

    def handle_collision(self, group, other):
        if group == 'enemy_blocker:ball':
            if self.state == 'blocking hit':
                server.ball.speed_x = BLOCKING_SPEED_PPS
                server.ball.speed_y = BLOCKING_SPEED_PPS // 2
                server.score.turn = 'ai'
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

    def is_enemy_setter_toss_wait(self):
        if server.setter.state == 'toss wait':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def is_move_to_net(self, r=0.5):
        if self.distance_less_than(server.background.net_x, server.background.net_y, self.x, self.y, r):
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def move_to_net(self, r=0.5):
        self.action = 1
        self.frame_num = 5
        self.frame_len = 50
        self.action_len = 110
        self.x += self.dir * MOVE_SPEED_PPS * game_framework.frame_time
        if self.distance_less_than(server.background.net_x, server.background.net_y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def blocking_ready(self):
        self.action = 2
        self.frame_num = 2
        self.frame_len = 50
        self.action_len = 110
        self.state = 'blocking ready'
        if int(self.frame) == 1:
            self.state = 'blocking wait'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_cur_state_blocking_wait(self):
        if self.state == 'blocking wait':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def blocking_wait(self):
        self.action = 3
        self.frame_num = 1
        self.frame_len = 50
        self.action_len = 110
        return BehaviorTree.RUNNING

    def is_enemy_spiker_ready(self):
        if server.player.state_machine.cur_state == AttackReady or server.player.state_machine.cur_state == TimeDifferenceAttackBlockerReady:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def blocking_hit(self):
        self.action = 0
        self.frame_num = 7
        self.frame_len = 60
        self.action_len = 180
        self.state = 'blocking hit'
        if int(self.frame) == 6:
            self.state = 'come back'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_cur_state_come_back(self):
        if self.state == 'come back':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def come_back(self):
        self.action = 1
        self.frame_num = 5
        self.frame_len = 50
        self.action_len = 110
        self.x += self.dir * -1 * MOVE_SPEED_PPS * game_framework.frame_time
        if self.x >= self.original_x:
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_cur_state_time_difference_attack(self):
        if self.state == 'time difference attack':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def time_difference_attack(self):
        self.action = 0
        self.frame_num = 12
        self.frame_len = 80
        self.action_len = 210
        if self.x >= server.net.x + 10:
            self.x += self.dir * MOVE_SPEED_PPS * game_framework.frame_time
        if int(self.frame) == 11:
            self.state = 'come back'
            server.spiker.state = 'attack ready'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('현재 상태가 Idle 인가?', self.is_cur_state_Idle)
        a1 = Action('Idle', self.Idle)

        SEQ_keep_Idle_state = Sequence('Idle 상태 유지', c1, a1)

        c2 = Condition('상대팀이 토스를 준비 중인가?', self.is_enemy_setter_toss_wait)
        a2 = Action('blocking ready', self.blocking_ready)

        c5 = Condition('네트 앞으로 가야 하는가?', self.is_move_to_net)
        a5 = Action('move to net', self.move_to_net)

        SEQ_move_to_net_front = Sequence('네트 앞으로 이동', c2, c5, a5)
        SEQ_change_blocking_ready_state = Sequence('blocking ready 상태로 변경', c2, a2)

        SEL_move_to_net_front_or_change_blocking_ready_state = Selector('네트 앞으로 이동 또는 blocking ready 상태로 변경',
                                                                        SEQ_move_to_net_front, SEQ_change_blocking_ready_state)

        c3 = Condition('현재 상태가 blocking wait 인가?', self.is_cur_state_blocking_wait)
        a3 = Action('blocking wait', self.blocking_wait)

        SEQ_keep_blocking_wait_state = Sequence('blocking wait 상태 유지', c3, a3)

        c4 = Condition('상대팀 스파이커가 공격을 준비 중인가?', self.is_enemy_spiker_ready)
        a4 = Action('blocking hit', self.blocking_hit)

        SEQ_change_blocking_hit_state = Sequence('blocking hit 상태로 변경', c4, a4)

        c6 = Condition('현재 상태가 come back 인가?', self.is_cur_state_come_back)
        a6 = Action('come back', self.come_back)

        SEQ_keep_come_back_state = Sequence('come back 상태 유지', c6, a6)

        SEL_blocking = Selector('blocking', SEQ_keep_come_back_state,
                    SEQ_change_blocking_hit_state,
                    SEQ_keep_blocking_wait_state,
                    SEL_move_to_net_front_or_change_blocking_ready_state,)

        c7 = Condition('현재 상태가 time difference attack 인가?', self.is_cur_state_time_difference_attack)
        a7 = Action('시간차 공격', self.time_difference_attack)

        SEQ_time_difference_attack = Sequence('time difference attack', c7, a7)

        root = SEL_time_difference_attack_blocking_or_Idle = Selector(
            'time difference attack or blocking or Idle',
                    SEQ_time_difference_attack, SEL_blocking, SEQ_keep_Idle_state)

        self.bt = BehaviorTree(root)