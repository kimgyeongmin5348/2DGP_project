import random
import server
from pico2d import *



class FixedBackground:

    def __init__(self):
        self.image = load_image('Map.png')
        self.cw = get_canvas_width()  # 화면의 너비
        self.ch = get_canvas_height()  # 화면의 높이
        self.w = self.image.w  # 이미지의 너비
        self.h = self.image.h  # 이미지의 높이
        self.bgm = load_music('backsound.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
        pass

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom, self.cw, self.ch,
            0, 0
        )
        pass

    def update(self):
        self.window_left = int(server.boy.x) - self.cw//2
        self.window_bottom = int(server.boy.y) - self.ch//2

        self.window_left = clamp(0, self.window_left, self.w - self.cw - 1)
        self.window_bottom = clamp(0, self.window_bottom, self.h - self.ch - 1)
        pass

    def handle_event(self, event):
        pass



    def handle_event(self, event):
        pass
