import sys
from threading import Event

import click
import numpy as np

from asciimatics.exceptions import ResizeScreenError
from asciimatics.screen import ManagedScreen, Screen

from . import __version__
from tetris.blocks import Tetromino, get_tetromino
from tetris.draw import NextDrawer, WellDrawer
from tetris.movement import TetrominoController, TetrominoDropper
from tetris.well import Well


def drop_tetromino(tetromino: Tetromino, well: Well, screen: Screen):
    update_well_flag = Event()
    update_well_flag.set()

    t_dropped = Event()
    t_dropped.clear()

    well_drawer = WellDrawer(update_well_flag)
    well_drawer.start(screen, well, tetromino)

    # 2. drop tetromino until it touches the others
    # well.matrix[5,5] = 1

    dropper = TetrominoDropper(0.25, update_well_flag, t_dropped)
    controller = TetrominoController(0.01, update_well_flag)

    controller.start(screen, tetromino, well)
    dropper.start(tetromino, well)

    try:
        t_dropped.wait()
    except KeyboardInterrupt:
        return 1

    controller.cancel()
    dropper.cancel()

    # 3. add tetromino to well
    well.add_tetromino(tetromino, in_place=True)

    return 0

@ManagedScreen
def play(screen: Screen = None):
    screen.clear()

    game_on = Event()
    game_on.set()

    well = Well()

    next_x = (screen.width // 2) + well.ncols + 6
    next_y = (screen.height // 2) - 4
    next_drawer = NextDrawer(screen, next_x, next_y)

    next_t = get_tetromino(
        np.random.choice(['I', 'O', 'L', 'J', 'S', 'Z', 'T']),
        well
    )

    lines_cleared = 0
    screen.print_at(lines_cleared, 0, 0)
    while game_on.is_set():
        # 1. generate new tetromino
        curr_t = next_t
        next_t = get_tetromino(
            np.random.choice(['I', 'O', 'L', 'J', 'S', 'Z', 'T']),
            well
        )
        next_drawer.next(next_t, screen)

        if drop_tetromino(curr_t, well, screen) == 1:
            return 1

        # 4. check for line clears
        lines_cleared += well.clear_lines()
        screen.print_at(lines_cleared, 0, 0)

        # 5. check for game over
        if well.is_game_over():
            return 0

    return 0

@click.command()
@click.version_option(version=__version__)
def main():
    """Tetris remake using asciimatics.
    """
    try:
        play()
    except ResizeScreenError:
        pass

    sys.exit(0)

if __name__ == '__main__':
    main()
