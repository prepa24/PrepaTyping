
import json
import urllib.request
import urllib.error

from PySide6.QtCore import QThread, Signal

from app.version import APP_VERSION, GITHUB_API_URL


def parse_version(version):
    version = version.strip().lstrip("v")

    parts = version.split(".")

    if len(parts) != 3:
        raise ValueError("Invalid version format")

    return tuple(int(part) for part in parts)


class UpdateChecker(QThread):

    update_available = Signal(str, str)
    no_update = Signal()
    check_failed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            request = urllib.request.Request(
                GITHUB_API_URL,
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "PrepaTyping-Updater",
                },
            )

            with urllib.request.urlopen(
                request, timeout=10
            ) as response:
                data = json.load(response)

            latest_version = data["tag_name"]
            release_url = data["html_url"]

            if (
                parse_version(latest_version)
                > parse_version(APP_VERSION)
            ):
                self.update_available.emit(
                    latest_version,
                    release_url,
                )
            else:
                self.no_update.emit()

        except urllib.error.HTTPError as error:
            if error.code == 404:
                self.no_update.emit()
            else:
                self.check_failed.emit(
                    f"GitHub HTTP error: {error.code}"
                )

        except (
            urllib.error.URLError,
            TimeoutError,
            ValueError,
            KeyError,
            OSError,
        ) as error:
            self.check_failed.emit(str(error))
