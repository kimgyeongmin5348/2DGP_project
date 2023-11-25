from pico2d import load_image


class Ground:
    def __init__(self):
        self.image = load_image('map1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1280//2,721//2)
