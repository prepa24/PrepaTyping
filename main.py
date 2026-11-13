

import sys

from PySide6.QtWidgets import QApplication
from app.window import PrepaTyping


def main():
    app = QApplication(sys.argv)

    window = PrepaTyping()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
