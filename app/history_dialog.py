
from datetime import datetime

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
)

from PySide6.QtCore import Qt

from app.database import get_practice_history


class HistoryDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Practice History")
        self.resize(850, 500)

        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: white;
            }

            QLabel {
                color: #22c55e;
                font-size: 24px;
                font-weight: bold;
            }

            QTableWidget {
                background-color: #1e293b;
                color: white;
                gridline-color: #334155;
                border: none;
                selection-background-color: #0369a1;
            }

            QHeaderView::section {
                background-color: #334155;
                color: white;
                padding: 8px;
                border: none;
            }

            QPushButton {
                background-color: #0284c7;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #0369a1;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        title = QLabel("Practice History")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Level",
            "Exercises",
            "WPM",
            "Accuracy",
            "Time",
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        layout.addWidget(self.table)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.load_history()

    def load_history(self):
        history = get_practice_history()

        self.table.setRowCount(len(history))

        for row_index, session in enumerate(history):

            completed_at = datetime.fromisoformat(
                session["completed_at"]
            )

            date_text = completed_at.strftime(
                "%Y-%m-%d %I:%M %p"
            )

            total_seconds = session["total_seconds"]
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)

            values = [
                date_text,
                session["level"].title(),
                str(session["exercises_completed"]),
                f'{session["average_wpm"]:.1f}',
                f'{session["average_accuracy"]:.1f}%',
                f"{minutes:02d}:{seconds:02d}",
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(
                    row_index,
                    column,
                    item
                )
