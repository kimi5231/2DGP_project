from pico2d import load_image

import game_framework
import server

# judge action speed
TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Judge:
    def __init__(self):
        self.x, self.y = 300, 300
        self.frame = 0
        self. action = 0
        self.frame_len = 300
        self.action_len = 200
        self.frame_num = 3
        self.state = 'serve check'
        self.team = 'player'
        self.image = load_image('judge.png')

    def draw(self):
        if self.state == 'serve check' or self.state == 'score check':
            if self.team == 'player':
                self.image.clip_draw(int(self.frame) * self.frame_len,
                                           self.action * self.action_len,
                                            self.frame_len, self.action_len, self.x - 50, self.y - 50,
                                            200, 100)
            else:
                self.image.clip_composite_draw(int(self.frame) * self.frame_len,
                                               self.action * self.action_len,
                                               self.frame_len, self.action_len, 0, 'h', self.x + 50, self.y - 50,
                                               200, 100)

    def update(self):
        if int(self.frame) == 2 and self.state == 'score check':
            self.state = 'serve check'
            if self.team == 'player':
                self.init_to_player_turn()
            else:
                self.init_to_ai_turn()
        elif int(self.frame) == 2 and self.state == 'serve check':
            self.state = 'hide'
            if self.team == 'ai' and server.spiker.state == 'serve ready':
                server.spiker.state = 'drive serve ready'
        self.frame = ((self.frame + self.frame_num * ACTION_PER_TIME * game_framework.frame_time)
                        % self.frame_num)

    def check_score_player(self):
        self.team = 'player'
        self.state = 'score check'
        self.frame = 0
        self.action = 1
        server.ball.state = 'Idle'

    def check_score_ai(self):
        self.team = 'ai'
        self.state = 'score check'
        self.frame = 0
        self.action = 1
        server.ball.state = 'Idle'

    def init_to_player_turn(self):
        server.score.turn = 'player'

        server.player.state_machine.handle_event(('Change_Serve_Wait', 0))
        server.player.x = 100
        server.setter.state, server.setter.x = 'Idle', 488
        server.blocker1.state, server.blocker1.x = 'Idle', 470
        server.blocker2.state, server.blocker2.x = 'Idle', 455

        server.spiker.state, server.spiker.x = 'Idle', 700
        server.enemy_setter.state, server.enemy_setter.x = 'Idle', 518
        server.enemy_blocker1.state, server.enemy_blocker1.x = 'Idle', 536
        server.enemy_blocker2.state, server.enemy_blocker2.x = 'Idle', 551

        server.ball.x, server.ball.y = server.player.x + 10, server.player.y + 10

        self.state = 'serve check'
        self.frame = 0
        self.action = 0

    def init_to_ai_turn(self):
        server.score.turn = 'ai'

        server.player.state_machine.handle_event(('Change_Idle', 0))
        server.player.x = 300
        server.setter.state, server.setter.x = 'Idle', 488
        server.blocker1.state, server.blocker1.x = 'Idle', 470
        server.blocker2.state, server.blocker2.x = 'Idle', 455

        server.spiker.state, server.spiker.x = 'serve ready', 900
        server.enemy_setter.state, server.enemy_setter.x = 'Idle', 518
        server.enemy_blocker1.state, server.enemy_blocker1.x = 'Idle', 536
        server.enemy_blocker2.state, server.enemy_blocker2.x = 'Idle', 551

        server.ball.x, server.ball.y = server.spiker.x - 10, server.spiker.y + 10

        self.state = 'serve check'
        self.frame = 0
        self.action = 0