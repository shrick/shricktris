# figure.py


import random
from brick import Brick


def generate_randomized_figures(game_field):
    """Generates figures using randomized bags"""

    brick_count = len(Brick.BRICKS)
    bag = []

    while True:
        if not bag:
            bag = random.sample(range(brick_count), brick_count)
        yield Figure(game_field, Brick(bag.pop()))


class Figure:
    def __init__(self, game_field, brick):
        self._game_field = game_field
        self._brick = brick
        self._x = int((self._game_field.get_columns() - self._brick.DIMENSION) / 2)
        self._y = 0
        self._freezed = False
    
    def get_name(self):
        return self._brick.get_name()

    def get_colorindex(self):
        return self._brick.get_colorindex()

    def get_xy_coordinates(self):
        return ((int(self._x + (p %  self._brick.DIMENSION)), int(self._y + (p / self._brick.DIMENSION)))
            for p in self._brick.get_points())
    
    def _step(self, dx=0, dy=0):
        """return if step was actually done (no collosion detected)"""

        x, y = self._x, self._y
        self._x += dx
        self._y += dy

        if self._game_field.collides(self):
            self._x, self._y = x, y
            return False
        
        return True

    def step_down(self):
        if not self._step(dy=+1):
            self._freeze()
    
    def step_left(self):
        self._step(dx=-1)

    def step_right(self):
        self._step(dx=+1)

    def fall_down(self):
        while self._step(dy=+1):
            pass

    def rotate(self):
        if self._brick.rotate_ahead():
            if self._game_field.collides(self):
                self._brick.rotate_aback()

    def _freeze(self):
        self._game_field.freeze_figure(self)
        self._freezed = True

    def is_freezed(self):
        return self._freezed