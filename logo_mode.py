from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time

import game_framework
import play_mode


def init():
    global image
    global running
    global logo_start_time
    image = load_image('Start.png')
    running = True
    logo_start_time = get_time()


def finish():
    global image
    del image


def update():
    global logo_start_time
    if get_time() - logo_start_time >= 3.0:
        logo_start_time = get_time()
        game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(1820//2,1000//2)
    update_canvas()

def handle_events():
    events = get_events()
