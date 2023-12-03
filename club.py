from pico2d import *
import game_world
import game_framework
import random

import play_mode
import server


class Club1:
    image = None

    def __init__(self):
        if Club1.image == None:
            Club1.image = load_image('club1.png')
        self.x = server.ball.x
        self.y = server.ball.y

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy)

    def update(self):
        pass


class Club2:
    image = None

    def __init__(self):
        if Club2.image == None:
            Club2.image = load_image('club2.png')
        self.x = server.boy.x
        self.y = server.boy.y

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy)

    def update(self):
        pass
