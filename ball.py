from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import game_world


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


class Fly:
    @staticmethod
    def enter(ball, e): # Fly 상태로 들어갈 때 할 것
        ball.dirX = 1
        ball.dirY = 1

    @staticmethod
    def exit(ball, e): # Fly 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(ball): # Fly 상태인 동안 할 것
        ball.x += ball.dirX * ball.speed
        ball.y += ball.dirY * ball.speed
        # if get_time() - ball.start_time > 0.5:
        #     ball.dirY = -1
        # if get_time() - ball.start_time > 2:
        #     game_world.remove_object(ball)

    @staticmethod
    def draw(ball): # ball 그리기
        ball.image.draw(ball.x, ball.y, 30, 30)


class Ready:
    @staticmethod
    def enter(ball, e): # Ready 상태로 들어갈 때 할 것
        ball.start_time = get_time()

    @staticmethod
    def exit(ball, e): # Ready 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(ball): # Ready 상태인 동안 할 것
        ball.x += ball.dirX * ball.speed
        ball.y += ball.dirY * ball.speed
        if get_time() - ball.start_time > 0.5:
            ball.dirY = -1
        if get_time() - ball.start_time > 2:
            game_world.remove_object(ball)

    @staticmethod
    def draw(ball): # ball 그리기
        ball.image.draw(ball.x, ball.y, 30, 30)


class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        self.cur_state = Ready
        self.table = {
            Ready: {space_down: Fly}
        }

    def start(self):
        self.cur_state.enter(self.ball, ('START', 0))

    def draw(self):
        self.cur_state.draw(self.ball)

    def update(self):
        self.cur_state.do(self.ball)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ball, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ball, e)
                return True
        return False


class Ball:
    def __init__(self, x, y, dirX, dirY, speed):
        self.x, self.y, self.dirX, self.dirY, self.speed = x, y, dirX, dirY, speed
        self.image = load_image('ball.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))