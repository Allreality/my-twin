"""State management — track processed message IDs to prevent reprocessing."""
import json
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import STATE_FILE


class State:
    def __init__(self):
        if STATE_FILE.exists():
            self.data = json.loads(STATE_FILE.read_text())
        else:
            self.data = {
                "processed_ids": [],
                "last_poll": None,
                "stats": {"total_processed": 0, "total_extracted": 0, "total_skipped": 0},
            }

    def is_processed(self, message_id: str) -> bool:
        return message_id in self.data["processed_ids"]

    def mark_processed(self, message_id: str, action: str):
        """action ∈ {extracted, skipped, flagged, error}"""
        if message_id not in self.data["processed_ids"]:
            self.data["processed_ids"].append(message_id)
            self.data["stats"]["total_processed"] += 1
            if action == "extracted":
                self.data["stats"]["total_extracted"] += 1
            elif action == "skipped":
                self.data["stats"]["total_skipped"] += 1

        # Cap stored IDs at 10000 — Gmail message IDs are stable, no need to keep forever
        if len(self.data["processed_ids"]) > 10000:
            self.data["processed_ids"] = self.data["processed_ids"][-10000:]

    def update_poll_time(self):
        self.data["last_poll"] = datetime.now().isoformat()

    def save(self):
        STATE_FILE.write_text(json.dumps(self.data, indent=2))
