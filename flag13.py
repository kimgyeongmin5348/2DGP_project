from pico2d import *
import game_world
import game_framework
import random
import server


class Flag13:
    image = None

    def __init__(self, x=None, y=None):
        if Flag13.image == None:
            Flag13.image = load_image('flag.png')
        self.x, self.y = 1152, 2155

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
        return sx - 10, sy - 25, sx + 10, sy + 27

    def handle_collision(self, group, other):
        match group:
            case 'ball:flag13':
                server.ball.tx = 1230
                server.ball.ty = 1944
                server.ball.ball_in_hole.play()
                server.boy.ball_count = 0
                print('다음 필드로!')


