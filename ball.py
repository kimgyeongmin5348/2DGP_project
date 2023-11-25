from pico2d import *
import game_world
import game_framework
import random

import server

class Ball:
    image = None

    def __int__(self, x=None, y=None):
        if Ball.image == None:
            Ball.image = load_image('ball.png')
        self.x = x if x else random.randint(1, server.background.w)
        self.y = y if y else random.randint(1, server.background.h)

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
            case 'mario:ball':
                game_world.remove_object(self)