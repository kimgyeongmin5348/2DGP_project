from pico2d import *
import game_world
import game_framework
import random

import server


class Flag:
    image = None

    def __init__(self, x=None, y=None):
        if Flag.image == None:
            Flag.image = load_image('flag.png')
        self.x = 670
        self.y = 950

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy)



    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 10, sy - 10, sx + 10, sy + 10

    def handle_collision(self, group, other):
        match group:
            case 'ball:flag':
                print('다음 필드로!')
