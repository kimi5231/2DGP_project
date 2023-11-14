from pico2d import load_image, get_time


class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        #self.cur_state = ?
        self.table = {

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
        self.start_time = get_time()

    def draw(self):
        self.image.draw(self.x, self.y, 30, 30)

    def update(self):
        self.x += self.dirX * self.speed
        self.y += self.dirY * self.speed