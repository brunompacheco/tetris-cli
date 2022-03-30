import sys
from threading import Timer
from time import sleep

import click
import numpy as np

from . import __version__
from tetris.blocks import TetrominoI
from tetris.well import Well

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.paths import DynamicPath
from asciimatics.screen import ManagedScreen, Screen


class KeyboardController(DynamicPath):
    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.KEY_UP:
                self._y -= 1
                self._y = max(self._y, 2)
            elif key == Screen.KEY_DOWN:
                self._y += 1
                self._y = min(self._y, self._screen.height-2)
            elif key == Screen.KEY_LEFT:
                self._x -= 2
                self._x = max(self._x, 3)
            elif key == Screen.KEY_RIGHT:
                self._x += 2
                self._x = min(self._x, self._screen.width-3)
            else:
                return event
        else:
            return event

def draw_well(matrix: np.ndarray, bg_square: str = " .") -> str:
    matrix = np.where(matrix == 0, bg_square, 2 * chr(0x2588))

    lines = [''.join(line) for line in matrix]
    board = '\n'.join(lines)

    return board

def update_screen(screen, well, tetromino):
    # TODO: draw only changes, avoid flickering

    x = (screen.width // 2) - (well.ncols // 2)
    y = (screen.height // 2) - (well.nrows // 2)

    well_str = draw_well(well.add_tetromino(tetromino))
    for l, line in enumerate(well_str.split('\n')):
        screen.print_at(
            line,
            x=x,
            y=y+l
        )

    screen.refresh()

class TetrominoDropper():
    def __init__(self) -> None:
        self.timer = None

        self._stop = False

    @property
    def is_alive(self):
        if self.timer is None:
            return False
        else:
            return self.timer.is_alive()

    def run(self, interval: float, tetromino):
        self.timer = Timer(interval, self.run, (interval, tetromino))
        self.timer.daemon = True
        self.timer.start()

        tetromino.y += 1

        # TODO: check for collision
        # if collision:  # in the future update
        #     tetromino.y -= 1
        #     self.timer.cancel()
        # maybe raise event on collision?

@ManagedScreen
def play(screen: Screen = None):
    well = Well()

    ## MAIN LOOP

    # 1. generate new tetromino
    t_I = TetrominoI(well)

    # 2. drop tetromino until it touches the others
    dropper = TetrominoDropper()
    dropper.run(1, t_I)

    while True:
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return

        update_screen(screen, well, t_I)

    # 3. add tetromino to well

    # 4. check for line clears



@click.command()
@click.version_option(version=__version__)
def main():
    """Tetris remake using asciimatics.
    """
    try:
        play()
        sys.exit(0)
    except ResizeScreenError:
        pass

if __name__ == '__main__':
    main()
