from pico2d import *
import game_world
import game_framework
import random


import server2


class Flag2:
    image = None

    def __init__(self, x=None, y=None):
        if Flag2.image == None:
            Flag2.image = load_image('flag.png')
        self.x = 670
        self.y = 950

    def draw(self):
        sx = self.x - server2.background2.window_left
        sy = self.y - server2.background2.window_bottom
        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())



    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server2.background2.window_left
        sy = self.y - server2.background2.window_bottom
        return sx - 10, sy - 37, sx + 10, sy + 37

    def handle_collision(self, group, other):
        match group:
            case 'ball:flag':
                print('다음 필드로!')

