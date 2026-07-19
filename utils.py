from pathlib import Path


def get_desktop():
    d = Path.home() / "Desktop"
    return d if d.exists() else Path.home()
