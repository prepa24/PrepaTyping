
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
    QFrame,
    QAbstractItemView,
)

from app.database import get_practice_history


class HistoryDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Practice History")
        self.resize(1050, 650)
        self.setMinimumSize(850, 500)

        self.history = []

        self.setup_ui()
        self.apply_styles()
        self.load_history()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        # Title
        title = QLabel("Practice History")
        title.setObjectName("historyTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Filters
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(15)

        self.level_filter = QComboBox()
        self.level_filter.addItem("All Levels", "all")
        self.level_filter.addItem("Beginner", "beginner")
        self.level_filter.addItem(
            "Intermediate", "intermediate"
        )
        self.level_filter.addItem("Advanced", "advanced")
        self.level_filter.addItem("Python", "python")

        self.sort_filter = QComboBox()
        self.sort_filter.addItem("Newest First", "newest")
        self.sort_filter.addItem("Oldest First", "oldest")

        filters_layout.addWidget(self.level_filter)
        filters_layout.addWidget(self.sort_filter)

        layout.addLayout(filters_layout)

        # Statistics
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        sessions_card, self.sessions_label = (
            self.create_stat_card("Total Sessions", "0")
        )

        wpm_card, self.average_wpm_label = (
            self.create_stat_card("Average WPM", "0")
        )

        accuracy_card, self.average_accuracy_label = (
            self.create_stat_card("Average Accuracy", "0%")
        )

        stats_layout.addWidget(sessions_card)
        stats_layout.addWidget(wpm_card)
        stats_layout.addWidget(accuracy_card)

        layout.addLayout(stats_layout)

        # History table
        self.table = QTableWidget()
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Date & Time",
            "Level",
            "Exercises",
            "WPM",
            "Accuracy",
            "Time",
        ])

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)

        layout.addWidget(self.table)

        # Empty history message
        self.empty_label = QLabel(
            "No practice sessions found."
        )
        self.empty_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.empty_label.setObjectName("emptyLabel")
        self.empty_label.hide()

        layout.addWidget(self.empty_label)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        # Signals
        self.level_filter.currentIndexChanged.connect(
            self.apply_filters
        )

        self.sort_filter.currentIndexChanged.connect(
            self.apply_filters
        )

    def create_stat_card(self, title, value):
        card = QFrame()
        card.setObjectName("historyStatCard")

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(5)

        value_label = QLabel(value)
        value_label.setObjectName("historyStatValue")
        value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title_label = QLabel(title)
        title_label.setObjectName("historyStatName")
        title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        card_layout.addWidget(value_label)
        card_layout.addWidget(title_label)

        return card, value_label

    def load_history(self):
        self.history = [
            dict(session)
            for session in get_practice_history()
        ]

        self.apply_filters()

    def apply_filters(self, *args):
        level = self.level_filter.currentData()
        sort_order = self.sort_filter.currentData()

        filtered = [
            session
            for session in self.history
            if level == "all"
            or session["level"].lower() == level
        ]

        filtered.sort(
            key=lambda session: datetime.fromisoformat(
                session["completed_at"]
            ),
            reverse=(sort_order == "newest"),
        )

        self.populate_table(filtered)
        self.update_statistics(filtered)

    def populate_table(self, history):
        self.table.setRowCount(len(history))

        self.empty_label.setVisible(not history)

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

        self.table.resizeRowsToContents()

    def update_statistics(self, history):
        total = len(history)

        self.sessions_label.setText(str(total))

        if total == 0:
            self.average_wpm_label.setText("0")
            self.average_accuracy_label.setText("0%")
            return

        average_wpm = sum(
            session["average_wpm"]
            for session in history
        ) / total

        average_accuracy = sum(
            session["average_accuracy"]
            for session in history
        ) / total

        self.average_wpm_label.setText(
            f"{average_wpm:.1f}"
        )

        self.average_accuracy_label.setText(
            f"{average_accuracy:.1f}%"
        )

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: white;
            }

            QLabel#historyTitle {
                color: #22c55e;
                font-size: 26px;
                font-weight: bold;
            }

            QLabel#emptyLabel {
                color: #94a3b8;
                font-size: 14px;
            }

            QFrame#historyStatCard {
                background-color: #1e293b;
                border-radius: 10px;
                min-height: 90px;
            }

            QLabel#historyStatValue {
                color: #38bdf8;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#historyStatName {
                color: #94a3b8;
                font-size: 13px;
            }

            QComboBox {
                background-color: #1e293b;
                color: white;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 10px;
            }

            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: white;
                selection-background-color: #0369a1;
            }

            QTableWidget {
                background-color: #1e293b;
                alternate-background-color: #243247;
                color: white;
                gridline-color: #334155;
                border: none;
                selection-background-color: #0369a1;
            }

            QHeaderView::section {
                background-color: #334155;
                color: white;
                padding: 10px;
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
