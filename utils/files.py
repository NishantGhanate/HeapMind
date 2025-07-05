"""
This script will manages operations realted to files
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def ensure_dir(path_str: str):
    path = Path(path_str)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {path}")
    else:
        print(f"Folder already exists: {path}")

def get_save_path(filename: str) -> Path:
    data_dir = PROJECT_ROOT / "data" / "documents"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / filename
