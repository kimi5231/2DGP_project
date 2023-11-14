from pico2d import load_image, get_time, delay
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_SPACE

import game_world
from ball import Ball

PLAYER_H = 110
MOVE_W = 50
MOVE_N = 5
DRIVE_W = 70
DRIVE_READY_N = 4
DRIVE_WAIT_N = 1
DRIVE_HIT_N = 3


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


def time_out(e):
    return e[0] == 'TIME_OUT'


class ServeHit:
    @staticmethod
    def enter(player, e): # Serve 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 3
        player.frame_num = DRIVE_HIT_N
        player.frame_len = DRIVE_W

    @staticmethod
    def exit(player, e): # Serve 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # Serve 상태인 동안 할 것
        if player.frame == 2:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = (player.frame + 1) % player.frame_num
        delay(0.05)

    @staticmethod
    def draw(player): # player 그리기
        player.image.clip_draw(player.frame * player.frame_len,
                              player.action * player.action_len,
                              player.frame_len, player.action_len, player.x, player.y)


class ServeWait:
    @staticmethod
    def enter(player, e): # Serve 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 2
        player.frame_num = DRIVE_WAIT_N
        player.frame_len = DRIVE_W
        player.start_time = get_time()

    @staticmethod
    def exit(player, e): # Serve 상태에서 나올 때 할 것
        player.make_ball()
        pass

    @staticmethod
    def do(player): # Serve 상태인 동안 할 것
        player.frame = (player.frame + 1) % player.frame_num
        if get_time() - player.start_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player): # player 그리기
        player.image.clip_draw(player.frame * player.frame_len,
                              player.action * player.action_len,
                              player.frame_len, player.action_len, player.x, player.y)


class ServeReady:
    @staticmethod
    def enter(player, e): # Serve 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 1
        player.frame_num = DRIVE_READY_N
        player.frame_len = DRIVE_W

    @staticmethod
    def exit(player, e): # Serve 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # Serve 상태인 동안 할 것
        if player.frame == 3:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = (player.frame + 1) % player.frame_num
        delay(0.05)

    @staticmethod
    def draw(player): # player 그리기
        player.image.clip_draw(player.frame * player.frame_len,
                              player.action * player.action_len,
                              player.frame_len, player.action_len, player.x, player.y)


class Move:
    @staticmethod
    def enter(player, e): # Move 상태로 들어갈 때 할 것
        if right_down(e) or left_up(e):
            player.dir = 1
        if left_down(e) or right_up(e):
            player.dir = -1
        player.frame = 0
        player.action = 0
        player.frame_num = MOVE_N
        player.frame_len = MOVE_W

    @staticmethod
    def exit(player, e): # Move 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # Move 상태인 동안 할 것
        player.frame = (player.frame + 1) % player.frame_num
        player.x += player.dir * player.speed

    @staticmethod
    def draw(player): # player 그리기
        player.image.clip_draw(player.frame * player.frame_len,
                              player.action * player.action_len,
                              player.frame_len, player.action_len, player.x, player.y)


class Idle:
    @staticmethod
    def enter(player, e): # Idle 상태로 들어갈 때 할 것
        player.frame = 0
        player.action = 0
        player.frame_num = 1
        player.frame_len = MOVE_W

    @staticmethod
    def exit(player, e): # Idle 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(player): # Move 상태인 동안 할 것
        player.frame = (player.frame + 1) % player.frame_num

    @staticmethod
    def draw(player): # player 그리기
        player.image.clip_draw(player.frame * player.frame_len,
                              player.action * player.action_len,
                              player.frame_len, player.action_len, player.x, player.y)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.table = {
            Idle: {right_down: Move, right_up: Move, left_down: Move, left_up: Move, space_down: ServeReady},
            Move: {right_down: Idle, right_up: Idle, left_down: Idle, left_up: Idle},
            ServeReady: {time_out: ServeWait},
            ServeWait: {space_down: ServeHit, time_out: Idle},
            ServeHit: {time_out: Idle}
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
        self.x, self.y, self.dir, self.speed = 300, 105, 0, 10
        self.frame = 0
        self.action = 0
        self.frame_num = MOVE_N
        self.frame_len = MOVE_W
        self.action_len = PLAYER_H
        self.image = load_image('player.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def make_ball(self):
        ball = Ball(self.x + 25, self.y + 50, 1, 10)
        game_world.add_object(ball, 1)