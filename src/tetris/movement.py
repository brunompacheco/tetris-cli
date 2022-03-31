from abc import ABC, abstractmethod
from threading import Event, Timer

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
    def __init__(self, interval: float, update_flag: Event, dropped_flag: Event
        ) -> None:
        super().__init__(interval)

        self.update_flag = update_flag
        self.dropped_flag = dropped_flag

    def run(self, tetromino: Tetromino, well: Well):
        tetromino.y += 1

        if well.check_overlap(tetromino) or well.check_oob(tetromino):
            tetromino.y -= 1
            self.dropped_flag.set()
        else:
            self.update_flag.set()

class TetrominoController(RecurringTimer):
    def __init__(self, interval: float, update_flag: Event) -> None:
        super().__init__(interval)

        self.update_flag = update_flag

    def run(self, screen: Screen, tetromino: Tetromino, well: Well):
        screen.wait_for_input(self.interval)

        old_x, old_y = tetromino.x, tetromino.y
        event = screen.get_event()
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.KEY_DOWN:
                tetromino.y += 1
            elif key == Screen.KEY_LEFT:
                tetromino.x -= 1
            elif key == Screen.KEY_RIGHT:
                tetromino.x += 1

        if well.check_overlap(tetromino) or well.check_oob(tetromino):
            tetromino.x, tetromino.y = old_x, old_y
        else:
            self.update_flag.set()
        