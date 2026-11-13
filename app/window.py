from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget
from app.ui import TypingUI
from app.styles import APP_STYLE
from app.session import TypingSession
from app.typing_engine import (
    calculate_accuracy,
    calculate_wpm,
)

class PrepaTyping(QWidget, TypingUI):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PrepaTyping")
        self.resize(1000, 600)
        self.session = TypingSession()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.setup_ui()
        self.apply_styles()


#sa se pou estyl
    def apply_styles(self):
        self.setStyleSheet(APP_STYLE)
    
    
    def start_practice(self):
        self.timer.stop()
        self.session.reset()

        self.typing_input.clear()
        self.typing_input.setEnabled(True)
        self.typing_input.setFocus()

        self.wpm_label.setText("0")
        self.accuracy_label.setText("100%")
        self.time_label.setText("00:00")

        self.start_button.setText("Restart Practice")


    
    
#sa se pou pati tape a
    
    
    def check_typing(self):
        target = self.practice_text.text()
        typed = self.typing_input.toPlainText()

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

        # Check whether the exercise is complete
        if len(typed) >= len(target):
            self.finish_practice()



    
    def finish_practice(self):
        if self.session.finished:
            return

        self.session.finish()
        self.timer.stop()

        self.update_stats()

        self.typing_input.setEnabled(False)
        self.start_button.setText("Try Again")





 #sa se pou opdet ekriti a   
    
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
        wpm = calculate_wpm(typed, elapsed_seconds)

        self.wpm_label.setText(str(wpm))
