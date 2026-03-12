from pathlib import Path

class FolderWatcher:
    def __init__(self, folder: str) -> None:
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self._seen: set[str] = set()

    def poll_new_files(self) -> list[Path]:
        current = {
            str(path)
            for path in self.folder.iterdir()
            if path.is_file()
        }
        new_files = sorted(Path(path) for path in (current - self._seen))
        self._seen.update(str(path) for path in new_files)
        return new_files
