# figure.py

import random
from colors import COLORS


# Tetriminos
FIGURE_DIMENSION = 4
FIGURES = [
    # O (yellow)
    [ "O", ((5, 6, 9, 10),) ],
    # I (cyan)
    [ "I", ((4, 5, 6, 7), (1, 5, 9, 13)) ],
    # L (orange)
    [ "L", ((2, 4, 5, 6), (1, 5, 9, 10), (4, 5, 6, 8), (1, 2, 6, 10)) ],
    # J (blue)
    [ "J", ((5, 9, 10, 11), (1, 2, 5, 9), (4, 5, 6, 10), (2, 6, 9, 10)) ],
    # T (purple)
    [ "T", ((2, 5, 6, 7), (2, 6, 7, 10), (5, 6, 7, 10), (2, 5, 6, 10)) ],
    # S (green)
    [ "S", ((6, 7, 9, 10), (1, 5, 6, 10)) ],
    # Z (red)
    [ "Z", ((5, 6, 10, 11), (2, 5, 6, 9)) ],
]
ROTATION_OFFSET = -1


class RandomFigure:
    def __init__(self, game_field):
        self._game_field = game_field
        self._type = random.randint(0, len(FIGURES) - 1)
        self._variants = FIGURES[self._type][1]
        self._variant = 0
        self._x = int((self._game_field.get_columns() - FIGURE_DIMENSION) / 2)
        self._y = 0
        self._freezed = False
    
    def get_name(self):
        return FIGURES[self._type][0]

    def get_colorindex(self):
        return (self._type % (len(COLORS) - 1)) + 1

    def get_xy_coordinates(self):
        return ((int(self._x + (p %  FIGURE_DIMENSION)), int(self._y + (p / FIGURE_DIMENSION)))
            for p in self._variants[self._variant])
    
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

    def _switch_variant(self, direction):
        """returns if actually rotated"""

        if len(self._variants) > 1:
            self._variant = (self._variant + direction) % len(self._variants)
            return True
        
        return False

    def rotate(self):
        if self._switch_variant(ROTATION_OFFSET):
            if self._game_field.collides(self):
                self._switch_variant(-ROTATION_OFFSET)

    def _freeze(self):
        self._game_field.freeze_figure(self)
        self._freezed = True

    def is_freezed(self):
        return self._freezed