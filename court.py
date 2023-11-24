from pico2d import load_image, get_canvas_width, get_canvas_height, clamp

import server


class Court:
    def __init__(self):
        self.image = load_image('background.png')
        self.court_image = load_image('court.png')
        self.net_image = load_image('net.png')
        self.cw = get_canvas_width()  # 화면의 너비
        self.ch = get_canvas_height()  # 화면의 높이
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        # self.image.draw(500, 300, 1000, 600)
        # self.court_image.draw(500, 51, 600, 10)
        # self.net_image.draw(500, 130, 30, 150)
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = int(server.player.x) - self.cw // 2
        self.window_bottom = int(server.player.y) - self.ch // 2

        self.window_left = clamp(0, self.window_left, self.w - self.cw - 1)
        self.window_bottom = clamp(0, self.window_bottom, self.h - self.ch - 1)