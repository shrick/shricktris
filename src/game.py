# game.py

import pygame
from field import GameField
from preview import Preview
from brick import Brick
from figure import generate_randomized_figures as FigureFactory
from control import Control
from score import Score
import colors


GAME_TITLE = "Shricktris"
START_FPS = 12
START_GAME_STEPOVER = 8
SCREEN_RESOLUTION = (600, 800)
GRID_COLUMNS = 16
GRID_ROWS = 30


class Game:
    def __init__(self):
        # init pygame components
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self._screen = pygame.display.set_mode(SCREEN_RESOLUTION)
        self._background = pygame.Surface(self._screen.get_size()).convert()
        self._background.fill(colors.WHITE)
        self._font = pygame.font.SysFont(None, 24)
        self._set_message("Press PAUSE key to start!", colors.GREEN)

        # init game components
        rect_pixel_length = 20
        self._field = GameField(self._screen, GRID_COLUMNS, GRID_ROWS, rect_pixel_length)
        self._preview = Preview(self._screen, SCREEN_RESOLUTION[0] - 100, 20,
            Brick.DIMENSION, int(rect_pixel_length / 2))
        self._figure_factory = FigureFactory(self._field)
        self._figure = next(self._figure_factory)
        self._next_figure = next(self._figure_factory)
        self._score = Score()
        self._control = Control(START_FPS)

        # init speed and game state
        self._stepover = START_GAME_STEPOVER
        self._nostep = self._stepover
        self._looping = True
        self._was_started = False
        self._has_stopped = False
        self._is_paused = True

    def _set_message(self, text, color):
        self._text_image = self._font.render(text, True, colors.GRAY if color is None else color)
        

    def _display_score(self):
        if self._has_stopped:
            score_text = self._score.get_final_score()
            self._set_message(score_text + "   Game finished. Press Q to quit!", colors.RED)
        else:
            score_text = self._score.get_current_score()
            self._set_message(score_text, colors.CYAN)

        print(score_text)

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
        if self._control.pause() and not self._has_stopped:
            self._is_paused = not self._is_paused
            if self._is_paused:
                self._set_message("Press PAUSE key to continue.", colors.BLUE)
            else:
                self._was_started = True
                self._set_message("Press PAUSE key to pause.", colors.BLUE)
        
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
    
    def _resolve_lines(self):
        lines = self._field.resolve_lines()
        if lines:
            self._score.add_lines(lines)
            self._display_score()
            # increase game speed
            self._stepover = max(self._stepover - 1, 1)
            print("[DEBUG] game_stepover = " + str(self._stepover))
    
    def _spawn_new_figure(self):
        if self._figure.is_freezed():
            self._figure = self._next_figure
            if self._field.collides(self._figure):
                self._has_stopped = True
                self._display_score()
            else:
                self._next_figure = next(self._figure_factory)
                print("Next figure: " + self._next_figure.get_name())

    def _draw(self):
        self._screen.blit(self._background, (0, 0))
        self._field.draw_grid()

        if self._was_started:
            if not self._has_stopped:
                self._field.draw_figure(self._figure)
                self._preview.draw_figure(self._next_figure)
            else:
                # hack in some flickering
                self._nostep =  (self._nostep + 1) % 3
                if not self._nostep:
                    self._field.draw_figure(self._figure, colors.GRAY)
        
        if self._text_image is not None:
            rect = self._text_image.get_rect()
            rect.topleft = (20, 20)
            self._screen.blit(self._text_image, rect)
        
        pygame.display.update()

    def loop(self):        
        while self._looping:
            self._control.process_events()
            self._check_states()
            
            if not self._is_paused and not self._has_stopped:
                self._move_figure()

                self._nostep =  (self._nostep + 1) % self._stepover
                if not self._nostep:
                    # advance game
                    self._figure.step_down()
                    self._resolve_lines()
                    self._spawn_new_figure()
            
            self._draw()
        
        if not self._has_stopped:
            print(self._score.get_final_score())
        
        pygame.quit()