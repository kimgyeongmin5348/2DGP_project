from pico2d import *
import game_world
import game_framework
import random

import play_mode2
import server


class Club:
    image = None

    def __init__(self, x=None, y=None):
        if Club.image == None:
            Club.image = load_image('golf_club.png')
        self.x = 300
        self.y = 300

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())



    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 10, sy - 10, sx + 10, sy + 10

    def handle_collision(self, group, other):
        match group:
            case 'club:ball':
                print('타격!')

