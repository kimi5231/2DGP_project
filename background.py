from pico2d import load_image, get_canvas_width, get_canvas_height, clamp, draw_rectangle, load_music

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
        self.window_left = int(server.ball.x) - self.cw // 2
        self.window_bottom = int(server.ball.y) - self.ch // 2
        self.bgm = load_music('play_music.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        court_sx = self.court_x - self.window_left
        court_sy = self.court_y - self.window_bottom
        net_sx = self.net_x - self.window_left
        net_sy = self.net_y - self.window_bottom

        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
        self.court_image.clip_draw(0, 0, 600, 10, court_sx, court_sy)
        self.net_image.clip_draw(0, 0, 10, 81, net_sx, net_sy)

    def update(self):
        self.window_left = int(server.ball.x) - self.cw // 2
        self.window_bottom = int(server.ball.y) - self.ch // 2

        self.window_left = clamp(0, self.window_left, self.w - self.cw - 1)
        self.window_bottom = clamp(0, self.window_bottom, self.h - self.ch - 1)


class Player_Court:
    def __init__(self):
        self.x, self.y = 500, 51

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 300, sy - 5, sx, sy + 5

    def handle_collision(self, group, other):
        if group == 'player_court:ball':
            server.score.ai_score += 1
            server.judge.check_score_ai()


class AI_Court:
    def __init__(self):
        self.x, self.y = 500, 51

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx, sy - 5, sx + 300, sy + 5

    def handle_collision(self, group, other):
        if group == 'ai_court:ball':
            server.score.player_score += 1
            server.judge.check_score_player()


class Player_Court_Out:
    def __init__(self):
        self.x, self.y = 500, 51

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 500, sy - 5, sx - 300, sy + 5

    def handle_collision(self, group, other):
        if group == 'player_court_out:ball' and server.score.turn == 'ai':
            server.score.player_score += 1
            server.judge.check_score_player()
        elif group == 'player_court_out:ball' and server.score.turn == 'player':
            server.score.ai_score += 1
            server.judge.check_score_ai()

class AI_Court_Out:
    def __init__(self):
        self.x, self.y = 500, 51

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx + 300, sy - 5, sx + 500, sy + 5

    def handle_collision(self, group, other):
        if group == 'ai_court_out:ball' and server.score.turn == 'player':
            server.score.ai_score += 1
            server.judge.check_score_ai()
        elif group == 'ai_court_out:ball' and server.score.turn == 'ai':
            server.score.player_score += 1
            server.judge.check_score_player()


class Net:
    def __init__(self):
        self.x, self.y = 500, 97

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 3, sy - 40, sx + 7, sy + 40

    def handle_collision(self, group, other):
        if group == 'net:ball':
            pass