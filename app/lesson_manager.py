
import random

from app.lessons import get_lessons


class LessonManager:
    def __init__(self, level="beginner"):
        self.level = level
        self.lessons = []
        self.current_index = 0

        self.load_lessons()

    def load_lessons(self):
        self.lessons = get_lessons(self.level).copy()
        random.shuffle(self.lessons)
        self.current_index = 0

    def set_level(self, level):
        self.level = level
        self.load_lessons()

    def next_lesson(self):
        if not self.lessons:
            return None

        if self.current_index >= len(self.lessons):
            self.load_lessons()

        lesson = self.lessons[self.current_index]
        self.current_index += 1

        return lesson

    def get_progress(self):
        return self.current_index, len(self.lessons)
