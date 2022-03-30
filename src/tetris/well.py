import numpy as np


class Well():
    def __init__(self, nrows=20, ncols=10) -> None:
        self.nrows = nrows
        self.ncols = ncols

        self.matrix = np.zeros((nrows, ncols))

    def add_tetromino(self, tetromino, in_place=False):
        t_matrix = tetromino.matrix

        x = tetromino.x
        y = tetromino.y

        new_matrix = self.matrix.copy()

        new_matrix[y:y + t_matrix.shape[0], x:x+t_matrix.shape[1]] += t_matrix

        if in_place:
            self.matrix = new_matrix
        else:
            return new_matrix
