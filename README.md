# ⌨️ PrepaTyping

**An offline typing practice application for Linux, built with Python and PySide6.**

PrepaTyping helps users improve their typing speed, accuracy, and consistency through structured lessons, real-time feedback, and local progress tracking.

## Features

- **Three difficulty levels:** Beginner, Intermediate, and Advanced
- **Structured typing lessons** with exercise progression
- **Real-time statistics:** Words Per Minute (WPM), accuracy, and elapsed time
- **Practice history:** Review previous sessions and performance
- **Session statistics:** Track average speed and accuracy
- **SQLite database:** Store practice history locally
- **Offline functionality:** Practice without an internet connection
- **Dark-themed interface:** A clean desktop experience
- **Update checker:** Check GitHub Releases for newer versions when internet access is available

## Technologies

- Python 3
- PySide6 (Qt for Python)
- SQLite
- PyInstaller
- Git and GitHub

## Download

The first official release is available here:

[Download PrepaTyping v1.0.0](https://github.com/prepa24/PrepaTyping/releases/tag/v1.0.0)

**Platform:** Linux x86_64

## Installation on Linux

1. Download `PrepaTyping-v1.0.0-linux-x86_64.tar.gz` from the release page.
2. Extract the archive.
3. Open a terminal inside the extracted directory.
4. Run the application:

```bash
./PrepaTyping
```

If executable permission is missing, run:

```bash
chmod +x PrepaTyping
./PrepaTyping
```

The application does not require a separate Python installation when using the packaged release.

Compatibility may vary between Linux distributions.

## Run from Source

Clone the repository:

```bash
git clone https://github.com/prepa24/PrepaTyping.git
cd PrepaTyping
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python main.py
```

## Data Storage

PrepaTyping uses SQLite to store practice history locally.

On Linux, the default database location is:

```text
~/.local/share/PrepaTyping/prepatyping.db
```

If `XDG_DATA_HOME` is configured, PrepaTyping uses that directory instead.

Practice data is stored separately from application files to help preserve user history during application updates.

## Updates

PrepaTyping includes a GitHub Releases update checker.

When a newer version is detected, users can open the official release page to download it.

Updates are not installed automatically.

## Project Structure

```text
PrepaTyping/
├── app/
│   ├── database.py
│   ├── history_dialog.py
│   ├── lesson_manager.py
│   ├── lessons.py
│   ├── results_dialog.py
│   ├── session.py
│   ├── styles.py
│   ├── typing_engine.py
│   ├── ui.py
│   ├── updater.py
│   ├── version.py
│   └── window.py
├── assets/
│   └── prepatyping.png
├── main.py
├── requirements.txt
└── README.md
```

## Version

**Current release:** v1.0.0

**Status:** First official Linux release

## Feedback and Issues

Found a bug or have a feature suggestion?

[Open an issue on GitHub](https://github.com/prepa24/PrepaTyping/issues)

## Project Repository

[github.com/prepa24/PrepaTyping](https://github.com/prepa24/PrepaTyping)

---

Built with Python, PySide6, and a focus on improving typing skills.