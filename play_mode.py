from pico2d import *

from mario import Mario
from ball import Ball
import game_framework
import game_world
import server

from background import FixedBackground as Background


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.mario.handle_event(event)


def init():

    server.background = Background()
    game_world.add_object(server.background, 0)
    game_world.add_collision_pair('mario:ball', server.mario, None)

    mario = Mario()
    game_world.add_object(server.mario, 2)

    server.ball = Ball()
    game_world.add_object(server.ball, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass



