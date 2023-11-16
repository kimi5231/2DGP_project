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


def remove_object(o): # 객체 삭제
    for layer in world:
        if o in layer:
            layer.remove(o)
            return


def clear():
    for layer in world:
        layer.clear()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True