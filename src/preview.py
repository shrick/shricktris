# preview.py


import pygame
from colors import COLORS


class Preview:
    def __init__(self, screen, x_offset, y_offset, dimension, length):
        self._screen = screen
        self._dimension = dimension
        self._rects = [[
            pygame.Rect(x_offset + length * x, y_offset + length * y, length, length)
            for x in range(dimension)]
            for y in range(dimension)]

    def draw_figure(self, figure):
        color = COLORS[figure.get_colorindex()]
        for x, y in figure.get_plain_coordinates():
            if x < self._dimension and y < self._dimension:
                pygame.draw.rect(self._screen, color, self._rects[y][x], 0)
