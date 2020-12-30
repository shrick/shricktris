# figure.py


from brick import RandomBrick, BRICK_DIMENSION, ROTATION_OFFSET


class RandomFigure:
    def __init__(self, game_field):
        self._game_field = game_field
        self._brick = RandomBrick()
        self._x = int((self._game_field.get_columns() - BRICK_DIMENSION) / 2)
        self._y = 0
        self._freezed = False
    
    def get_name(self):
        return self._brick.get_name()

    def get_colorindex(self):
        return self._brick.get_colorindex()

    def get_xy_coordinates(self):
        return ((int(self._x + (p %  BRICK_DIMENSION)), int(self._y + (p / BRICK_DIMENSION)))
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
        if self._brick.rotate(ROTATION_OFFSET):
            if self._game_field.collides(self):
                self._brick.rotate(-ROTATION_OFFSET)

    def _freeze(self):
        self._game_field.freeze_figure(self)
        self._freezed = True

    def is_freezed(self):
        return self._freezed