import sys
from threading import Thread, Event

import click
import numpy as np

from tetris.movement import TetrominoController, TetrominoDropper

from . import __version__
from tetris.blocks import Tetromino, TetrominoI, TetrominoO, get_tetromino
from tetris.well import Well

from asciimatics.exceptions import ResizeScreenError
from asciimatics.screen import ManagedScreen, Screen


def draw_well(matrix: np.ndarray, bg_square: str = "  ", visible=20) -> str:
    solid_block = chr(0x2588)
    matrix = np.where(matrix == 0, bg_square, 2 * solid_block)
    matrix = matrix[-visible:]  # display only visible rows

    lines = [2*solid_block + ''.join(line) + 2*solid_block for line in matrix]
    lines.insert(0, solid_block * len(lines[0]))
    lines.append(solid_block * len(lines[0]))
    board = '\n'.join(lines)

    return board

class WellDrawer():
    """Update on-demand.
    """
    def __init__(self, flag: Event) -> None:
        self.thread = None
        self.flag = flag

        self._past_well_str = None

    def start(self, *args, **kwargs):
        self.thread = Thread(target=self.run, args=args, kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()

    def run(self, screen: Screen, well: Well, tetromino: Tetromino):
        self.flag.wait()
        self.flag.clear()

        # TODO: draw only changes, avoid flickering

        x = (screen.width // 2) - (well.ncols // 2)
        y = (screen.height // 2) - (well.nrows // 2)

        well_str = draw_well(well.add_tetromino(tetromino))
        for l, line in enumerate(well_str.split('\n')):
            if self._past_well_str is not None:
                past_line = self._past_well_str.split('\n')[l]
                if (past_line == line).all():
                    continue

            screen.print_at(
                line,
                x=x,
                y=y+l
            )

        screen.refresh()

        self.thread = Thread(target=self.run, args=(screen, well, tetromino))
        self.thread.daemon = True
        self.thread.start()

def drop_tetromino(tetromino: Tetromino, well: Well, screen: Screen):
    update_flag = Event()
    update_flag.set()

    t_dropped = Event()
    t_dropped.clear()

    well_drawer = WellDrawer(update_flag)
    well_drawer.start(screen, well, tetromino)

    # 2. drop tetromino until it touches the others
    # well.matrix[5,5] = 1

    dropper = TetrominoDropper(0.25, update_flag, t_dropped)
    controller = TetrominoController(0.01, update_flag)

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
    game_on = Event()
    game_on.set()

    well = Well()

    lines_cleared = 0
    screen.print_at(lines_cleared, 0, 0)
    while game_on.is_set():
        ## MAIN LOOP

        # 1. generate new tetromino
        t = get_tetromino(
            np.random.choice(['I', 'O', 'L', 'J', 'S', 'Z', 'T']),
            well
       )

        if drop_tetromino(t, well, screen) == 1:
            return 1

        # 4. check for line clears
        lines_cleared += well.clear_lines()
        screen.print_at(lines_cleared, 0, 0)

        # 5. check for game overs
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
