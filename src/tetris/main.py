import sys
from time import sleep

import click

from . import __version__

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen, Screen


class Well(Print):
    def __init__(self, screen, nrows=20, ncols=10) -> None:
        board = ""
        board += "${7,2,7}_" * (2 * ncols + 4) + '\n'
        board += ("${7,2,7}__${7,2,0}" + " ." * ncols + '${7,2,7}__\n') * nrows
        board += "${7,2,7}_" * (2 * ncols + 4) + '\n'

        super().__init__(
            screen,
            StaticRenderer(images=[board,]),
            x=(screen.width // 2) - (ncols // 2),
            y=(screen.height // 2) - (nrows // 2),
            speed=0,
        )

@ManagedScreen
def demo(screen: Screen = None):
    effects = [
        Well(screen),
    ]
    screen.play([Scene(effects, -1),])

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
