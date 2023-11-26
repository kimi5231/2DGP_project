from pico2d import load_image, get_canvas_width, get_canvas_height, clamp

import server


class Background:
    def __init__(self):
        self.image = load_image('background.png')
        self.court_image = load_image('court.png')
        self.net_image = load_image('net.png')
        self.cw = get_canvas_width()  # 화면의 너비
        self.ch = get_canvas_height()  # 화면의 높이
        self.w = self.image.w
        self.h = self.image.h
        self.court_x, self.court_y = 500, 51
        self.net_x, self.net_y = 500, 97

    def draw(self):
        court_sx = self.court_x - server.background.window_left
        court_sy = self.court_y - server.background.window_bottom
        net_sx = self.net_x - server.background.window_left
        net_sy = self.net_y - server.background.window_bottom

        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
        self.court_image.clip_draw(0, 0, 600, 10, court_sx, court_sy)
        self.net_image.clip_draw(0, 0, 10, 81, net_sx, net_sy)

    def update(self):
        self.window_left = int(server.ball.x) - self.cw // 2
        self.window_bottom = int(server.ball.y) - self.ch // 2

        self.window_left = clamp(0, self.window_left, self.w - self.cw - 1)
        self.window_bottom = clamp(0, self.window_bottom, self.h - self.ch - 1)