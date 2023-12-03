from pico2d import *
import game_world
import game_framework
import random

import server


class Item:
    image = None

    def __init__(self, x=None, y=None):
        if Item.image == None:
            Item.image = load_image('club.jpg')

        self.x = 50
        self.y = 50

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass
