from abc import ABC, abstractmethod
from threading import Thread, Event

import numpy as np

from asciimatics.screen import Screen

from tetris.blocks import Tetromino, TetrominoI
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

class DrawerThread(ABC):
    """Update on-demand.
    """
    def __init__(self, flag: Event) -> None:
        self.thread = None
        self.flag = flag

    def start(self, *args, **kwargs):
        self.thread = Thread(target=self._run, args=args, kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()

    def _run(self, *args, **kwargs):
        self.flag.wait()
        self.flag.clear()

        self.run(*args, **kwargs)

        self.thread = Thread(target=self._run, args=args, kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()

    @abstractmethod
    def run(self):
        pass

class WellDrawer(DrawerThread):
    def __init__(self, flag: Event) -> None:
        super().__init__(flag)

        self._past_well_str = None

    def run(self, screen: Screen, well: Well, tetromino: Tetromino):
        # TODO: draw only changes, avoid flickering

        x = (screen.width // 2) - well.ncols
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

class NextDrawer():
    solid_block = chr(0x2588)
    def __init__(self, screen: Screen, x: int, y: int, bg_square="  ") -> None:
        self.x = x 
        self.y = y

        self.bg_square = bg_square

        self.base = [16 * self.solid_block,]
        self.base += [
            2 * self.solid_block + 6 * self.bg_square + 2 * self.solid_block,
        ] * 6
        self.base += [16 * self.solid_block,]

        for i, line in enumerate(self.base):
            screen.print_at(
                line,
                x=self.x,
                y=self.y + i,
            )
        screen.refresh()
    
    def next(self, tetromino: Tetromino, screen: Screen):
        screen.clear_buffer(
            screen.COLOUR_BLACK,
            screen.A_NORMAL,
            screen.COLOUR_BLACK,
            self.x + 2,
            self.y + 1,
            12,
            6,
        )

        if tetromino.name == 'I':
            x_, y_ = self.x + 4, self.y + 2
        elif tetromino.name == 'O':
            x_, y_ = self.x + 6, self.y + 3
        else:
            x_, y_ = self.x + 5, self.y + 3

        matrix = np.where(tetromino.matrix == 0, self.bg_square, 2 * self.solid_block)

        for i, line in enumerate(matrix):
            screen.print_at(
                ''.join(line),
                x_,
                y_ + i,
            )
        screen.refresh()
