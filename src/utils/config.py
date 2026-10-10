"""Configuration management: loads settings from config/config.json."""
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "config.json")

DEFAULTS = {
    "data_file": "data/students.json",
    "export_file": "data/students_export.csv",
    "log_file": "logs/app.log",
    "log_level": "INFO",
}


def load_config(path=CONFIG_PATH):
    """Return settings merged over defaults. Paths are resolved to absolute.

    Environment variables (e.g. SIS_DATA_FILE) override the file, which is
    handy in cloud/container deployments.
    """
    settings = dict(DEFAULTS)
    try:
        with open(path, "r", encoding="utf-8") as f:
            settings.update(json.load(f))
    except FileNotFoundError:
        pass  # fall back to defaults
    except json.JSONDecodeError as exc:
        raise ValueError(f"Config file is not valid JSON: {exc}")

    for key in list(settings):
        env_value = os.environ.get(f"SIS_{key.upper()}")
        if env_value:
            settings[key] = env_value

    for key in ("data_file", "export_file", "log_file"):
        if not os.path.isabs(settings[key]):
            settings[key] = os.path.join(ROOT_DIR, settings[key])
    return settings
