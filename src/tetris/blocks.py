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
        y = 1

        super().__init__(well, x, y)

        self.matrix = np.zeros((4,4))
        self.matrix[1,:] = 1

class TetrominoJ(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 1
        y = 0

        super().__init__(well, x, y)

        self.matrix = np.zeros((3,3))
        self.matrix[0,0] = 1
        self.matrix[1,:] = 1

class TetrominoL(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 1
        y = 0

        super().__init__(well, x, y)

        self.matrix = np.zeros((3,3))
        self.matrix[0,2] = 1
        self.matrix[1,:] = 1

class TetrominoO(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 1
        y = 0

        super().__init__(well, x, y)

        self.matrix = np.ones((2,2))

class TetrominoS(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 1
        y = 0

        super().__init__(well, x, y)

        self.matrix = np.ones((3,3))
        self.matrix[0,0] = 0
        self.matrix[1,2] = 0
        self.matrix[2,:] = 0

class TetrominoZ(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 1
        y = 0

        super().__init__(well, x, y)

        self.matrix = np.ones((3,3))
        self.matrix[0,2] = 0
        self.matrix[1,0] = 0
        self.matrix[2,:] = 0

class TetrominoT(Tetromino):
    def __init__(self, well: Well) -> None:
        x = (well.ncols // 2) - 1
        y = 0

        super().__init__(well, x, y)

        self.matrix = np.ones((3,3))
        self.matrix[0,0] = 0
        self.matrix[0,2] = 0
        self.matrix[2,:] = 0

def get_tetromino(name: str, *args, **kwargs):
    name = name.upper()

    return eval(f"Tetromino{name}")(*args, **kwargs)
