from abc import ABC, abstractmethod
import numpy as np

from .well import Well


class Tetromino(ABC):
    def __init__(self, well: Well, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self._well = well

        self.r = 0

    @property
    @abstractmethod
    def matrix(self):
        pass

    def rotate(self, ccw=False):
        if ccw:  # counter-clockwise
            self.r -= 1

            if self.r < 0:
                self.r = self.n_cycles - 1
        else:
            self.r += 1

            if self.r < self.n_cycles - 1:
                self.r = 0

class TetrominoI(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 2
        y = 0

        super().__init__(well, x, y)

        self.n_cycles = 2

    @property
    def matrix(self):
        # at position 0
        s = np.ones((1,4))

        # at position 1
        if self.r == 1:
            s = s.T

        return s