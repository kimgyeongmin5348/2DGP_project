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

    def __init__(self, x=610, y=120, size = 0.5):
        self.x = x
        self.y = y
        self.size = size
        self.load_images()
        self.dir = 0.0
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.build_behavior_tree()
        self.loc_no = 0
        self.state = 'Idle'
        self.tx = 610
        self.ty = 120
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
        self.bt.run()



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

    def set_target_location(self):
        events = get_events()
        for event in events:
            if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                self.tx, self.ty = event.x - server.background.window_left, event.y - server.background.window_bottom
                return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = BALL_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time


    def move_to(self, r = 0.5):
        self.state = 'Idle'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            self.current_size = self.base_size
            return BehaviorTree.SUCCESS
        else:
            self.current_size += self.size_change_speed * game_framework.frame_time
            self.current_size = min(self.current_size, self.target_size)
            return BehaviorTree.RUNNING


    def handle_events(self):
        pass



    def build_behavior_tree(self):
        a1 = Action('목표지점을 입력', self.set_target_location)
        a2 = Action('공이 움직인다', self.move_to)
        root = SEQ_move_to_target = Sequence('목표 위치로 이동', a1, a2)

        self.bt = BehaviorTree(root)
