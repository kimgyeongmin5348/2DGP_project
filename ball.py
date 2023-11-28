from pico2d import load_image, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, draw_rectangle
from sdl2 import SDL_MOUSEBUTTONUP

import game_world
import game_framework
import random
import math
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
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
        self.dir = 0.0
        self.speed = 0.0
        self.build_behavior_tree()
        self.loc_no = 0
        self.is_moving = False
        self.destination_y = 0
        self.tx, self.ty = 2000, 2000

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

    def set_target_location(self, x = None, y = None):
        if not x or not y:
            raise ValueError('위치를 지정해야 합니다.')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.dir = math.atan2(ty - sy, tx - sx)
        self.speed = BALL_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time


    def move_to(self, r = 0.5):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, sx, sy, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def handle_events(self, events):
        for event in events:
            if event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
                self.tx, self.ty = event.x, event.y
        return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
        a1 = Action('목표지점을 입력', self.handle_events)
        a2 = Action('공이 움직인다', self.move_to)
        root = SEQ_move_to_target = Sequence('목표 위치로 이동', a1, a2)

        self.bt = BehaviorTree(root)
