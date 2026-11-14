
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class ResultsDialog(QDialog):
    def __init__(
        self,
        level,
        exercises,
        average_wpm,
        average_accuracy,
        total_seconds,
        parent=None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Practice Completed!")
        self.setMinimumSize(520, 430)

        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #f8fafc;
            }

            QLabel {
                color: #f8fafc;
                font-size: 15px;
            }

            QLabel#resultTitle {
                color: #22c55e;
                font-size: 26px;
                font-weight: bold;
            }

            QLabel#resultValue {
                color: #38bdf8;
                font-size: 29px;
                font-weight: bold;
            }

            QFrame#resultCard {
                background-color: #1e293b;
                border-radius: 12px;
            }

            QPushButton {
                background-color: #0284c7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #0369a1;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(18)

        title = QLabel("Practice Completed!")
        title.setObjectName("resultTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            f"Level: {level.title()} | "
            f"Exercises Completed: {exercises}"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        stats_layout.addWidget(
            self.create_card(
                "Average WPM",
                f"{average_wpm:.1f}"
            )
        )

        stats_layout.addWidget(
            self.create_card(
                "Accuracy",
                f"{average_accuracy:.1f}%"
            )
        )

        layout.addLayout(stats_layout)

        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)

        time_label = QLabel(
            f"Total Time: {minutes:02d}:{seconds:02d}"
        )
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(time_label)

        self.close_button = QPushButton("Continue")
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)

    def create_card(self, name, value):
        card = QFrame()
        card.setObjectName("resultCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        value_label = QLabel(value)
        value_label.setObjectName("resultValue")
        value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        name_label = QLabel(name)
        name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(value_label)
        layout.addWidget(name_label)

        return card
