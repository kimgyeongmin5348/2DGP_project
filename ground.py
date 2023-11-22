from pico2d import load_image


class Ground:
    def __init__(self):
        self.image = load_image('map1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1820//2,1000//2)
