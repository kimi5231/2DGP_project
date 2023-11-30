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

# ai team
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

    player.state_machine.handle_event(('Change_Serve_Wait', 0))
    player.x = 100
    setter.state, setter.x = 'Idle', 488
    blocker1.state, blocker1.x = 'Idle', 470
    blocker2.state, blocker2.x = 'Idle', 455

    spiker.state, spiker.x = 'Idle', 700
    enemy_setter.state, enemy_setter.x = 'Idle', 518
    enemy_blocker1.state, enemy_blocker1.x = 'Idle', 536
    enemy_blocker2.state, enemy_blocker2.x = 'Idle', 551

    ball.x, ball.y = player.x + 10, player.y + 10

    judge.team = 'player'
    judge.state = 'draw'
    judge.frame = 0
    judge.action = 0


def init_to_ai_turn():
    score.turn = 'ai'

    player.state_machine.handle_event(('Change_Idle', 0))
    player.x = 300
    setter.state, setter.x = 'Idle', 488
    blocker1.state, blocker1.x = 'Idle', 470
    blocker2.state, blocker2.x = 'Idle', 455

    spiker.state, spiker.x = 'serve ready', 900
    enemy_setter.state, enemy_setter.x = 'Idle', 518
    enemy_blocker1.state, enemy_blocker1.x = 'Idle', 536
    enemy_blocker2.state, enemy_blocker2.x = 'Idle', 551

    ball.x, ball.y = spiker.x - 10, spiker.y + 10

    judge.team = 'ai'
    judge.state = 'draw'
    judge.frame = 0
    judge.action = 0