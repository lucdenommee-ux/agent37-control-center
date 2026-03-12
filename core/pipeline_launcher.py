import json
import subprocess
import sys
from pathlib import Path
from core.logging_utils import get_logger

logger = get_logger("pipeline_launcher")

def load_settings() -> dict:
    settings_path = Path("config/settings.json")
    with settings_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def run_lab6_pipeline() -> None:
    settings = load_settings()
    steps = settings.get("pipeline_steps", [])
    for step in steps:
        logger.info("Running pipeline step: %s", step)
        subprocess.run([sys.executable, step], check=True)
