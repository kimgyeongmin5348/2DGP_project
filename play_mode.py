import random
import json
import os

from pico2d import *

import game_framework
import game_world
import item_mode

import server
from boy import Boy
from ball import Ball
from flag import Flag
from flag2 import Flag2
from flag3 import Flag3
from flag4 import Flag4
from flag5 import Flag5
from flag6 import Flag6
from flag7 import Flag7
from flag8 import Flag8
from flag9 import Flag9
from flag10 import Flag10
from flag11 import Flag11
from flag12 import Flag12
from flag13 import Flag13
from flag14 import Flag14
from flag15 import Flag15
from flag16 import Flag16
from flag17 import Flag17
from item import Item
from final_flag import Final

from background import FixedBackground as Background



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.push_mode(item_mode)
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
    game_world.add_collision_pair('ball:flag2', server.ball, None)
    game_world.add_collision_pair('ball:flag3', server.ball, None)
    game_world.add_collision_pair('ball:flag4', server.ball, None)
    game_world.add_collision_pair('ball:flag5', server.ball, None)
    game_world.add_collision_pair('ball:flag6', server.ball, None)
    game_world.add_collision_pair('ball:flag7', server.ball, None)
    game_world.add_collision_pair('ball:flag8', server.ball, None)
    game_world.add_collision_pair('ball:flag9', server.ball, None)
    game_world.add_collision_pair('ball:flag10', server.ball, None)
    game_world.add_collision_pair('ball:flag11', server.ball, None)
    game_world.add_collision_pair('ball:flag12', server.ball, None)
    game_world.add_collision_pair('ball:flag13', server.ball, None)
    game_world.add_collision_pair('ball:flag14', server.ball, None)
    game_world.add_collision_pair('ball:flag15', server.ball, None)
    game_world.add_collision_pair('ball:flag16', server.ball, None)
    game_world.add_collision_pair('ball:flag17', server.ball, None)
    game_world.add_collision_pair('ball:final', server.ball, None)

    # flag_coordinates = [(2196,776),(2605,1031)]
    # flags = [Flag() for x,y in flag_coordinates]
    server.flag = Flag()
    game_world.add_object(server.flag, 3)
    game_world.add_collision_pair('ball:flag', None, server.flag)

    server.item = Item()
    game_world.add_object(server.item, 3)

    server.final_flag = Final()
    game_world.add_object(server.final_flag, 3)
    game_world.add_collision_pair('ball:final', None, server.final_flag)

    server.flag2 = Flag2()
    game_world.add_object(server.flag2, 3)
    game_world.add_collision_pair('ball:flag2', None, server.flag2)

    server.flag3 = Flag3()
    game_world.add_object(server.flag3, 3)
    game_world.add_collision_pair('ball:flag3', None, server.flag3)

    server.flag4 = Flag4()
    game_world.add_object(server.flag4, 3)
    game_world.add_collision_pair('ball:flag4', None, server.flag4)

    server.flag5 = Flag5()
    game_world.add_object(server.flag5, 3)
    game_world.add_collision_pair('ball:flag5', None, server.flag5)

    server.flag6 = Flag6()
    game_world.add_object(server.flag6, 3)
    game_world.add_collision_pair('ball:flag6', None, server.flag6)

    server.flag7 = Flag7()
    game_world.add_object(server.flag7, 3)
    game_world.add_collision_pair('ball:flag7', None, server.flag7)

    server.flag8 = Flag8()
    game_world.add_object(server.flag8, 3)
    game_world.add_collision_pair('ball:flag8', None, server.flag8)

    server.flag9 = Flag9()
    game_world.add_object(server.flag9, 3)
    game_world.add_collision_pair('ball:flag9', None, server.flag9)

    server.flag10 = Flag10()
    game_world.add_object(server.flag10, 3)
    game_world.add_collision_pair('ball:flag10', None, server.flag10)

    server.flag11 = Flag11()
    game_world.add_object(server.flag11, 3)
    game_world.add_collision_pair('ball:flag11', None, server.flag11)

    server.flag12 = Flag12()
    game_world.add_object(server.flag12, 3)
    game_world.add_collision_pair('ball:flag12', None, server.flag12)

    server.flag13 = Flag13()
    game_world.add_object(server.flag13, 3)
    game_world.add_collision_pair('ball:flag13', None, server.flag13)

    server.flag14 = Flag14()
    game_world.add_object(server.flag14, 3)
    game_world.add_collision_pair('ball:flag14', None, server.flag14)

    server.flag15 = Flag15()
    game_world.add_object(server.flag15, 3)
    game_world.add_collision_pair('ball:flag15', None, server.flag15)

    server.flag16 = Flag16()
    game_world.add_object(server.flag16, 3)
    game_world.add_collision_pair('ball:flag16', None, server.flag16)

    server.flag17 = Flag17()
    game_world.add_object(server.flag17, 3)
    game_world.add_collision_pair('ball:flag17', None, server.flag17)











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



