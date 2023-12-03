from pico2d import *

import game_world
import game_framework
import logo_mode
import play_mode


def init():
    global image
    global running
    global music
    image = load_image('Last.png')
    running = True
    music = load_music('last_music.mp3')
    music = music.set_volume(32)
    music = music.repeat_play()



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
