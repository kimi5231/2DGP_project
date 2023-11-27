from pico2d import load_image, draw_rectangle

import game_framework
import server
from behavior_tree import BehaviorTree, Action, Condition, Sequence, Selector

# spiker move speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
MOVE_SPEED_KMPH = 10.0 # Km / Hour
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

# player drive speed
DRIVE_SPEED_KMPH = 50.0 # Km / Hour
DRIVE_SPEED_MPM = (DRIVE_SPEED_KMPH * 1000.0 / 60.0)
DRIVE_SPEED_MPS = (DRIVE_SPEED_MPM / 60.0)
DRIVE_SPEED_PPS = (DRIVE_SPEED_MPS * PIXEL_PER_METER)

# spiker receive speed
RECEIVE_SPEED_KMPH = 10.0 # Km / Hour
RECEIVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
RECEIVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
RECEIVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

# spiker action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Spiker:
    def __init__(self):
        self.x = 700
        self.y = 85
        self.frame = 0
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        self.action_len = 110
        self.image_110 = load_image('player_h110.png')
        self.image_210 = load_image('player_h210.png')
        self.build_behavior_tree()
        self.state = 'Idle'

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        if self.action_len == 110:
            self.image_110.clip_composite_draw(int(self.frame) * self.frame_len,
                                               self.action * self.action_len,
                                               self.frame_len, self.action_len, 0, 'h', sx, sy, 33, 66)
        elif self.action_len == 210:
            self.image_210.clip_composite_draw(int(self.frame) * self.frame_len,
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
        return sx - 16, sy - 33, sx + 16, sy + 33

    def handle_collision(self, group, other):
        if group == 'spiker:ball':
            if self.state == 'chase':
                self.state = 'receive'
                server.ball.speed_x = RECEIVE_SPEED_PPS
                server.ball.speed_y = DRIVE_SPEED_PPS

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
        if self.distance_less_than(server.ball.x, server.ball.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def chase_ball(self, r=0.5):
        self.action = 1
        self.frame_num = 5
        self.frame_len = 50
        self.action_len = 110
        self.state = 'chase'
        if server.ball.x < self.x:
            self.x += -1 * MOVE_SPEED_PPS * game_framework.frame_time
        else:
            self.x += 1 * MOVE_SPEED_PPS * game_framework.frame_time
        return BehaviorTree.RUNNING

    def is_cur_state_receive(self):
        if self.state == 'receive':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def receive(self):
        self.action = 6
        self.frame_num = 5
        self.frame_len = 70
        self.action_len = 110
        if int(self.frame) == 4:
            self.state = 'move to net'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_move_to_net(self):
        if self.state == 'move to net':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_net(self, r=0.5):
        self.action = 1
        self.frame_num = 5
        self.frame_len = 50
        self.action_len = 110
        self.x += -1 * MOVE_SPEED_PPS * game_framework.frame_time
        if self.distance_less_than(server.background.net_x, server.background.net_y, self.x, self.y, 0.5):
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_cur_state_wait_setter_toss(self):
        if self.state == 'wait setter toss':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def spike(self):
        pass

    def is_cur_state_serve_ready(self):
        if self.state == 'serve ready':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def serve_ready(self):
        self.action = 2
        self.frame_num = 1
        self.frame_len = 70
        self.action_len = 110
        return BehaviorTree.RUNNING

    def is_cur_state_drive_serve_ready(self):
        if self.state == 'drive serve ready':
            server.ball.speed_y = DRIVE_SPEED_PPS
            server.ball.state = 'fly'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def drive_serve_ready(self):
        self.action = 3
        self.frame_num = 4
        self.frame_len = 70
        self.action_len = 110
        if int(self.frame) == 3:
            self.state = 'drive_serve_wait'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_cur_state_drive_serve_wait(self):
        if self.state == 'drive serve wait':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def drive_serve_wait(self):
        self.action = 4
        self.frame_num = 1
        self.frame_len = 70
        self.action_len = 110
        return BehaviorTree.RUNNING

    def is_cur_state_drive_serve_hit(self):
        if self.state == 'drive serve hit':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def drive_serve_hit(self):
        self.action = 5
        self.frame_num = 3
        self.frame_len = 70
        self.action_len = 110
        if int(self.frame) == 2:
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('현재 상태가 Idle 인가?', self.is_cur_state_Idle)
        a1 = Action('Idle', self.Idle)

        SEQ_keep_Idle_state = Sequence('Idle 상태 유지', c1, a1)

        c2 = Condition('공이 근처에 있는가?', self.is_ball_nearby, 10)
        a2 = Action('chase ball', self.chase_ball)

        SEQ_chase_ball = Sequence('chase ball 상태로 변경', c2, a2)

        c3 = Condition('현재 상태가 receive 인가?', self.is_cur_state_receive)
        a3 = Action('receive', self.receive)

        SEQ_keep_receive_state = Sequence('receive 상태 유지', c3, a3)

        c4 = Condition('네트 앞으로 가야 하는가?', self.is_move_to_net)
        a4 = Action('move to net', self.move_to_net)

        SEQ_move_to_net_front = Sequence('네트 앞으로 이동', c4, a4)

        c5 = Condition('현재 상태가 drive serve ready 인가?', self.is_cur_state_drive_serve_ready)
        a5 = Action('drive serve ready', self.drive_serve_ready)

        SEQ_drive_serve_ready = Sequence('drive serve ready', c5, a5)

        c6 = Condition('현재 상태가 drive serve wait 인가?', self.is_cur_state_drive_serve_wait)
        a6 = Action('drive serve wait', self.drive_serve_wait)

        SEQ_drive_serve_wait = Sequence('drive serve wait', c6, a6)

        c7 = Condition('현재 상태가 drive serve hit 인가?', self.is_cur_state_drive_serve_hit)
        a7 = Action('drive serve hit', self.drive_serve_hit)

        SEQ_drive_serve_hit = Sequence('drive serve hit', c6, a6)

        c8 = Condition('현재 상태가 serve ready 인가?', self.is_cur_state_serve_ready)
        a8 = Action('serve ready', self.serve_ready)

        SEQ_serve_ready = Sequence('serve ready', c8, a8)

        root = SEL__move_to_net_receive_or_chase_ball_or_Idle = Selector('move to net or receive or chase ball or Idle',
                                                            SEQ_serve_ready,
                                                            SEQ_drive_serve_hit,
                                                            SEQ_drive_serve_wait,
                                                            SEQ_drive_serve_ready,
                                                            SEQ_move_to_net_front,
                                                            SEQ_keep_receive_state,
                                                            SEQ_chase_ball,
                                                            SEQ_keep_Idle_state)

        self.bt = BehaviorTree(root)