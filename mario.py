import math

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    SDLK_UP, SDLK_DOWN, \
    draw_rectangle

import game_world
import game_framework
import server


# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def upkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def upkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def downkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def downkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# mario Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Idle:

    @staticmethod
    def enter(mario, e):
        if mario.action == 0:
            mario.action = 2
        elif mario.action == 1:
            mario.action = 3
        mario.speed = 0
        mario.dir = 0
        pass

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class RunRight:
    @staticmethod
    def enter(mario, e):
        mario.action = -1
        mario.speed = RUN_SPEED_PPS
        mario.dir = 0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class RunRightUp:
    @staticmethod
    def enter(mario, e):
        mario.action = 1
        mario.speed = RUN_SPEED_PPS
        mario.dir = math.pi / 4.0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class RunRightDown:
    @staticmethod
    def enter(mario, e):
        mario.action = 1
        mario.speed = RUN_SPEED_PPS
        mario.dir = -math.pi / 4.0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class RunLeft:
    @staticmethod
    def enter(mario, e):
        mario.action = 0
        mario.speed = RUN_SPEED_PPS
        mario.dir = math.pi

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class RunLeftUp:
    @staticmethod
    def enter(mario, e):
        mario.action = 0
        mario.speed = RUN_SPEED_PPS
        mario.dir = math.pi * 3.0 / 4.0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class RunLeftDown:
    @staticmethod
    def enter(mario, e):
        mario.action = 0
        mario.speed = RUN_SPEED_PPS
        mario.dir = - math.pi * 3.0 / 4.0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class RunUp:
    @staticmethod
    def enter(mario, e):
        if mario.action == 2:
            mario.action = 0
        elif mario.action == 3:
            mario.action = 1
        mario.speed = RUN_SPEED_PPS
        mario.dir = math.pi / 2.0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class RunDown:
    @staticmethod
    def enter(mario, e):
        if mario.action == 2:
            mario.action = 0
        elif mario.action == 3:
            mario.action = 1
        mario.speed = RUN_SPEED_PPS
        mario.dir = - math.pi / 2.0
        pass

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass


class StateMachine:
    def __init__(self, mario):
        self.mario = mario
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft, upkey_down: RunUp,
                   downkey_down: RunDown, upkey_up: RunDown, downkey_up: RunUp},
            RunRight: {right_up: Idle, left_down: Idle, upkey_down: RunRightUp, upkey_up: RunRightDown,
                       downkey_down: RunRightDown, downkey_up: RunRightUp},
            RunRightUp: {upkey_up: RunRight, right_up: RunUp, left_down: RunUp, downkey_down: RunRight},
            RunUp: {upkey_up: Idle, left_down: RunLeftUp, downkey_down: Idle, right_down: RunRightUp,
                    left_up: RunRightUp, right_up: RunLeftUp},
            RunLeftUp: {right_down: RunUp, downkey_down: RunLeft, left_up: RunUp, upkey_up: RunLeft},
            RunLeft: {left_up: Idle, upkey_down: RunLeftUp, right_down: Idle, downkey_down: RunLeftDown,
                      upkey_up: RunLeftDown, downkey_up: RunLeftUp},
            RunLeftDown: {left_up: RunDown, downkey_up: RunLeft, upkey_down: RunLeft, right_down: RunDown},
            RunDown: {downkey_up: Idle, left_down: RunLeftDown, upkey_down: Idle, right_down: RunRightDown,
                      left_up: RunRightDown, right_up: RunLeftDown},
            RunRightDown: {right_up: RunDown, downkey_up: RunRight, left_down: RunDown, upkey_down: RunRight}
        }

    def start(self):
        self.cur_state.enter(self.mario, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.mario)
        self.mario.frame = (self.mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.mario.x += math.cos(self.mario.dir) * self.mario.speed * game_framework.frame_time
        self.mario.y += math.sin(self.mario.dir) * self.mario.speed * game_framework.frame_time

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.mario, e)
                self.cur_state = next_state
                self.cur_state.enter(self.mario, e)
                return True

        return False


class Mario:
    def __init__(self):
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.x = server.background.w // 2
        self.y = server.background.h // 2

    def update(self):
        self.state_machine.update()
        self.x = clamp(50, self.x, server.background.w - 50)
        self.y = clamp(50, self.y, server.background.h - 50)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * 100, self.action * 100, 100, 100, sx, sy)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 20, sy - 50, sx + 20, sy + 50

