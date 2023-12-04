from pico2d import *
import game_world
import game_framework
import random

import last_mode
import server


class Final:
    image = None

    def __init__(self, x=None, y=None):
        if Final.image == None:
            Final.image = load_image('flag.png')
        self.x, self.y = 3295, 1284
        self.bgm = load_music('last_music.mp3')
        self.bgm.set_volume(32)

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
            case 'ball:final':
                server.ball.ball_in_hole.play()
                server.background.bgm.stop()
                game_framework.change_mode(last_mode)
                self.bgm.repeat_play()
                server.ball.x = 100
                server.ball.x = 100

                print('필드 종료')


