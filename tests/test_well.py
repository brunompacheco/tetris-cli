import numpy as np
import pytest

from tetris.blocks import TetrominoI
from tetris.well import Well


@pytest.fixture
def basic_well():
    return Well()

def test_no_initial_overlap(basic_well):
    # TODO: do for all tetrominos
    t = TetrominoI(basic_well)

    assert not basic_well.check_overlap(t)

def test_no_initial_oob(basic_well):
    # TODO: do for all tetrominos
    t = TetrominoI(basic_well)

    assert not basic_well.check_oob(t)

def test_oob(basic_well):
    # TODO: do for all tetrominos
    t = TetrominoI(basic_well)

    t.x = basic_well.ncols - 4
    assert not basic_well.check_oob(t)

    t.x += 1
    assert basic_well.check_oob(t)

    t.rotate()
    assert not basic_well.check_oob(t)

def test_add_tetromino_inplace(basic_well):
    t = TetrominoI(basic_well)

    m = basic_well.add_tetromino(t, in_place=False)

    basic_well.add_tetromino(t, in_place=True)

    assert (basic_well.matrix == m).all()

def test_add_tetromino(basic_well):
    # TODO: do for all tetrominos
    t = TetrominoI(basic_well)
    
    m = basic_well.add_tetromino(t)

    assert m.sum() == 4

def test_trim_tetrominos(basic_well):
    well = Well(2,2)

    t = TetrominoI(well)

    t.x = -1
    t.y = -1

    matrix, x, y = well._trim_tetromino_matrix(t)

    assert max(matrix.shape) == 2
    assert x == 0
    assert y == 0

    assert (matrix == np.array([
        [1,1],
        [0,0],
    ])).all()
