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

    assert not basic_well.check_overlap(t)

    t.x += 1

    assert basic_well.check_overlap(t)

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
