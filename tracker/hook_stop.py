"""
Stop Hook — 每次 Claude 完成一次回應時觸發
記錄：stop 事件與時間戳記（用於計算 IC 來回次數）
"""
import sys
import json
import time
from pathlib import Path


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)

    session_id = data.get("session_id", "unknown")

    log_dir  = Path.home() / ".claude" / "kpi-sessions"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{session_id}.jsonl"

    event = {"ts": time.time(), "type": "stop"}

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()
