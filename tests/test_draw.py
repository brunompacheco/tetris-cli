import numpy as np

from tetris import draw


def test_draw_well():
    matrix = np.array([
        [0, 1],
        [2, 0],
    ])
    board = draw.draw_well(matrix, "  ")

    s = 2 * chr(0x2588)
    expected = [
        4 * s,
        s + "  " + 2 * s,
        2 * s + "  " + s,
        4 * s
    ]
    assert board == '\n'.join(expected)