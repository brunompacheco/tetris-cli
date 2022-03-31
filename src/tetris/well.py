from typing import Tuple
import numpy as np


class Well():
    def __init__(self, nrows=23, ncols=10) -> None:
        self.nrows = nrows
        self.ncols = ncols

        self.matrix = np.zeros((nrows, ncols))

    def _trim_tetromino_matrix(self, tetromino) -> Tuple[np.ndarray, int, int]:
        matrix, x, y = tetromino.matrix, tetromino.x, tetromino.y

        if y < 0:
            matrix = matrix[-y:]
            y =  0

        if x < 0:
            matrix = matrix[:,-x:]
            x = 0

        x_margin = self.ncols - x
        y_margin = self.nrows - y

        matrix = matrix[:y_margin,:x_margin]

        return matrix, x, y

    def add_tetromino(self, tetromino, in_place=False):
        matrix, x, y = self._trim_tetromino_matrix(tetromino)

        new_matrix = self.matrix.copy()

        if matrix.sum() > 0:
            new_matrix[y:y + matrix.shape[0], x:x + matrix.shape[1]] += matrix

        if in_place:
            self.matrix = new_matrix
        else:
            return new_matrix

    def check_overlap(self, tetromino) -> bool:
        matrix, x, y = self._trim_tetromino_matrix(tetromino)

        well_region = self.matrix[
            y:y + matrix.shape[0],
            x:x + matrix.shape[1]
        ]

        well_region = well_region > 0
        tetromino_region = matrix > 0

        intersection = (well_region & tetromino_region).sum()

        return intersection > 0

    def check_oob(self, tetromino) -> bool:
        """Check if tetromino is out of bounds.
        """
        ys, xs = np.nonzero(tetromino.matrix)
        x_max, y_max = max(xs), max(ys)
        x_min, _ = min(xs), min(ys)

        if tetromino.x + x_min < 0:
            return True
        elif tetromino.x + x_max >= self.ncols:
            return True
        elif tetromino.y + y_max >= self.nrows:
            return True
        else:
            return False
    
    def clear_lines(self):
        occupied = self.matrix > 0

        lines_cleared = occupied.all(axis=1)

        new_matrix = np.zeros((self.nrows, self.ncols))
        new_matrix[sum(lines_cleared):] = self.matrix[~lines_cleared]

        self.matrix = new_matrix

        return sum(lines_cleared)
    
    def is_game_over(self, visible=20):
        ys, _ = np.nonzero(self.matrix)
        
        if len(ys) == 0:
            return False
        else:
            y_min = min(ys)

            return y_min < self.nrows - visible
