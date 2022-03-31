import pytest

from tetris.blocks import TetrominoI
from tetris.well import Well

@pytest.fixture
def basic_well():
    return Well()

@pytest.fixture
def tetromino_I(basic_well):
    return TetrominoI(basic_well)

def test_matrices(tetromino_I):
    # TODO: iterate all tetrominos

    for _ in range(tetromino_I.n_cycles):
        tetromino_I.rotate()

        assert max(tetromino_I.matrix.shape) <= 4

def test_rotation(tetromino_I):
    # TODO: iterate all tetrominos

    first_matrix = tetromino_I.matrix
    for _ in range(tetromino_I.n_cycles):
        tetromino_I.rotate()
    rotated_matrix = tetromino_I.matrix

    assert first_matrix.shape == rotated_matrix.shape
    assert (first_matrix == rotated_matrix).all()
