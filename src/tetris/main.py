import sys

import click
import numpy as np

from tetris.movement import TetrominoController, TetrominoDropper

from . import __version__
from tetris.blocks import TetrominoI
from tetris.well import Well

from asciimatics.exceptions import ResizeScreenError
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
