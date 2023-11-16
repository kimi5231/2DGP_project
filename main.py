from pico2d import open_canvas, delay, close_canvas

import play_mode

open_canvas(1000, 600)

play_mode.init()

while play_mode.running:
    play_mode.handle_events()
    play_mode.update_world()
    play_mode.draw()
    delay(0.05)

play_mode.finish()

close_canvas()