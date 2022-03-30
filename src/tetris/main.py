import sys

import click

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

class Tetrimino(Sprite):
    def __init__(self, screen, **kwargs):
        box = "####\n"
        box += "####"

        super().__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=[box]),
            },
            path=KeyboardController(screen, 1 + screen.width // 2, screen.height // 2),
            clear=True,
            **kwargs
        )

class Well(Print):
    def __init__(self, screen, nrows=20, ncols=10) -> None:
        bg_dot = "  "
        board = ""
        board += "${7,2,7}_" * (2 * ncols + 4) + '\n'
        board += ("${7,2,7}__${7,2,0}" + bg_dot * ncols + '${7,2,7}__\n') * nrows
        board += "${7,2,7}_" * (2 * ncols + 4) + '\n'

        super().__init__(
            screen,
            StaticRenderer(images=[board,]),
            x=(screen.width // 2) - (ncols // 2),
            y=(screen.height // 2) - (nrows // 2),
            speed=0,
            transparent=True,
        )

@ManagedScreen
def demo(screen: Screen = None):
    effects = [
        Well(screen),
        Tetrimino(screen),
    ]
    # screen.play([Scene(effects, -1),])
    screen.set_scenes([Scene(effects, -1),])
    while True:
        try:
            screen.draw_next_frame()
        except StopApplication:
            break

@click.command()
@click.version_option(version=__version__)
def main():
    """Tetris remake using asciimatics.
    """
    try:
        demo()
        sys.exit(0)
    except ResizeScreenError:
        pass

if __name__ == '__main__':
    main()
