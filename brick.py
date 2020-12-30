# brick.py


import random
from colors import COLORS




class RandomBrick:
    DIMENSION = 4

    # Tetriminos
    _BRICKS = [
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

    _DEFAULT_ROTATION_DIRECTION = -1

    def __init__(self):
        self._type = random.randint(0, len(self._BRICKS) - 1)
        self._variants = self._BRICKS[self._type][1]
        self._variant = 0

    def get_name(self):
        return self._BRICKS[self._type][0]

    def get_dimension():
        return self._BRICK_DIMENSION

    def get_colorindex(self):
        return (self._type % (len(COLORS) - 1)) + 1

    def get_points(self):
        return self._variants[self._variant]

    def _rotate(self, direction):
        """returns if actually rotated"""

        if len(self._variants) > 1:
            self._variant = (self._variant + direction) % len(self._variants)
            return True

        return False

    def rotate_ahead(self):
        return self._rotate(self._DEFAULT_ROTATION_DIRECTION)

    def rotate_aback(self):
        return self._rotate(-self._DEFAULT_ROTATION_DIRECTION)
