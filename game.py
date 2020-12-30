# game.py

import pygame
from field import GameField
from figure import RandomFigure
from control import Control
from colors import COLORS, WHITE, GRAY

GAME_TITLE = "Shricktris"
START_FPS = 12
START_GAME_STEPOVER = 8
SCREEN_RESOLUTION = (600, 800)
GRID_COLUMNS = 16
GRID_ROWS = 30


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