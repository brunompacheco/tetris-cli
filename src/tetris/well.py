import numpy as np


class Well():
    def __init__(self, nrows=20, ncols=10, bg_square=" .") -> None:
        self.nrows = nrows
        self.ncols = ncols

        self.bg_square = bg_square

        self.matrix = np.zeros((nrows, ncols))

    def add_tetromino(self, tetromino):
        t_matrix = tetromino.matrix

        x = tetromino.x
        y = tetromino.y
        self.matrix[y:y + t_matrix.shape[0], x:x+t_matrix.shape[1]] += t_matrix

    def __str__(self) -> str:
        matrix = np.where(self.matrix == 0, self.bg_square, 2 * chr(0x2588))

        lines = [''.join(line) for line in matrix]
        board = '\n'.join(lines)

        return board
