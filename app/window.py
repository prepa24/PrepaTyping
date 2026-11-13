
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget

from app.ui import TypingUI
from app.styles import APP_STYLE
from app.session import TypingSession
from app.lesson_manager import LessonManager

from app.typing_engine import (
    calculate_accuracy,
    calculate_wpm,
)


class PrepaTyping(QWidget, TypingUI):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PrepaTyping")
        self.resize(1000, 650)

        self.session = TypingSession()
        self.lesson_manager = LessonManager("beginner")

        self.current_level = "beginner"
        self.current_lesson = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)

        self.setup_ui()
        self.apply_styles()

        self.level_selector.currentIndexChanged.connect(
            self.change_level
        )

        self.update_progress()

    def apply_styles(self):
        self.setStyleSheet(APP_STYLE)

    # Update progress indicator
    def update_progress(self):
        current, total = self.lesson_manager.get_progress()

        self.progress_label.setText(
            f"Exercise {current}/{total}"
        )

        if total > 0:
            percentage = int((current / total) * 100)
        else:
            percentage = 0

        self.progress_bar.setValue(percentage)

    # Change exercise level
    def change_level(self, index):
        level = self.level_selector.currentData()

        if level == self.current_level:
            return

        self.timer.stop()
        self.session.reset()

        self.lesson_manager.set_level(level)
        self.current_level = level
        self.current_lesson = None

        self.typing_input.blockSignals(True)
        self.typing_input.clear()
        self.typing_input.blockSignals(False)

        self.typing_input.setEnabled(False)

        self.target_text = ""
        self.practice_text.clear()

        self.wpm_label.setText("0")
        self.accuracy_label.setText("100%")
        self.time_label.setText("00:00")

        self.start_button.setText("Start Practice")
        self.next_button.setEnabled(False)

        self.update_progress()

    # Start or restart current exercise
    def start_practice(self):

        if self.current_lesson is None:
            self.current_lesson = (
                self.lesson_manager.next_lesson()
            )

        if self.current_lesson is None:
            return

        self.target_text = self.current_lesson

        self.timer.stop()
        self.session.reset()

        self.typing_input.blockSignals(True)
        self.typing_input.clear()
        self.typing_input.blockSignals(False)

        self.practice_text.setText(self.target_text)

        self.typing_input.setEnabled(True)
        self.typing_input.setFocus()

        self.wpm_label.setText("0")
        self.accuracy_label.setText("100%")
        self.time_label.setText("00:00")

        self.start_button.setText("Restart Practice")
        self.next_button.setEnabled(False)

        self.update_progress()

    # Load next exercise
    def next_exercise(self):

        if not self.session.finished:
            return

        self.current_lesson = (
            self.lesson_manager.next_lesson()
        )

        if self.current_lesson is None:
            return

        self.start_practice()

    # Check typing
    def check_typing(self):

        if not self.target_text:
            return

        if self.session.finished:
            return

        target = self.target_text
        typed = self.typing_input.toPlainText()

        self.highlight_characters(target, typed)

        if not typed:
            self.accuracy_label.setText("100%")
            self.update_stats()
            return

        if not self.session.started:
            self.session.start()
            self.timer.start(1000)

        accuracy = calculate_accuracy(target, typed)

        self.accuracy_label.setText(
            f"{accuracy:.1f}%"
        )

        self.update_stats()

        if len(typed) >= len(target):
            self.finish_practice()

    # Finish current exercise
    def finish_practice(self):

        if self.session.finished:
            return

        self.session.finish()
        self.timer.stop()

        self.update_stats()

        self.typing_input.setEnabled(False)

        self.start_button.setText("Restart Practice")
        self.next_button.setEnabled(True)

    # Update statistics
    def update_stats(self):

        if not self.session.started and not self.session.finished:
            return

        elapsed_seconds = self.session.elapsed_seconds()

        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)

        self.time_label.setText(
            f"{minutes:02d}:{seconds:02d}"
        )

        typed = self.typing_input.toPlainText()

        wpm = calculate_wpm(
            typed,
            elapsed_seconds
        )

        self.wpm_label.setText(str(wpm))
