from pico2d import *

import logo_mode
from ground import Ground
from mario import Mario
import game_framework
import game_world



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(logo_mode)
        else:
            mario.handle_event(event)


def init():
    global mario

    ground = Ground()
    game_world.add_object(ground,0)

    mario = Mario()
    game_world.add_object(mario,1)



def update():
    game_world.update()

def finish():
    game_world.clear()
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()



