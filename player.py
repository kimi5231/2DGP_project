from pico2d import load_image, get_time, delay, draw_rectangle, clamp
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_SPACE, SDLK_a, SDLK_z

import game_framework
import game_world
import server
from ball import Ball

# player move speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
MOVE_SPEED_KMPH = 10.0 # Km / Hour
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

# player spike speed
SPIKE_SPEED_KMPH = 105.0 # Km / Hour
SPIKE_SPEED_MPM = (SPIKE_SPEED_KMPH * 1000.0 / 60.0)
SPIKE_SPEED_MPS = (SPIKE_SPEED_MPM / 60.0)
SPIKE_SPEED_PPS = (SPIKE_SPEED_MPS * PIXEL_PER_METER)

# player drive speed
DRIVE_SPEED_KMPH = 50.0 # Km / Hour
DRIVE_SPEED_MPM = (DRIVE_SPEED_KMPH * 1000.0 / 60.0)
DRIVE_SPEED_MPS = (DRIVE_SPEED_MPM / 60.0)
DRIVE_SPEED_PPS = (DRIVE_SPEED_MPS * PIXEL_PER_METER)

# player action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z


def time_out(e):
    return e[0] == 'TIME_OUT'


class OpenAttackHit:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.action = 5
        player.frame_num = 6
        player.frame_len = 80
        player.action_len = 210

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if int(player.frame) == 5:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)

    @staticmethod
    def draw(player):
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_210.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy + 33, 50, 100)


class OpenAttackWait:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.action = 4
        player.frame_num = 1
        player.frame_len = 80
        player.action_len = 210
        player.start_time = get_time()

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)
        if get_time() - player.start_time > 1.5:
            player.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(player):
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_210.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy + 33, 50, 100)


class OpenAttackReady:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.action = 3
        player.frame_num = 7
        player.frame_len = 80
        player.action_len = 210

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if int(player.frame) == 6:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)

    @staticmethod
    def draw(player):
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_210.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy+20, 50, 100)


class Receive:
    @staticmethod
    def enter(player, e): # Receive 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 6
        player.frame_num = 5
        player.frame_len = 70
        player.action_len = 110

    @staticmethod
    def exit(player, e): # Receive 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # Receive 상태인 동안 할 것
        if int(player.frame) == 4:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)

    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_110.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy, 40, 66)


class SpikeServeHit:
    @staticmethod
    def enter(player, e): # DriveServeHit 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 2
        player.frame_num = 6
        player.frame_len = 80
        player.action_len = 210

    @staticmethod
    def exit(player, e): # DriveServeHit 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # DriveServeHit 상태인 동안 할 것
        if int(player.frame) == 5:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)

    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_210.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy + 33, 43, 99)


class SpikeServeWait:
    @staticmethod
    def enter(player, e): # DriveServeWait 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 1
        player.frame_num = 1
        player.frame_len = 80
        player.action_len = 210
        player.start_time = get_time()

    @staticmethod
    def exit(player, e): # DriveServeWait 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # DriveServeWait 상태인 동안 할 것
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)
        if get_time() - player.start_time > 1.5:
            player.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_210.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy + 33, 43, 99)


class SpikeServeReady:
    @staticmethod
    def enter(player, e): # SpikeServeReady 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 0
        player.frame_num = 10
        player.frame_len = 80
        player.action_len = 210

    @staticmethod
    def exit(player, e): # SpikeServeReady 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # SpikeServeReady 상태인 동안 할 것
        if int(player.frame) == 9:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = ((player.frame + player.frame_num * (ACTION_PER_TIME//1.5) * game_framework.frame_time)
                        % player.frame_num)

    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_210.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy+20, 43, 99)


class DriveServeHit:
    @staticmethod
    def enter(player, e): # DriveServeHit 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 5
        player.frame_num = 3
        player.frame_len = 70
        player.action_len = 110

    @staticmethod
    def exit(player, e): # DriveServeHit 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # DriveServeHit 상태인 동안 할 것
        if int(player.frame) == 2:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)

    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_110.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy, 40, 66)


class DriveServeWait:
    @staticmethod
    def enter(player, e): # DriveServeWait 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 4
        player.frame_num = 1
        player.frame_len = 70
        player.action_len = 110
        player.start_time = get_time()

    @staticmethod
    def exit(player, e): # DriveServeWait 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # DriveServeWait 상태인 동안 할 것
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)
        if get_time() - player.start_time > 1.5:
            player.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_110.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy, 40, 66)


class DriveServeReady:
    @staticmethod
    def enter(player, e): # DriveServeReady 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 3
        player.frame_num = 4
        player.frame_len = 70
        player.action_len = 110

    @staticmethod
    def exit(player, e): # DriveServeReady 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # DriveServeReady 상태인 동안 할 것
        if int(player.frame) == 3:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)

    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_110.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy, 40, 66)


class ServeWait:
    @staticmethod
    def enter(player, e): # ServeWait 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 2
        player.frame_num = 1
        player.frame_len = 70
        player.action_len = 110
        player.start_time = get_time()

    @staticmethod
    def exit(player, e): # ServeWait 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # ServeWait 상태인 동안 할 것
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)
        if get_time() - player.start_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_110.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy, 40, 66)


class Move:
    @staticmethod
    def enter(player, e): # Move 상태로 들어갈 때 할 것
        if right_down(e) or left_up(e):
            player.dir = 1
        if left_down(e) or right_up(e):
            player.dir = -1
        player.frame = 0
        player.action = 1
        player.frame_num = 5
        player.frame_len = 50
        player.action_len = 110

    @staticmethod
    def exit(player, e): # Move 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # Move 상태인 동안 할 것
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)
        player.x += player.dir * MOVE_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_110.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy, 33, 66)


class Idle:
    @staticmethod
    def enter(player, e): # Idle 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 0
        player.frame_num = 1
        player.frame_len = 50
        player.action_len = 110

    @staticmethod
    def exit(player, e): # Idle 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # Move 상태인 동안 할 것
        player.frame = ((player.frame + player.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % player.frame_num)

    @staticmethod
    def draw(player): # player 그리기
        sx = player.x - server.background.window_left
        sy = player.y - server.background.window_bottom
        player.image_110.clip_draw(int(player.frame) * player.frame_len,
                                   player.action * player.action_len,
                                   player.frame_len, player.action_len, sx, sy, 33, 66)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.table = {
            Idle: {right_down: Move, right_up: Move, left_down: Move, left_up: Move, space_down: ServeWait, a_down: Receive, z_down:OpenAttackReady},
            Move: {right_down: Idle, right_up: Idle, left_down: Idle, left_up: Idle},
            ServeWait: {right_down: DriveServeReady, left_down: SpikeServeReady, time_out: Idle},
            DriveServeReady: {time_out: DriveServeWait},
            DriveServeWait: {space_down: DriveServeHit, time_out: Idle},
            DriveServeHit: {time_out: Idle},
            SpikeServeReady: {time_out: SpikeServeWait},
            SpikeServeWait: {space_down: SpikeServeHit, time_out: Idle},
            SpikeServeHit: {time_out: Idle},
            Receive: {time_out: Idle},
            OpenAttackReady: {time_out: OpenAttackWait},
            OpenAttackWait: {z_down: OpenAttackHit, time_out: Idle},
            OpenAttackHit: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('START', 0))

    def draw(self):
        self.cur_state.draw(self.player)

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True
        return False


class Player:
    def __init__(self):
        self.x = 100
        self.y = 85
        self.dir = 0
        self.frame = 0
        self.action = 0
        self.frame_num = 1
        self.frame_len = 50
        self.action_len = 110
        self.image_110 = load_image('player_h110.png')
        self.image_210 = load_image('player_h210.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom

        if self.state_machine.cur_state == Move:
            return sx - 16, sy - 33, sx + 16, sy + 33
        elif self.state_machine.cur_state == DriveServeHit:
            return sx + 5, sy - 5, sx + 15, sy + 5
        elif self.state_machine.cur_state == SpikeServeHit:
            return sx, sy + 70, sx + 10, sy + 80
        elif self.state_machine.cur_state == OpenAttackHit:
            return sx, sy + 70, sx + 10, sy + 80
        else:
            return 0, 0, 0, 0

    def handle_collision(self, group, other):
        if group == 'player:ball':
            if self.state_machine.cur_state == DriveServeHit:
                server.ball.speed_x = DRIVE_SPEED_PPS
                server.ball.speed_y = DRIVE_SPEED_PPS
            elif self.state_machine.cur_state == SpikeServeHit:
                server.ball.speed_x = SPIKE_SPEED_PPS
                server.ball.speed_y = DRIVE_SPEED_PPS
            elif self.state_machine.cur_state == OpenAttackHit:
                server.ball.speed_x = SPIKE_SPEED_PPS