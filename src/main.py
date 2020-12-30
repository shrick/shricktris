#!/usr/bin/env python3
#
# main.py


from game import Game


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


if __name__ == "__main__":
    print(SYNOPSIS)
    game = Game()
    game.loop()
