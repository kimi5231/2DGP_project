from pico2d import load_image, get_time, draw_rectangle, clamp

import game_framework
import server

# ball gravity speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
Gravity_SPEED_MPSS = 9.8//2
Gravity_SPEED_PPS = (Gravity_SPEED_MPSS * PIXEL_PER_METER)


class Ball:
    def __init__(self, x, y, dir, speed_x, speed_y):
        self.x, self.y, self.dir, self.speed_x, self.speed_y = x, y, dir, speed_x, speed_y
        self.state = 'fly'
        self.image = load_image('ball.png')
        self.start_time = 0.0

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy, 22, 22)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.state != 'Idle':
            self.x += self.dir * self.speed_x * game_framework.frame_time
            self.y += self.speed_y * game_framework.frame_time
            if get_time() - self.start_time >= 0.5 and self.state == 'fly':
                self.start_time = get_time()
                self.speed_y -= Gravity_SPEED_PPS
            self.x = clamp(30, self.x, server.background.w - 40)
            self.y = clamp(30, self.y, server.background.h - 40)

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 11, sy - 11, sx + 11, sy + 11

    def handle_collision(self, group, other):
        if group == 'player:ball':
            self.dir = 1
        # if group == 'setter:ball':
        #     self.dir = 0
        if group == 'blocker:ball':
            self.dir = 1
        if group == 'spiker:ball':
            self.dir = -1
        if group == 'enemy_blocker:ball':
            self.dir = -1
        if group == 'player_court:ball' or group == 'ai_court_out:ball' or group == 'ai_court:ball' or group == 'player_court_out:ball':
            self.state = 'Idle'
            self.dir = 0
            self.speed_x = 0
            self.speed_y = 0
        if group == 'net:ball':
            self.dir *= -1