from time import sleep
import pytest

from threading import Event
from tetris.blocks import TetrominoI

from tetris.movement import TetrominoDropper
from tetris.well import Well


@pytest.fixture
def basic_well():
    return Well()

@pytest.fixture
def tetromino(basic_well):
    return TetrominoI(basic_well)

@pytest.fixture
def dropper():
    return TetrominoDropper(0.05, Event(), Event())

def test_drop_cancel(basic_well, tetromino, dropper):
    dropper.start(tetromino, basic_well)

    sleep(6 * dropper.interval)

    dropper.cancel()

    assert tetromino.y == 5

    sleep(5 * dropper.interval)

    assert tetromino.y == 5

def test_drop_flag(basic_well):
    t = TetrominoI(basic_well)

    interval = 0.05
    flag = Event()
    flag.clear()

    dropper = TetrominoDropper(interval, Event(), flag)

    dropper.start(t, basic_well)

    sleep(dropper.interval * (basic_well.nrows + 2))

    assert flag.is_set()

def test_update_flag(basic_well):
    t = TetrominoI(basic_well)

    interval = 0.05
    flag = Event()
    flag.clear()

    dropper = TetrominoDropper(interval, flag, Event())

    dropper.start(t, basic_well)

    sleep(dropper.interval + 0.01)

    assert flag.is_set()
