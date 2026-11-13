
LESSONS = {
    "beginner": [
        "The cat is on the mat.",
        "I like to learn Python.",
        "Practice makes progress.",
        "My keyboard is ready.",
    ],
    "intermediate": [
        "Typing every day helps improve your speed.",
        "Python is a powerful programming language.",
        "Accuracy is more important than speed.",
    ],
    "advanced": [
        "Consistent practice develops muscle memory and improves typing accuracy over time.",
        "Software development requires patience, logical thinking, and attention to detail.",
    ],
    "python": [
        "print('Hello World')",
        "name = 'PrepaTyping'",
        "for i in range(10):",
        "def calculate_wpm(words, minutes):",
    ],
}


def get_lessons(level: str) -> list[str]:
    return LESSONS.get(level, [])
