from pico2d import load_image, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, draw_rectangle, get_events
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

animation_names = ['Walk', 'Idle']


class Ball:
    images = None

    def load_images(self):
        if Ball.images == None:
            Ball.images = {}
            for name in animation_names:
                Ball.images[name] = [load_image("./ball/" + name + " (%d)" % i + ".png") for i in range(1, 11)]
            Ball.marker_image = load_image('target.png')

    def __init__(self, x=610, y=120, size=0.5):
        self.x = x
        self.y = y
        self.size = size
        self.load_images()
        self.dir = 0.0
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        # self.build_behavior_tree()
        self.loc_no = 0
        self.state = 'Idle'
        self.tx = 610
        self.ty = 120
        self.distance_far = 1000
        self.base_size = size
        self.target_size = size * 1.5
        self.current_size = self.base_size
        self.size_change_speed = (self.target_size - self.base_size) / BALL_SPEED_PPS  # 크기 변화 속도

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        if math.cos(self.dir) < 0:
            Ball.images[self.state][int(self.frame)].composite_draw(0, 'h', sx, sy)
        else:
            Ball.images[self.state][int(self.frame)].draw(sx, sy)
        # draw_rectangle(*self.get_bb())
        self.marker_image.draw(self.tx - server.background.window_left,
                               self.ty - server.background.window_bottom, 30, 30)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # self.bt.run()

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 7, sy - 7, sx + 7, sy + 7

    def handle_collision(self, group, other):
        match group:
            case 'boy:ball':
                # self.x = self.x + 10
                self.state = 'Idle'
                self.dir = math.atan2(self.y - server.boy.y, self.x - server.boy.x)
                self.speed = BALL_SPEED_PPS
                self.x += math.cos(self.dir) * self.speed * game_framework.frame_time
                self.y += math.sin(self.dir) * self.speed * game_framework.frame_time

                self.distance_far -= self.speed * game_framework.frame_time
                # if self.distance_far <= 0:
                #     self.state = 'Idle'
                #     print('성공')

                print('n번째 턴')
            case 'ball:flag':
                print('다음 필드로!')

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance < (PIXEL_PER_METER * r) ** 2

    # def fly(self):
    #     self.state = 'Idle'
    #     self.dir = math.atan2(self.y - server.boy.y, self.x - server.boy.x)
    #     self.speed = BALL_SPEED_PPS
    #     self.x += math.cos(self.dir) * self.speed * game_framework.frame_time
    #     self.y += math.sin(self.dir) * self.speed * game_framework.frame_time
    #
    #     self.distance_far -= self.speed * game_framework.frame_time
    #     if self.distance_far <= 0:
    #         return BehaviorTree.SUCCESS
    #
    #     return BehaviorTree.RUNNING
    #
    # def is_boy_nearby(self, distance):
    #     return self.distance_less_than(server.boy.x, server.boy.y, self.x, self.y, distance)
    #
    #
    # def handle_events(self):
    #     pass
    #
    # def build_behavior_tree(self):
    #     # c1 = Condition('클럽이 공을침', self.is_boy_nearby, 1)
    #     # a1 = Action('공이 움직인다', self.fly)
    #     # root = SEQ_move_to_target = Sequence('목표 위치로 이동', c1, a1)
    #     #
    #     # self.bt = BehaviorTree(root)
    #     pass
