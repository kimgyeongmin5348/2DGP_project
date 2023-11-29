from pico2d import *

import game_world
import game_framework
import play_mode


def init():
    global image
    global running
    image = load_image('Start.png')
    running = True



def finish():
    global image
    del image


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    image.draw(1280 // 2, 721 // 2)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_s:
            game_framework.change_mode(play_mode)
