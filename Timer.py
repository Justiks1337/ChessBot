from time import sleep
from threading import Thread
from BaseErrors import ChessError
from config.ConfigValues import ConfigValues


class Timer:
    def __init__(self, color: bool):
        self.seconds: int = ConfigValues.game_time
        self.expires: bool = color
        self.color = lambda x: "белых" if color else "чёрных"
        Thread(target=self.start_timer).start()

    def start_timer(self):
        """Запускает цикл событий"""

        self.update_timer()

    def update_timer(self):
        """Ведёт время отсчёта"""

        while self.seconds:
            if self.expires:
                self.seconds -= 1
                sleep(1)
        try:
            assert self.seconds
        except AssertionError:
            raise ChessError(ConfigValues.on_end_time.replace('{color}', self.color))

    def flip_the_timer(self):
        """Меняет положение таймера (активный/деактивный)"""

        self.expires = not self.expires

    def get_timeset(self) -> str:
        """:return время в виде таймера на электронных часах"""

        return f"{round(self.seconds / 60)}:{self.seconds % 60}"
