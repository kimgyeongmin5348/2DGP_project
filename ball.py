from pico2d import load_image, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, draw_rectangle

import game_world
import game_framework
import random
import math

import server


ball_speed = 20.0

PIXEL_PER_METER = (10.0 / 0.3)
BALL_SPEED_KMPH = ball_speed
BALL_SPEED_MPM = (BALL_SPEED_KMPH * 1000.0 / 60.0)
BALL_SPEED_MPS = (BALL_SPEED_MPM / 60.0)
BALL_SPEED_PPS = (BALL_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Ball:
    image = None

    def __init__(self, x=None, y=None):
        self.image = load_image('ball.png')
        self.x = 610
        self.y = 120
        self.is_moving = False
        self.destination_y = 0

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy)
        # draw_rectangle(*self.get_bb())

    def update(self):
        if self.is_moving:
            distance = BALL_SPEED_PPS * game_framework.frame_time
            if self.y < self.destination_y:
                self.y = min(self.y + distance, self.destination_y)
            else:
                self.is_moving = False


    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 7, sy - 7, sx + 7, sy + 7

    def handle_collision(self, group, other):
        match group:
            case 'boy:ball':
                self.x = self.x + 10

                print('n번째 턴')
            case 'ball:flag':
                print('다음 필드로!')

    def handle_events(self, events):
        for event in events:
            if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                if not self.is_moving:
                    self.start_moving()

    def start_moving(self):
        self.is_moving = True
        self.destination_y = self.y + BALL_SPEED_PPS * 5
