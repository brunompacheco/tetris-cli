import numpy as np
import pytest

from tetris.blocks import TetrominoI, TetrominoJ, TetrominoL, TetrominoS, TetrominoZ, TetrominoO, TetrominoT
from tetris.well import Well

@pytest.fixture
def basic_well():
    return Well()

@pytest.fixture
def tetromino_I(basic_well):
    return TetrominoI(basic_well)

def test_full_rotation(basic_well):
    for T in [TetrominoI, TetrominoJ, TetrominoL, TetrominoO, TetrominoS, TetrominoZ, TetrominoT]:
        t = T(basic_well)

        first_matrix = t.matrix
        for _ in range(4):
            t.rotate()
        rotated_matrix = t.matrix

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
