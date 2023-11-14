world = [ [], [] ]


def add_object(o, depth): # 게임 월드에 객체 담기
    world[depth].append(o)


def update(): # 게임 월드 객체 업데이트
    for layer in world:
        for o in layer:
            o.update()


def render(): # 게임 월드 객체 그리기
    for layer in world:
        for o in layer:
            o.draw()