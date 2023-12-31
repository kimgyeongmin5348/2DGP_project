from pico2d import *

import game_world
import game_framework
import logo_mode
import play_mode


def init():
    global image
    image = load_image('Last.png')





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
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(logo_mode)
