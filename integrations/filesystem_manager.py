from datetime import datetime
from pathlib import Path
import shutil

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a"}

def _build_mission_dir(missions_root: Path, market: str) -> Path:
    today = datetime.now().strftime("%Y_%m_%d")
    mission_dir = missions_root / f"{today}_{market}"
    (mission_dir / "photos").mkdir(parents=True, exist_ok=True)
    (mission_dir / "videos").mkdir(parents=True, exist_ok=True)
    (mission_dir / "audio").mkdir(parents=True, exist_ok=True)
    return mission_dir

def organize_media(files: list[Path], missions_dir: str, market: str = "seg_plaza") -> list[Path]:
    missions_root = Path(missions_dir)
    mission_dir = _build_mission_dir(missions_root, market)
    moved: list[Path] = []

    for path in files:
        ext = path.suffix.lower()

        if ext in IMAGE_EXTENSIONS:
            target_dir = mission_dir / "photos"
        elif ext in VIDEO_EXTENSIONS:
            target_dir = mission_dir / "videos"
        elif ext in AUDIO_EXTENSIONS:
            target_dir = mission_dir / "audio"
        else:
            continue

        target = target_dir / path.name
        shutil.move(str(path), str(target))
        moved.append(target)

    return moved
