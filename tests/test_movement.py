from time import sleep
import pytest

from threading import Event
from tetris.blocks import TetrominoI

from tetris.movement import TetrominoDropper, TetrominoController
from tetris.well import Well


@pytest.fixture
def basic_well():
    return Well()

@pytest.fixture
def tetromino(basic_well):
    return TetrominoI(basic_well)

def test_drop_cancel(basic_well, tetromino):
    interval = 0.05
    
    dropper = TetrominoDropper(interval, Event())

    dropper.start(tetromino, basic_well)

    sleep(5 * interval + 0.01)

    dropper.cancel()

    assert tetromino.y == 5

    sleep(5 * interval)

    assert tetromino.y == 5

def test_update_flag(basic_well, tetromino):
    interval = 0.05
    flag = Event()
    flag.clear()
    
    dropper = TetrominoDropper(interval, flag)

    dropper.start(tetromino, basic_well)

    sleep(interval + 0.01)

    assert flag.is_set()
