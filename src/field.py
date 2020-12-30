# field.py

import pygame
from colors import COLORS

# simple wrapper for rect/color pairs
class _ColoredRectangle:
    def __init__(self, rectangle, colorindex):
        self.rectangle = rectangle
        self.colorindex = colorindex


class GameField:
    def __init__(self, screen, columns, rows, length):
        self._screen = screen
        self._columns = columns
        self._rows = rows

        x_offset = int((screen.get_width() / length - columns) / 2 * length)
        y_offset = int((screen.get_height() / length - rows) / 2 * length)

        self._field = [[
            _ColoredRectangle(pygame.Rect(x_offset + length * x, y_offset + length * y, length, length), 0)
            for x in range(columns)]
            for y in range(rows)]

    def get_columns(self):
        return self._columns

    def draw_grid(self):
        for x in range(self._columns):
            for y in range(self._rows):
                cell = self._field[y][x]
                color = COLORS[cell.colorindex]
                border_only = 0 if cell.colorindex else 1
                pygame.draw.rect(self._screen, color, cell.rectangle, border_only)

    def draw_figure(self, figure):
        for x, y in figure.get_xy_coordinates():
            pygame.draw.rect(self._screen, COLORS[figure.get_colorindex()], self._field[y][x].rectangle, 0)

    def collides(self, figure):
        for x, y in figure.get_xy_coordinates():
            # check grid boundaries
            if not (0 <= x < self._columns and 0 <= y < self._rows):
                return True
            # check freezed figures
            if self._field[y][x].colorindex != 0:
                return True

        return False

    def freeze_figure(self, figure):
        colorindex = figure.get_colorindex()
        for x, y in figure.get_xy_coordinates():
            self._field[y][x].colorindex = colorindex
    
    def resolve_lines(self):
        lines = 0
        for y1 in range(self._rows):
            if all(self._field[y1][x].colorindex != 0 for x in range(self._columns)):
                # copy down
                for y2 in range(y1, 1, -1):
                    for x in range(self._columns):
                        self._field[y2][x].colorindex = self._field[y2 - 1][x].colorindex
                
                # empty first line
                for x in range(self._columns):
                    self._field[0][x].colorindex = 0

                lines += 1
        
        return lines