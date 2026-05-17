import json
import os
from datetime import datetime


class ExperimentTracker:
    def __init__(self, project_root: str = None, version: str = "v1"):
        workspace_dir = os.path.abspath(project_root or os.getcwd())
        self.version = version
        self.workspace_dir = workspace_dir
        self.experiments_dir = os.path.join(self.workspace_dir, "experiments")
        self.save_dir = os.path.join(self.experiments_dir, f"experiment_{version}")
        os.makedirs(self.save_dir, exist_ok=True)
        self.metrics_file = os.path.join(self.save_dir, "metrics.json")

    def log_artifact(self, name: str, data):
        artifact_path = os.path.join(self.save_dir, name)
        os.makedirs(os.path.dirname(artifact_path), exist_ok=True)

        if isinstance(data, (list, tuple)):
            with open(artifact_path, "w", encoding="utf-8") as f:
                for item in data:
                    f.write(str(item) + "\n")
        else:
            with open(artifact_path, "w", encoding="utf-8") as f:
                f.write(str(data))

    def log_metrics(self, metrics: dict):
        existing = {}
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, OSError):
                existing = {}

        timestamp = datetime.utcnow().isoformat()
        existing[timestamp] = metrics

        with open(self.metrics_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

    def log_text_report(self, name: str, text: str):
        report_path = os.path.join(self.save_dir, name)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(text)
