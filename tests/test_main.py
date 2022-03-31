from threading import Event
import click.testing
import pytest
import numpy as np

from tetris import main

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

def test_draw_well():
    matrix = np.array([
        [0, 1],
        [2, 0],
    ])
    board = main.draw_well(matrix, "  ")

    s = 2 * chr(0x2588)
    expected = [
        4 * s,
        s + "  " + 2 * s,
        2 * s + "  " + s,
        4 * s
    ]
    assert board == '\n'.join(expected)
