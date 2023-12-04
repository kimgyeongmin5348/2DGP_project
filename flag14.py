from pico2d import *
import game_world
import game_framework
import random
import server


class Flag14:
    image = None

    def __init__(self, x=None, y=None):
        if Flag14.image == None:
            Flag14.image = load_image('flag.png')
        self.x, self.y = 893, 2066

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy)
        # draw_rectangle(*self.get_bb())



    def update(self):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 10, sy - 25, sx + 10, sy + 27

    def handle_collision(self, group, other):
        match group:
            case 'ball:flag14':
                server.ball.tx = 674
                server.ball.ty = 1958
                server.ball.ball_in_hole.play()
                server.boy.ball_count = 0
                print('다음 필드로!')


