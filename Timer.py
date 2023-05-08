from time import sleep
from threading import Thread


class Timer:
    def __init__(self, color: bool):
        self.seconds: int = 900
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
                print(self.seconds)
                self.seconds -= 1
                sleep(1)

        assert self.seconds, f"Закончилось время у {self.color}. Противоположный игрок победил"

    def flip_the_timer(self):
        """Меняет положение таймера (активный/деактивный)"""

        self.expires = not self.expires

    def get_timeset(self) -> str:
        """:return время в виде таймера на электронных часах"""

        return f"{round(self.seconds / 60)}:{self.seconds % 60}"
