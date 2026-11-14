
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QFrame,
    QComboBox,
    QProgressBar,
)
from html import escape

from app.typing_engine import compare_characters


class TypingUI:

    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        # Application title
        title = QLabel("⌨ PrepaTyping")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel(
            "Improve your typing speed every day."
        )
        layout.addWidget(subtitle)

        # Statistics cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        wpm_card, self.wpm_label = self.create_stat_card(
            "WPM", "0"
        )

        accuracy_card, self.accuracy_label = (
            self.create_stat_card("Accuracy", "100%")
        )

        time_card, self.time_label = self.create_stat_card(
            "Time", "00:00"
        )

        stats_layout.addWidget(wpm_card)
        stats_layout.addWidget(accuracy_card)
        stats_layout.addWidget(time_card)

        layout.addLayout(stats_layout)

        # Level selection
        self.level_selector = QComboBox()

        self.level_selector.addItem("Beginner", "beginner")
        self.level_selector.addItem("Intermediate", "intermediate")
        self.level_selector.addItem("Advanced", "advanced")
        self.level_selector.addItem("Python", "python")

        self.level_selector.setObjectName("levelSelector")
        layout.addWidget(self.level_selector)

        # Exercise progress
        self.progress_label = QLabel("Exercise 0/0")
        self.progress_label.setObjectName("progressLabel")
        layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setObjectName("exerciseProgress")
        layout.addWidget(self.progress_bar)

        # Practice text
        self.target_text = (
            "The first logiciel Python with ChatGPT."
        )

        self.practice_text = QLabel()
        self.practice_text.setText(self.target_text)
        self.practice_text.setWordWrap(True)
        self.practice_text.setObjectName("practiceText")

        layout.addWidget(self.practice_text)

        # Typing input
        self.typing_input = QTextEdit()
        self.typing_input.setPlaceholderText(
            "Start typing here..."
        )
        self.typing_input.setEnabled(False)
        self.typing_input.textChanged.connect(
            self.check_typing
        )

        layout.addWidget(self.typing_input)

        # Practice action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.start_button = QPushButton("Start Practice")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(
            self.start_practice
        )

        self.next_button = QPushButton("Next Exercise")
        self.next_button.setObjectName("nextButton")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(
            self.next_exercise
        )

        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.next_button)

        layout.addLayout(buttons_layout)

        # History button
        self.history_button = QPushButton("View History")
        self.history_button.setObjectName("historyButton")
        self.history_button.clicked.connect(
            self.show_history
        )

        layout.addWidget(self.history_button)

        self.setLayout(layout)

    def create_stat_card(self, label, value):
        card = QFrame()
        card.setObjectName("statCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(5)

        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        name_label = QLabel(label)
        name_label.setObjectName("statName")
        name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        card_layout.addWidget(value_label)
        card_layout.addWidget(name_label)

        return card, value_label

    def highlight_characters(self, target: str, typed: str):
        results = compare_characters(target, typed)

        colors = {
            "correct": "#22c55e",
            "incorrect": "#ef4444",
            "pending": "#e2e8f0",
        }

        highlighted_text = []

        for index, status in enumerate(results):
            character = escape(target[index])
            color = colors[status]

            highlighted_text.append(
                f'<span style="color: {color};">'
                f'{character}</span>'
            )

        self.practice_text.setText(
            "".join(highlighted_text)
        )
