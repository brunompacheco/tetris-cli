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
    
    def check_collision(self, tetromino) -> bool:
        well_region = self.matrix[
            tetromino.y:tetromino.y + tetromino.matrix.shape[0],
            tetromino.x:tetromino.x + tetromino.matrix.shape[1]
        ]

        well_region = well_region > 0
        tetromino_region = tetromino.matrix > 0

        intersection = (well_region & tetromino_region).sum()

        return intersection > 0

    def check_oob(self, tetromino) -> bool:
        """Check if tetromino is out of bounds.
        """
        if tetromino.x < 0:
            return True
        elif tetromino.y < 0:
            return True
        elif tetromino.x + tetromino.matrix.shape[1] > self.ncols:
            return True
        elif tetromino.y + tetromino.matrix.shape[0] > self.nrows:
            return True
        else:
            return False
