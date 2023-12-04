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
        self.x, self.y = 2196, 776
        self.font = load_font('Super Comic.ttf', 50)

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
            case 'ball:flag':
                server.ball.tx = 2210
                server.ball.ty = 885
                if server.boy.ball_count == 0:
                    self.font.draw(self.x - 30, self.y, 'BOGEY', (0, 255, 0))
                print('다음 필드로!')


