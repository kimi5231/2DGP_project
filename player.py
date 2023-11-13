from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_SPACE

PLAYER_H = 110
MOVE_W = 50
MOVE_N = 5
DRIVE_W = 70
DRIVE_READY_N = 4
DRIVE_WAIT_N = 1
DRIVE_HIT_N = 3


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
    def exit(boy, e): # Move 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(boy): # Move 상태인 동안 할 것
        pass

    @staticmethod
    def draw(boy): # player 그리기
        pass


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Move
        self.table = {
            Move: { }
        }

    def start(self):
        self.cur_state.enter(self.player, ('START', 0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.plyer)

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
        self.x = 300
        self.y = 105
        self.dir = 0
        self.speed = 10
        self.frame = 0
        self.action = 0
        self.frame_num = MOVE_N
        self.frame_len = MOVE_W
        self.action_len = PLAYER_H
        self.image = load_image('player.png')

    def draw(self):
        self.frame = (self.frame + 1) % self.frame_num
        self.image.clip_draw(self.frame * self.frame_len,
                             self.action * self.action_len,
                             self.frame_len, self.action_len, self.x, self.y)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.action = 0
                self.frame_num = MOVE_N
                self.frame_len = MOVE_W
                self.dir = 1
            elif event.key == SDLK_LEFT:
                self.action = 0
                self.frame_num = MOVE_N
                self.frame_len = MOVE_W
                self.dir = -1
            elif event.key == SDLK_SPACE:
                self.action = 2
                self.frame_num = DRIVE_WAIT_N
                self.frame_len = DRIVE_W
        elif event.type == SDL_KEYUP:
            self.dir = 0
            self.frame = 0

    def move(self):
        self.x += self.dir * self.speed

    def drive_serve(self):
        pass