import json
import time
from pathlib import Path
from core.logging_utils import get_logger
from core.pipeline_launcher import run_lab6_pipeline
from core.watcher import FolderWatcher
from integrations.filesystem_manager import organize_media

logger = get_logger("agent37")

class AgentController:
    def __init__(self) -> None:
        self.settings = self._load_settings()
        self.watcher = FolderWatcher(self.settings["incoming_dir"])
        self.runtime_state_path = Path("state/runtime_state.json")

    def _load_settings(self) -> dict:
        with open("config/settings.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_runtime_state(self, detected_files: list[str], status: str) -> None:
        payload = {
            "last_run": time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_pipeline_status": status,
            "last_detected_files": detected_files,
        }
        with self.runtime_state_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def run(self) -> None:
        logger.info("Agent 37 started")
        logger.info("Watching folder: %s", self.settings["incoming_dir"])
        poll_interval = self.settings.get("poll_interval_seconds", 2)

        while True:
            new_files = self.watcher.poll_new_files()

            if new_files:
                logger.info("New files detected: %s", [str(f) for f in new_files])
                organized = organize_media(
                    files=new_files,
                    missions_dir=self.settings["missions_dir"],
                    market=self.settings.get("default_market", "seg_plaza"),
                )
                logger.info("Files organized: %s", [str(f) for f in organized])

                try:
                    run_lab6_pipeline()
                    self._write_runtime_state(
                        detected_files=[str(f) for f in organized],
                        status="success",
                    )
                    logger.info("Pipeline completed successfully")
                except Exception as exc:
                    self._write_runtime_state(
                        detected_files=[str(f) for f in organized],
                        status=f"error: {exc}",
                    )
                    logger.exception("Pipeline failed")

            time.sleep(poll_interval)
