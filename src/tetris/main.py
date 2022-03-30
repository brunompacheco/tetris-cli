from abc import ABC, abstractmethod
import sys
from threading import Thread, Timer
from time import sleep

import click
import numpy as np

from . import __version__
from tetris.blocks import Tetromino, TetrominoI
from tetris.well import Well

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.paths import DynamicPath
from asciimatics.screen import ManagedScreen, Screen


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

class RecurringTimer(ABC):
    def __init__(self, interval: float) -> None:
        self.timer = None
        self.interval = interval

    @property
    def is_alive(self):
        if self.timer is None:
            return False
        else:
            return self.timer.is_alive()

    def start(self, *args, **kwargs):
        self.timer = Timer(self.interval, self._run, args=args, kwargs=kwargs)
        self.timer.daemon = True
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

    def _run(self, *args, **kwargs):
        self.timer = Timer(self.interval, self._run, args=args, kwargs=kwargs)
        self.timer.daemon = True
        self.timer.start()

        self.run(*args, **kwargs)
    
    @abstractmethod
    def run(self):
        pass

class TetrominoDropper(RecurringTimer):
    def run(self, tetromino, well):
        tetromino.y += 1

        if well.check_overlap(tetromino) or well.check_oob(tetromino):
            tetromino.y -= 1
        # maybe raise event on collision?

class TetrominoController(RecurringTimer):
    def run(self, screen: Screen, tetromino: Tetromino, well: Well):
        screen.wait_for_input(self.interval)

        event = screen.get_event()
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.KEY_DOWN:
                screen.print_at("D",0,0)
                tetromino.y += 1

                if well.check_overlap(tetromino) or well.check_oob(tetromino):
                    tetromino.y -= 1
            elif key == Screen.KEY_LEFT:
                screen.print_at("L",0,0)
                tetromino.x -= 1

                if well.check_overlap(tetromino) or well.check_oob(tetromino):
                    tetromino.x += 1
            elif key == Screen.KEY_RIGHT:
                screen.print_at("R",0,0)
                tetromino.x += 1

                if well.check_overlap(tetromino) or well.check_oob(tetromino):
                    tetromino.x -= 1
        

@ManagedScreen
def play(screen: Screen = None):
    well = Well()

    ## MAIN LOOP

    # 1. generate new tetromino
    t = TetrominoI(well)

    # 2. drop tetromino until it touches the others
    # well.matrix[5,5] = 1

    dropper = TetrominoDropper(0.25)
    controller = TetrominoController(0.01)

    controller.start(screen, t, well)
    dropper.start(t, well)

    while True:
        update_screen(screen, well, t)

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
