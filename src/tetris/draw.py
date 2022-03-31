from threading import Thread, Event

import numpy as np

from asciimatics.screen import Screen

from tetris.blocks import Tetromino
from tetris.well import Well


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
