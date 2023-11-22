from pico2d import open_canvas, close_canvas
import game_framework

import logo_mode as start_mode

open_canvas(1820, 1000)
game_framework.run(start_mode)
close_canvas()