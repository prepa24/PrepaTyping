
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QFrame,
)


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

        # Practice text
        self.practice_text = QLabel(
            "The first logiciel Python with ChatGPT."
        )
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

        # Start button
        self.start_button = QPushButton(
            "Start Practice"
        )
        self.start_button.clicked.connect(
            self.start_practice
        )
        layout.addWidget(self.start_button)

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
