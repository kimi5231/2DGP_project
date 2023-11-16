def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    while running: # 현재 게임 모드에 대한 게임 루프를 실행
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while (len(stack) > 0): # 스택에 남아있는 모든 게임 모드들을 차례대로 제거
        stack[-1].finish()
        stack.pop()


def quit():
    global running
    running = False


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    if (len(stack) > 0):
        stack[-1].resume()