"""
This script will manages operations realted to files
"""
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = Path("data/documents")

def ensure_dir(path_str: str):
    path = Path(path_str)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {path}")
    else:
        print(f"Folder already exists: {path}")

def get_save_path(filename: str) -> Path:
    """
    Return folder path to save upload doc
    """
    now = datetime.now()
    folder = BASE_PATH / str(now.year) / f"{now.month:02d}" / f"{now.day:02d}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / filename
