import pygame
import random


GAME_TITLE = "Shricktris"
MIN_FPS = 1
MAX_FPS = 24
START_FPS = 3
SCREEN_RESOLUTION = (600, 800)
COLUMNS = 16
ROWS = 30

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
    _to_quit = False
    _keystates = {}

    def process_events(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._to_quit = True
            elif event.type == pygame.KEYDOWN:                
                self._keystates[event.key] = True
            elif event.type == pygame.KEYUP:
                self._keystates[event.key] = False
        pygame.event.pump()
    
    def _is_pressed(self, keys):
        return all(k in self._keystates and self._keystates[k] for k in keys)

    def quit(self):
        return self._to_quit or self._is_pressed([pygame.K_q])
    
    def pause(self):
        return self._is_pressed([pygame.K_PAUSE])

    def move_left(self):
        return self._is_pressed([pygame.K_LEFT])

    def move_right(self):
        return self._is_pressed([pygame.K_RIGHT])

    def fast_down(self):
        return self._is_pressed([pygame.K_DOWN])

    def fall_down(self):
        return self._is_pressed([pygame.K_SPACE])

    def rotate(self):
        return self._is_pressed([pygame.K_UP])

    def speedup(self):
        return self._is_pressed([pygame.K_PLUS])

    def speeddown(self):
        return self._is_pressed([pygame.K_MINUS])


# Tetriminos
FIGURE_DIMENSION = 4
FIGURES = [
    # O (yellow)
    [ "O", ((5, 6, 9, 10),) ],
    # I (cyan)
    [ "I", ((4, 5, 6, 7), (1, 5, 9, 13)) ],
    # L (orange)
    [ "L", ((1, 5, 9, 10), (4, 5, 6, 8), (1, 2, 6, 10), (2, 4, 5, 6)) ],
    # J (blue)
    [ "J", ((5, 9, 10, 11), (1, 2, 5, 9), (4, 5, 6, 10), (2, 6, 9, 10)) ],
    # T (purple)
    [ "T", ((5, 6, 7, 10), (2, 5, 6, 10), (2, 5, 6, 7), (1, 5, 6, 9)) ],
    # S (green)
    [ "S", ((6, 7, 9, 10), (1, 5, 6, 10)) ],
    # Z (red)
    [ "Z", ((5, 6, 10, 11), (2, 5, 6, 9)) ],
]

class RandomFigure:
    def __init__(self, game_field):
        self._game_field = game_field
        self._type = random.randint(0, len(FIGURES) - 1)
        self._name = FIGURES[self._type][0]
        self._variants = FIGURES[self._type][1]
        self._variant = 0
        self._x = int((self._game_field.get_columns() - FIGURE_DIMENSION) / 2)
        self._y = 0
        self._freezed = False
    
    def get_name(self):
        return self._name

    def get_colorindex(self):
        return self._type + 1

    def get_colorrgb(self):
        return COLORS[self.get_colorindex()]

    def get_points(self):
        return self._variants[self._variant]

    def get_xy_coordinates(self):
        return ((int(self._x + (p %  FIGURE_DIMENSION)), int(self._y + (p / FIGURE_DIMENSION)))
            for p in figure.get_points())
    
    def step_down(self):
        self._y += 1
        if self._game_field.collides(self):
            self._y -= 1
            self.freeze()
    
    def _move(self, dx=0, dy=0):
        self._x += dx
        self._y += dy

        if self._game_field.collides(self):
            self._x -= dx
            self._y -= dy

    def move_left(self):
        self._move(dx=-1)

    def move_right(self):
        self._move(dx=+1)

    def fast_down(self):
        self._move(dy=+1)

    def fall_down(self):
        while not self.is_freezed():
            self.step_down()

    def _switch_variant(self, direction):
        self._variant = (self._variant + direction) % len(self._variants)

    def rotate(self):
        if len(self._variants) > 1:
            self._switch_variant(+1)
            if self._game_field.collides(self):
                self._switch_variant(-1)

    def freeze(self):
        self._game_field.freeze_figure(figure)
        figure._freezed = True

    def is_freezed(self):
        return self._freezed
    
    
class GameField:
    def __init__(self, screen, columns, rows, length):
        self._screen = screen
        self._columns = columns
        self._rows = rows

        x_offset = int((screen.get_width() / length - columns) / 2 * length)
        y_offset = int((screen.get_height() / length - rows) / 2 * length)

        self._field = [[
            [pygame.Rect(x_offset + length * x, y_offset + length * y, length, length), 0]
            for x in range(columns)]
            for y in range(rows)]

    def get_columns(self):
        return self._columns

    def draw_grid(self):
        for x in range(self._columns):
            for y in range(self._rows):
                cell = self._field[y][x]
                rect = cell[0]
                color = cell[1]
                pygame.draw.rect(self._screen, COLORS[color], rect, 0 if color else 1)

    def draw_figure(self, figure):
        for x, y in figure.get_xy_coordinates():
            pygame.draw.rect(self._screen, figure.get_colorrgb(), self._field[y][x][0], 0)

    def collides(self, figure):
        for x, y in figure.get_xy_coordinates():
            # check grid boundaries
            if not (0 <= x < self._columns and 0 <= y < self._rows):
                return True
            # check freezed figures
            if self._field[y][x][1] != 0:
                return True

        return False

    def freeze_figure(self, figure):
        colorindex = figure.get_colorindex()
        for x, y in figure.get_xy_coordinates():
            self._field[y][x][1] = colorindex
    
    def resolve_lines(self):
        lines = 0
        for y1 in range(self._rows):
            if all(self._field[y1][x][1] != 0 for x in range(self._columns)):
                # copy down
                for y2 in range(y1, 1, -1):
                    for x in range(self._columns):
                        self._field[y2][x][1] = self._field[y2 - 1][x][1]
                
                # empty first line
                for x in range(self._columns):
                    self._field[0][x][1] = 0

                lines += 1
        
        return lines

        

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    fps = START_FPS
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption(GAME_TITLE)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    field = GameField(screen, COLUMNS, ROWS, 20)
    figure = RandomFigure(field)
    next_figure = RandomFigure(field)
    resolved_lines = 0
    score = 0

    control = Control()
    game_stop = False
    game_running = True
    game_pause = True
    print("Press PAUSE key to pause/unpause!")

    while game_running:
        clock.tick(fps)
        control.process_events()
        
        # toggle game speed
        if control.speedup():
            fps = min(fps + 1, MAX_FPS)
            print("fps=" + str(fps))
        if control.speeddown():
            fps = max(fps - 1, MIN_FPS)
            print("fps=" + str(fps))
        
        # check game state
        if control.quit():
            game_running = False
            break
        if control.pause():
            game_pause = not game_pause
        
        if not (game_pause or game_stop):
            # move figure
            if control.move_left():
                figure.move_left()
            if control.move_right():
                figure.move_right()
            if control.fast_down():
                figure.fast_down()
            if control.fall_down():
                figure.fall_down()
            if control.rotate():
                figure.rotate()

            # step game
            figure.step_down()
            
            # resolve lines
            lines = field.resolve_lines()
            if lines:
                resolved_lines += lines
                bonus = lines ** 2
                score += bonus
                print("Score: {} (+{} point{} for {} line{})".format(
                    score, 
                    bonus, "" if bonus == 1 else "s",
                    lines, "" if resolved_lines == 1 else "s"))
            
            # spawn new figure
            if figure.is_freezed():
                figure = next_figure
                if field.collides(figure):
                    print("Game finished.")
                    game_stop = True
                    fps = MAX_FPS # increase key processing
                else:
                    next_figure = RandomFigure(field)
                    print("Next figure: " + next_figure.get_name())
        
        # draw
        screen.blit(background, (0, 0))
        field.draw_grid()
        field.draw_figure(figure)
        pygame.display.update()

print("Final score: {} ({} resolved line{})".format(score, resolved_lines, "" if resolved_lines == 1 else "s"))
