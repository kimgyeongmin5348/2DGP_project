import random
import json
import os

from pico2d import *

import game_framework
import game_world

import server
from boy import Boy
from ball import Ball
from flag import Flag
from item import Item
from club import Club

from background import FixedBackground as Background



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.boy.handle_event(event)



def init():

    server.background = Background()
    game_world.add_object(server.background, 0)



    server.boy = Boy()
    game_world.add_object(server.boy, 2)
    game_world.add_collision_pair('boy:ball', server.boy, None)

    server.ball = Ball()
    game_world.add_object(server.ball, 2)
    game_world.add_collision_pair('boy:ball', None, server.ball)
    game_world.add_collision_pair('ball:flag', server.ball, None)
    game_world.add_collision_pair('club:ball', None, server.ball)

    server.flag = Flag()
    game_world.add_object(server.flag, 3)
    game_world.add_collision_pair('ball:flag', None, server.flag)

    server.item = Item()
    game_world.add_object(server.item, 3)

    server.club = Club()
    game_world.add_object(server.club, 2)
    game_world.add_collision_pair('club:ball', server.club, None)







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



