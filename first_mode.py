from pico2d import *

import game_world
import game_framework
import logo_mode
import play_mode
import second_mode


def init():
    global image, bgm
    global running
    image = load_image('First.png')
    running = True
    bgm = load_music('firstmusic.mp3')
    bgm.set_volume(32)
    bgm.play()


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
            game_framework.change_mode(second_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
