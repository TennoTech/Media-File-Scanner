import os
from pathlib import Path

# --- File Type Extensions ---
EXTENSIONS = {
    "photos": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif", ".heic", ".heif", ".dng", ".arw", ".cr2", ".cr3", ".nef", ".orf", ".rw2", ".avif"},
    "videos": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".3gp", ".3g2", ".ts"},
    "audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".opus", ".wma", ".m4a", ".aiff", ".aif", ".amr", ".m4b"},
    "pdf": {".pdf"},
    "document": {".csv", ".tsv", ".docx", ".doc", ".odt", ".rtf", ".xlsx", ".xls", ".ods", ".xlsm"},
    "text": {".txt", ".log", ".md", ".rst", ".ini", ".cfg", ".conf", ".json", ".xml", ".yaml", ".yml", ".toml"},
    "zip": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz", ".tar.gz", ".tar.bz2", ".tar.xz"}
}

IGNORED_KEYWORDS = ["anki"]

# --- UI Log Tags ---
TAG_FOLDER = "folder"
TAG_OK = "ok"
TAG_SKIP = "skip"
TAG_ERR = "err"
TAG_INFO = "info"
TAG_DONE = "done"

def should_skip(path_parts):
    """Checks if any folder in the path contains ignored keywords."""
    return any(kw in part.lower() for part in path_parts for kw in IGNORED_KEYWORDS)

def get_desktop_path():
    """Returns Default Destination Path safely."""
    d = Path.home() / "Desktop"
    return d / "Media_Backup" if d.exists() else Path.home() / "Media_Backup"