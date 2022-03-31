from abc import ABC
import numpy as np

from .well import Well


class Tetromino(ABC):
    def __init__(self, well: Well, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self._well = well

    def rotate(self, ccw=False):
        if ccw:
            self.matrix = np.rot90(self.matrix, k=1)
        else:
            self.matrix = np.rot90(self.matrix, k=-1)

class TetrominoI(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 2
        y = -1

        super().__init__(well, x, y)

        self.matrix = np.zeros((4,4))
        self.matrix[1,:] = 1

class TetrominoJ(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 2
        y = 0

        super().__init__(well, x, y)

        self.n_cycles = 2
