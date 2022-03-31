import numpy as np
import pytest

from tetris.blocks import TetrominoI
from tetris.well import Well

@pytest.fixture
def basic_well():
    return Well()

@pytest.fixture
def tetromino_I(basic_well):
    return TetrominoI(basic_well)

def test_full_rotation(tetromino_I):
    # TODO: iterate all tetrominos

    first_matrix = tetromino_I.matrix
    for _ in range(4):
        tetromino_I.rotate()
    rotated_matrix = tetromino_I.matrix

    assert first_matrix.shape == rotated_matrix.shape
    assert (first_matrix == rotated_matrix).all()

def test_rotation_I(tetromino_I):
    assert (tetromino_I.matrix == np.array([
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
    ])).all()
    tetromino_I.rotate()
    assert (tetromino_I.matrix == np.array([
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,0],
    ])).all()
    tetromino_I.rotate()
    assert (tetromino_I.matrix == np.array([
        [0,0,0,0],
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
    ])).all()
    tetromino_I.rotate()
    assert (tetromino_I.matrix == np.array([
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
    ])).all()
    tetromino_I.rotate()
    assert (tetromino_I.matrix == np.array([
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
    ])).all()
    tetromino_I.rotate(ccw=True)
    assert (tetromino_I.matrix == np.array([
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
    ])).all()
    tetromino_I.rotate(ccw=True)
    assert (tetromino_I.matrix == np.array([
        [0,0,0,0],
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
    ])).all()
    tetromino_I.rotate(ccw=True)
    assert (tetromino_I.matrix == np.array([
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,0],
    ])).all()
    tetromino_I.rotate(ccw=True)
    assert (tetromino_I.matrix == np.array([
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
    ])).all()
