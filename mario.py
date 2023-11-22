# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

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

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE




class Idle:

    @staticmethod
    def enter(mario, e):
        if mario.face_dir == -1:
            mario.action = 2
        elif mario.face_dir == 1:
            mario.action = 3
        mario.dir = 0
        mario.frame = 0
        mario.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % 8
        if get_time() - mario.wait_time > 2:
            mario.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(mario):
        mario.image.clip_draw(mario.frame * 100, mario.action * 207, 23, 37, mario.x, mario.y)



class Run:

    @staticmethod
    def enter(mario, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            mario.dir, mario.face_dir, mario.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            mario.dir, mario.face_dir, mario.action = -1, -1, 0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % 8
        mario.x += mario.dir * 5
        pass

    @staticmethod
    def draw(mario):
        mario.image.clip_draw(mario.frame * 100, mario.action * 100, 100, 100, mario.x, mario.y)


class StateMachine:
    def __init__(self, mario):
        self.mario = mario
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
        }

    def start(self):
        self.cur_state.enter(self.mario, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.mario)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.mario, e)
                self.cur_state = next_state
                self.cur_state.enter(self.mario, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.mario)





class Mario:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.face_dir = 1
        self.image = load_image('mario_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
