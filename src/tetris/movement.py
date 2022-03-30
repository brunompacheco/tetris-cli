from abc import ABC, abstractmethod
from threading import Timer

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen

from tetris.blocks import Tetromino
from tetris.well import Well


class RecurringTimer(ABC):
    def __init__(self, interval: float) -> None:
        self.timer = None
        self.interval = interval

    @property
    def is_alive(self):
        if self.timer is None:
            return False
        else:
            return self.timer.is_alive()

    def start(self, *args, **kwargs):
        self.timer = Timer(self.interval, self._run, args=args, kwargs=kwargs)
        self.timer.daemon = True
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

    def _run(self, *args, **kwargs):
        self.timer = Timer(self.interval, self._run, args=args, kwargs=kwargs)
        self.timer.daemon = True
        self.timer.start()

        self.run(*args, **kwargs)
    
    @abstractmethod
    def run(self):
        pass

class TetrominoDropper(RecurringTimer):
    def run(self, tetromino: Tetromino, well: Well):
        tetromino.y += 1

        if well.check_overlap(tetromino) or well.check_oob(tetromino):
            tetromino.y -= 1
        # maybe raise event on collision?

class TetrominoController(RecurringTimer):
    def run(self, screen: Screen, tetromino: Tetromino, well: Well):
        screen.wait_for_input(self.interval)

        event = screen.get_event()
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.KEY_DOWN:
                screen.print_at("D",0,0)
                tetromino.y += 1

                if well.check_overlap(tetromino) or well.check_oob(tetromino):
                    tetromino.y -= 1
            elif key == Screen.KEY_LEFT:
                screen.print_at("L",0,0)
                tetromino.x -= 1

                if well.check_overlap(tetromino) or well.check_oob(tetromino):
                    tetromino.x += 1
            elif key == Screen.KEY_RIGHT:
                screen.print_at("R",0,0)
                tetromino.x += 1

                if well.check_overlap(tetromino) or well.check_oob(tetromino):
                    tetromino.x -= 1
        