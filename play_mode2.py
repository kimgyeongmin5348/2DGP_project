import random
import json
import os

from pico2d import *

import game_framework
import game_world

import server2
from boy2 import Boy2
from ball2 import Ball2
from flag2 import Flag2
from item import Item

from background2 import FixedBackground2 as Background2



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server2.boy2.handle_event(event)



def init():

    server2.background2 = Background2()
    game_world.add_object(server2.background2, 0)

    server2.boy2 = Boy2()
    game_world.add_object(server2.boy2, 2)
    game_world.add_collision_pair('boy:ball', server2.boy2, None)

    server2.ball2 = Ball2()
    game_world.add_object(server2.ball2, 2)
    game_world.add_collision_pair('boy:ball', None, server2.ball2)
    game_world.add_collision_pair('ball:flag', server2.ball2, None)

    server2.flag2 = Flag2()
    game_world.add_object(server2.flag2, 3)
    game_world.add_collision_pair('ball:flag', None, server2.flag2)

    server2.item = Item()
    game_world.add_object(server2.item, 3)







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


