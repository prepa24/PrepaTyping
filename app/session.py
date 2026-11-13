
from PySide6.QtCore import QElapsedTimer


class TypingSession:
    def __init__(self):
        self.elapsed_timer = QElapsedTimer()
        self.started = False
        self.finished = False
        self.final_elapsed_seconds = 0.0

    def start(self):
        if self.started or self.finished:
            return

        self.elapsed_timer.start()
        self.started = True

    def finish(self):
        if not self.started or self.finished:
            return

        self.final_elapsed_seconds = (
            self.elapsed_timer.elapsed() / 1000
        )

        self.finished = True
        self.started = False

    def reset(self):
        self.elapsed_timer.invalidate()
        self.started = False
        self.finished = False
        self.final_elapsed_seconds = 0.0

    def elapsed_seconds(self):
        if self.finished:
            return self.final_elapsed_seconds

        if not self.started:
            return 0.0

        return self.elapsed_timer.elapsed() / 1000
