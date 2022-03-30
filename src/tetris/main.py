import sys
from time import sleep

import click
from tetris.blocks import TetrominoI

from tetris.well import Well

from . import __version__

from asciimatics.effects import Print, Sprite
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.renderers import StaticRenderer
from asciimatics.paths import DynamicPath
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen, Screen


class KeyboardController(DynamicPath):
    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.KEY_UP:
                self._y -= 1
                self._y = max(self._y, 2)
            elif key == Screen.KEY_DOWN:
                self._y += 1
                self._y = min(self._y, self._screen.height-2)
            elif key == Screen.KEY_LEFT:
                self._x -= 2
                self._x = max(self._x, 3)
            elif key == Screen.KEY_RIGHT:
                self._x += 2
                self._x = min(self._x, self._screen.width-3)
            else:
                return event
        else:
            return event

@ManagedScreen
def play(screen: Screen = None):
    well = Well()

    t_I = TetrominoI(well)
    t_I.y = 5
    well.add_tetromino(t_I)

    while True:
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return

        sleep(1)
        # screen.clear()
        x = (screen.width // 2) - (well.ncols // 2)
        y = (screen.height // 2) - (well.nrows // 2)
        for l, line in enumerate(str(well).split('\n')):
            screen.print_at(
                line,
                x=x,
                y=y+l
            )
        screen.refresh()

@click.command()
@click.version_option(version=__version__)
def main():
    """Tetris remake using asciimatics.
    """
    try:
        play()
        sys.exit(0)
    except ResizeScreenError:
        pass

if __name__ == '__main__':
    main()
