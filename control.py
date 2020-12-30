# control.py

import pygame


MIN_FPS = 1
MAX_FPS = 24


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