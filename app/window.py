from app.results_dialog import ResultsDialog
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QWidget,
    QMessageBox,
)
from app.updater import UpdateChecker
from app.version import APP_VERSION
import sys
from pathlib import Path
from PySide6.QtGui import QIcon
from app.history_dialog import HistoryDialog
from sqlite3 import Error as SQLiteError
from app.database import initialize_database, save_session

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
        if getattr(sys, "frozen", False):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent

        icon_path = base_dir / "assets" / "prepatyping.png"

        self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1000, 650)

        self.session = TypingSession()
        self.lesson_manager = LessonManager("beginner")

        self.current_level = "beginner"
        self.current_lesson = None
        self.exercise_results = {}
        self.session_saved = False
        initialize_database()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)

        self.setup_ui()
        self.apply_styles()

        self.level_selector.currentIndexChanged.connect(
            self.change_level
        )

        self.update_progress()
        # Check for updates in background
        self.update_checker = UpdateChecker(self)

        self.update_checker.update_available.connect(
            self.show_update_notification
        )

        self.update_checker.no_update.connect(
            self.on_no_update
        )

        self.update_checker.check_failed.connect(
            self.on_update_error
        )

        self.update_checker.start()


    #sa pou styles
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
        self.exercise_results.clear()
        self.session_saved = False
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

        current, total = self.lesson_manager.get_progress()

        if current >= total and total > 0:
            if not self.show_final_results():
                return
            # Prepare a new exercise cycle
            self.current_lesson = None
            self.exercise_results.clear()
            self.session_saved = False

            # Reset the lesson sequence
            self.lesson_manager.set_level(
                self.current_level
            )

            self.timer.stop()
            self.session.reset()

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
            return

        self.current_lesson = (
            self.lesson_manager.next_lesson()
        )

        if self.current_lesson is not None:
            self.start_practice()


    
    def get_next_level(self):
        levels = [
            "beginner",
            "intermediate",
            "advanced",
            "python",
        ]

        current_index = levels.index(self.current_level)

        if current_index + 1 < len(levels):
            return levels[current_index + 1]

        return None


    def advance_to_next_level(self):
        next_level = self.get_next_level()

        if next_level is None:
            QMessageBox.information(
                self,
                "All Levels Completed",
                "Congratulations! You have completed all levels."
            )
            return

        index = self.level_selector.findData(next_level)

        if index >= 0:
            self.level_selector.setCurrentIndex(index)
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

    def finish_practice(self):

        if self.session.finished:
            return

        self.session.finish()
        self.timer.stop()

        self.update_stats()

        typed = self.typing_input.toPlainText()
        elapsed = self.session.elapsed_seconds()

        result = {
            "wpm": calculate_wpm(typed, elapsed),
            "accuracy": calculate_accuracy(
                self.target_text, typed
            ),
            "time": elapsed,
        }

        current, total = self.lesson_manager.get_progress()

        self.exercise_results[current] = result

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


    
    
    def show_final_results(self):

        if not self.exercise_results:
            return

        results = list(self.exercise_results.values())
        total = len(results)

        average_wpm = sum(
            result["wpm"] for result in results
        ) / total

        average_accuracy = sum(
            result["accuracy"] for result in results
        ) / total

        total_seconds = sum(
            result["time"] for result in results
        )

        # Save once per completed cycle
        if not self.session_saved:
            try:
                save_session(
                    level=self.current_level,
                    exercises_completed=total,
                    average_wpm=average_wpm,
                    average_accuracy=average_accuracy,
                    total_seconds=total_seconds,
                )

            except SQLiteError as error:
                QMessageBox.warning(
                    self,
                    "Database Error",
                    f"Could not save session:\n{error}"
                )

                # Do not mark the session as saved
                return False

            self.session_saved = True

        
        dialog = ResultsDialog(
            level=self.current_level,
            exercises=total,
            average_wpm=average_wpm,
            average_accuracy=average_accuracy,
            total_seconds=total_seconds,
            parent=self,
        )

        dialog.exec()

        self.advance_to_next_level()

        return True


    def show_history(self):
        dialog = HistoryDialog(self)
        dialog.exec()

    def show_update_notification(self, version, url):
        reply = QMessageBox.question(
            self,
            "Update Available",
            (
                f"PrepaTyping {version} is available!\n\n"
                f"Current version: {APP_VERSION}\n\n"
                "Would you like to open the download page?"
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            import webbrowser
            webbrowser.open(url)


    def on_no_update(self):
        print("PrepaTyping: No update available.")


    def on_update_error(self, error):
        print(f"Update check failed: {error}")