from pico2d import *
import game_world
import game_framework
import random

import play_mode2
import server
import math

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


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# club Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    @staticmethod
    def enter(club,e):
        club.speed = 0
        club.dir = 0
        
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass
    

class RunRight:
    @staticmethod
    def enter(club,e):
        club.speed = RUN_SPEED_PPS
        club.dir = 0
    
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass
        
    

class RunRightUp:
    @staticmethod
    def enter(club, e):
        club.speed = RUN_SPEED_PPS
        club.dir = math.pi / 4.0
        
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass
        

class RunRightDown:
    @staticmethod
    def enter(club,e):
        club.speed = RUN_SPEED_PPS
        club.dir = -math.pi / 4.0
        
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass
        

class RunLeft:
    @staticmethod
    def enter(club, e):
        club.action = 0
        club.speed = RUN_SPEED_PPS
        club.dir = math.pi
        
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass


class RunLeftUp:
    @staticmethod
    def enter(club, e):
        club.speed = RUN_SPEED_PPS
        club.dir = math.pi * 3.0 / 4.0
        
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass


class RunLeftDown:
    @staticmethod
    def enter(club, e):
        club.speed = RUN_SPEED_PPS
        club.dir = - math.pi * 3.0 / 4.0
        
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass


class RunUp:
    @staticmethod
    def enter(club, e):
        club.speed = RUN_SPEED_PPS
        club.dir = math.pi / 2.0
        
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass


class RunDown:
    @staticmethod
    def enter(club, e):
        club.speed = RUN_SPEED_PPS
        club.dir = - math.pi / 2.0
    
    @staticmethod
    def exit(club, e):
        pass

    @staticmethod
    def do(club):
        pass


class StateMachine:
    def __init__(self, club):
        self.club = club
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
        self.cur_state.enter(self.club, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.club)
        self.club.frame = (self.club.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.club.x += math.cos(self.club.dir) * self.club.speed * game_framework.frame_time
        self.club.y += math.sin(self.club.dir) * self.club.speed * game_framework.frame_time

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.club, e)
                self.cur_state = next_state
                self.cur_state.enter(self.club, e)
                return True

        return False


class Club:
    image = None

    def __init__(self):

        self.image = load_image('golf_club.png')
        self.frame = 0
        self.x = server.boy.x - 50
        self.y = server.boy.y
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())



    def update(self):
        self.state_machine.update()
        self.x = clamp(50, self.x, server.background.w - 50)
        self.y = clamp(50, self.y, server.background.h - 50)
        pass

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 15, sy - 15, sx + 15, sy + 15

    def handle_collision(self, group, other):
        match group:
            case 'club:ball':
                print('타격!')

