from pico2d import *

import game_world
import game_framework
import play_mode


def init():
    global image, bgm
    global running
    image = load_image('Start.png')
    running = True
    bgm = load_music('SellBuyMusic.mp3')
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
            game_framework.change_mode(play_mode)
        elif event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

