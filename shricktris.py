#!/usr/bin/env python3

import pygame
import random
import collections

SYNOPSIS = """Keyboard keys to control game:
  
  Pause         pause/continue
  q             quit
  +             speed up
  -             speed down
  
  Cursor left   move left
         right  move right
         down   move down
         up     rotate
  Space         fall down
"""

GAME_TITLE = "Shricktris"
MIN_FPS = 1
MAX_FPS = 24
START_FPS = 12
START_GAME_STEPOVER = 8
SCREEN_RESOLUTION = (600, 800)
GRID_COLUMNS = 16
GRID_ROWS = 30

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

YELLOW  = (240, 240, 20)
CYAN    = (20, 240, 240)
ORANGE  = (240, 140, 0)
BLUE    = (0, 0, 240)
PURPLE  = (120, 0, 120)
GREEN   = (0, 240, 0)
RED     = (240, 0, 0)

COLORS = [
    GRAY,       # grid
    YELLOW,     # 0
    CYAN,       # I
    ORANGE,     # L
    BLUE,       # J
    PURPLE,     # T
    GREEN,      # S
    RED,        # Z
]


class Control:
    def __init__(self, fps):
        self._clock = pygame.time.Clock()
        self._to_quit = False
        self._keystates = {}

        self._fps = 0
        self.adjust_fps(fps)
        
    def process_events(self):
        self._clock.tick(self._fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._to_quit = True
            elif event.type == pygame.KEYDOWN:                
                self._keystates[event.key] = True
            elif event.type == pygame.KEYUP:
                self._keystates[event.key] = False

    def adjust_fps(self, dfps):
        self._fps = max(min(self._fps + dfps, MAX_FPS), MIN_FPS)
        print("[DEBUG] fps = " + str(self._fps))
        
    def _is_pressed(self, keys):
        return all(k in self._keystates and self._keystates[k] for k in keys)

    def quit(self):
        return self._to_quit or self._is_pressed([pygame.K_q])
    
    def pause(self):
        return self._is_pressed([pygame.K_PAUSE])

    def step_left(self):
        return self._is_pressed([pygame.K_LEFT])

    def step_right(self):
        return self._is_pressed([pygame.K_RIGHT])

    def step_down(self):
        return self._is_pressed([pygame.K_DOWN])

    def fall_down(self):
        return self._is_pressed([pygame.K_SPACE])

    def rotate(self):
        return self._is_pressed([pygame.K_UP])

    def speed_up(self):
        return self._is_pressed([pygame.K_PLUS])

    def speed_down(self):
        return self._is_pressed([pygame.K_MINUS])


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
    

# simple wrapper for rect/color pairs
class ColoredRectangle:
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
            ColoredRectangle(pygame.Rect(x_offset + length * x, y_offset + length * y, length, length), 0)
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


class Score:
    def __init__(self):
        self.lines = []
        self.last_bonus = 0
        self.score = 0
    
    def add_lines(self, lines):
        self.lines.append(lines)
        self.last_bonus = lines ** 2
        self.score += self.last_bonus

    def print_current_score(self):
        lines = self.lines[-1] if self.lines else 0
        print("Score: {} (+{} point{} for {} line{})".format(
            self.score, 
            self.last_bonus, "" if self.last_bonus == 1 else "s",
            lines, "" if  lines == 1 else "s"))
    
    def print_final_score(self):
        lines = sum(self.lines)
        print("Final score: {} ({} resolved line{})".format(
            self.score, 
            lines, "" if lines == 1 else "s"))
        

class Game:
    def __init__(self):
        # init pygame components
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self._screen = pygame.display.set_mode(SCREEN_RESOLUTION)
        self._background = pygame.Surface(self._screen.get_size()).convert()
        self._background.fill(WHITE)

        # init game components
        self._field = GameField(self._screen, GRID_COLUMNS, GRID_ROWS, 20)
        self._figure = RandomFigure(self._field)
        self._next_figure = RandomFigure(self._field)
        self._score = Score()
        self._control = Control(START_FPS)

        # init speed and game state
        self._stepover = START_GAME_STEPOVER
        self._nostep = self._stepover
        self._looping = True
        self._stopped = False
        self._paused = True

    def _adjust_speed(self, delta):
        old_stepover = self._stepover
        self._stepover = max(self._stepover + delta, 1)

        if self._stepover != old_stepover:
            print("[DEBUG] game_stepover = " + str(self._stepover))

    def _check_states(self):
        # game speed
        if self._control.speed_up():
            self._adjust_speed(-1)
        
        if self._control.speed_down():
            self._adjust_speed(+1)
        
        # game state
        if self._control.pause():
            self._paused = not self._paused
            if self._paused:
                print("Press PAUSE key continue.")
            else:
                print("Press PAUSE key to pause again.")
        
        if self._control.quit():
            print("Quitting...")
            self._looping = False

    def _move_figure(self):
        if self._control.step_left():
            self._figure.step_left()
        if self._control.step_right():
            self._figure.step_right()
        if self._control.step_down():
            self._figure.step_down()
        if self._control.fall_down():
            self._figure.fall_down()
        if self._control.rotate():
            self._figure.rotate()
        
    def _advance(self):
        # force step down
        self._figure.step_down()
        
        # resolve lines
        lines = self._field.resolve_lines()
        if lines:
            self._score.add_lines(lines)
            self._score.print_current_score()
            # increase game speed
            self._stepover = max(self._stepover - 1, 1)
            print("[DEBUG] game_stepover = " + str(self._stepover))
        
        # spawn new figure
        if self._figure.is_freezed():
            self._figure = self._next_figure
            if self._field.collides(self._figure):
                self._stopped = True
                print("Game finished.")
                self._score.print_final_score()
            else:
                self._next_figure = RandomFigure(self._field)
                print("Next figure: " + self._next_figure.get_name())

    def _draw(self):
        self._screen.blit(self._background, (0, 0))
        self._field.draw_grid()

        if self._stopped:
            # hack in some flickering
            self._nostep =  (self._nostep + 1) % 3
            if not self._nostep:
                self._field.draw_figure(self._figure)
        else:
            self._field.draw_figure(self._figure)
        
        pygame.display.update()

    def loop(self):
        print("Press PAUSE key to start!")
        
        while self._looping:
            self._control.process_events()
            self._check_states()
            
            if not self._paused and not self._stopped:
                self._move_figure()

                self._nostep =  (self._nostep + 1) % self._stepover
                if not self._nostep:
                    self._advance()
            
            self._draw()
        
        if not self._stopped:
            self._score.print_final_score()
        
        pygame.quit()
        

if __name__ == "__main__":
    print(SYNOPSIS)
    game = Game()
    game.loop()
