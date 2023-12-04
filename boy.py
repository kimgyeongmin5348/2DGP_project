import math

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    SDLK_UP, SDLK_DOWN, \
    draw_rectangle, get_events, load_music, load_wav
from sdl2 import SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_MOUSEBUTTONUP, SDL_QUIT, SDLK_1, SDLK_2, SDLK_a, SDLK_d, \
    SDLK_w, SDLK_s

from ball import Ball
import game_world
import game_framework
import server
from club import Club1
from club import Club2



# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def upkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def upkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w


def downkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def downkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def left_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT


def left_click_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP and e[1].button == SDL_BUTTON_LEFT

def time_out(e):
    return e[0] == 'TIME_OUT'



# time_out = lambda e : e[0] == 'TIME_OUT'


# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Idle:

    @staticmethod
    def enter(boy, e):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.speed = 0
        boy.dir = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class RunRight:
    @staticmethod
    def enter(boy, e):
        boy.action = 1
        boy.speed = RUN_SPEED_PPS
        boy.dir = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class RunRightUp:
    @staticmethod
    def enter(boy, e):
        boy.action = 1
        boy.speed = RUN_SPEED_PPS
        boy.dir = math.pi / 4.0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class RunRightDown:
    @staticmethod
    def enter(boy, e):
        boy.action = 1
        boy.speed = RUN_SPEED_PPS
        boy.dir = -math.pi / 4.0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class RunLeft:
    @staticmethod
    def enter(boy, e):
        boy.action = 0
        boy.speed = RUN_SPEED_PPS
        boy.dir = math.pi

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class RunLeftUp:
    @staticmethod
    def enter(boy, e):
        boy.action = 0
        boy.speed = RUN_SPEED_PPS
        boy.dir = math.pi * 3.0 / 4.0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class RunLeftDown:
    @staticmethod
    def enter(boy, e):
        boy.action = 0
        boy.speed = RUN_SPEED_PPS
        boy.dir = - math.pi * 3.0 / 4.0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class RunUp:
    @staticmethod
    def enter(boy, e):
        if boy.action == 2:
            boy.action = 0
        elif boy.action == 3:
            boy.action = 1
        boy.speed = RUN_SPEED_PPS
        boy.dir = math.pi / 2.0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class RunDown:
    @staticmethod
    def enter(boy, e):
        if boy.action == 2:
            boy.action = 0
        elif boy.action == 3:
            boy.action = 1
        boy.speed = RUN_SPEED_PPS
        boy.dir = - math.pi / 2.0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class Swing:
    @staticmethod
    def enter(boy, e):
        boy.action = 1
        boy.dir = 0
        boy.swing_x, boy.swing_y = e[1].x + server.background.window_left , 721 - e[1].y + server.background.window_bottom
        print(f'swing 좌표 ({boy.swing_x}, {boy.swing_y})')
        boy.swing_sound = load_wav('hit.wav')
        boy.swing_sound.set_volume(32)
        boy.swing_sound.play()


    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft, upkey_down: RunUp,
                   downkey_down: RunDown, upkey_up: RunDown, downkey_up: RunUp, left_click: Swing},
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
            RunRightDown: {right_up: RunDown, downkey_up: RunRight, left_down: RunDown, upkey_down: RunRight},
            Swing: {left_click_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.boy.x += math.cos(self.boy.dir) * self.boy.speed * game_framework.frame_time
        self.boy.y += math.sin(self.boy.dir) * self.boy.speed * game_framework.frame_time

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False



class Boy:
    def __init__(self):
        self.frame = 0
        self.action = 3
        self.ball_count = 0
        self.image = load_image('animation_sheet.png')
        self.font = load_font('ENCR10B.TTF', 24)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.x = 3300
        self.y = 628
        self.item = None

        self.swing_x = 3040
        self.swing_y = 646

    def update(self):
        self.state_machine.update()
        self.x = clamp(50, self.x, server.background.w - 50)
        self.y = clamp(50, self.y, server.background.h - 50)
        # fill here

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        # sx = server.background.cw // 2
        # sy = server.background.ch // 2

        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame)*100, self.action * 100, 100, 100, sx, sy)  # 이건 처음에 다 100이었음
        self.font.draw(sx - 10, sy + 60, f'{self.ball_count}', (0, 0, 255))
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 20, sy - 50, sx + 20, sy + 50

    def clubs(self):
        if self.item == 'Club1':
            club = Club1()
            game_world.add_object(club)
        elif self.item == 'Club2':
            club = Club2()
            game_world.add_object(club)

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            self.ball_count += 1
            self.x = server.ball.x + 50

            print('턴 시작!')

