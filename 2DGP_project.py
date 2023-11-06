from pico2d import *
from court import Court

open_canvas(1000, 600)
court = Court()
court.draw()
update_canvas()
delay(1.0)
close_canvas()