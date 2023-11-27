from player import ServeWait, Idle

background = None
player_court = None
ai_court = None
player_court_out = None
ai_court_out = None
net = None

# plyer team
player = None
setter = None
blocker1 = None
blocker2 = None

# enemy team
spiker = None
enemy_setter = None
enemy_blocker1 = None
enemy_blocker2 = None

ball = None

timer = None
score = None
judge = None

stage = 1


def init_to_player_turn():
    score.turn = 'player'
    player.cur_state = ServeWait
    player.x = 100
    setter.x = 488
    blocker1.x = 470
    blocker2.x = 455

    spiker.state = 'Idle'
    spiker.x = 700
    enemy_setter.x = 518
    enemy_blocker1.x = 536
    enemy_blocker2.x = 551

    ball.x = player.x + 10
    ball.y = player.y + 10

    judge.team = 'player'
    judge.state = 'draw'
    judge.frame = 0
    judge.action = 0


def init_to_ai_turn():
    score.turn = 'ai'
    player.cur_state = Idle
    player.x = 300
    setter.x = 488
    blocker1.x = 470
    blocker2.x = 455

    spiker.state = 'serve ready'
    spiker.x = 900
    enemy_setter.x = 518
    enemy_blocker1.x = 536
    enemy_blocker2.x = 551

    ball.x = spiker.x - 10
    ball.y = spiker.y + 10

    judge.team = 'ai'
    judge.state = 'draw'
    judge.frame = 0
    judge.action = 0