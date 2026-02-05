# discontinuity.py
import json
import os
from datetime import datetime

FILE = "discontinuity.json"

def load_discontinuity():
    if not os.path.exists(FILE):
        return {
            "boot_count": 0,
            "last_shutdown": None,
            "last_boot": None,
            "total_downtime_seconds": 0,
            "longest_gap_seconds": 0
        }
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def register_boot():
    data = load_discontinuity()
    now = datetime.now()

    if data["last_shutdown"]:
        last = datetime.fromisoformat(data["last_shutdown"])
        gap = (now - last).total_seconds()
        data["total_downtime_seconds"] += gap
        data["longest_gap_seconds"] = max(
            data["longest_gap_seconds"], gap
        )

    data["boot_count"] += 1
    data["last_boot"] = now.isoformat()

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data

def register_shutdown():
    data = load_discontinuity()
    data["last_shutdown"] = datetime.now().isoformat()

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
