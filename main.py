
from pico2d import open_canvas, delay, close_canvas
import game_framework

import first_mode as start_mode

open_canvas(1280, 721)
game_framework.run(start_mode)
close_canvas()

