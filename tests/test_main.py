from threading import Event
import click.testing
import pytest
import numpy as np

from tetris import main
from tetris.blocks import TetrominoO
from tetris.well import Well


@pytest.fixture
def runner():
    return click.testing.CliRunner()

@pytest.fixture
def mock_event_flag(mocker):
    mock = mocker.patch.object(Event, 'is_set')
    mock.return_value = False

    return mock

@pytest.fixture
def mock_screen(mocker):
    return mocker.patch('asciimatics.screen.Screen')

def test_play(mock_event_flag, mock_screen):
    assert main.play() == 0

def test_main_succeeds(runner, mock_event_flag, mock_screen):
    result = runner.invoke(main.main)

    assert result.exit_code == 0

def test_drop_tetromino(mock_screen):
    well = Well(5, 5)
    t = TetrominoO(well)
    screen = mock_screen.return_value

    main.drop_tetromino(t, well, screen)

    expected = np.array([
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,1,1,0,0],
        [0,1,1,0,0],
    ])
    assert (well.matrix >= expected).all()
