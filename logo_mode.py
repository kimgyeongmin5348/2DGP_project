from pico2d import load_image, delay, clear_canvas, update_canvas, get_events
from sdl2 import SDL_BUTTON_LEFT, SDL_MOUSEBUTTONDOWN

import game_world
import game_framework
import play_mode


def init():
    global image
    global running
    image = load_image('menu.png')
    running = True



def finish():
    global image
    del image


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    image.draw(1080 // 2, 721 // 2)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            game_framework.change_mode(play_mode)
