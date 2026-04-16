"""
背景儲存工作者 — 由 hook_stop.py 呼叫，在背景計算並 upsert 到 sessions.csv
不會阻塞 Claude Code 的回應速度
"""
import csv
import json
import sys
import time
from datetime import date
from pathlib import Path

SESSION_DIR  = Path.home() / ".claude" / "kpi-sessions"
KPI_DIR      = Path(__file__).parent.parent
DATA_DIR     = KPI_DIR / "data"
SESSIONS_CSV = DATA_DIR / "sessions.csv"

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

FIELDNAMES = [
    "date", "session_id", "project",
    "total_tasks", "passed_first_try", "tcr",
    "avg_iterations", "ic",
    "lines_generated", "lines_kept", "car",
    "ttwc_claude_min", "ttwc_manual_estimate_min", "ttwc_ratio",
    "notes",
]


def load_events(path: Path) -> list[dict]:
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return events


def compute(events: list[dict], session_id: str) -> dict:
    stop_count = sum(1 for e in events if e.get("type") == "stop")
    lines_gen  = sum(
        e.get("lines", 0) for e in events
        if e.get("type") == "tool" and e.get("tool") in WRITE_TOOLS
    )
    ts_list   = [e["ts"] for e in events if "ts" in e]
    duration  = round((max(ts_list) - min(ts_list)) / 60, 1) if len(ts_list) >= 2 else 0
    cwd_event = next((e for e in events if e.get("type") == "cwd"), None)
    project   = Path(cwd_event["cwd"]).name if cwd_event else ""

    return {
        "date":                     str(date.today()),
        "session_id":               session_id,
        "project":                  project,
        "total_tasks":              "",
        "passed_first_try":         "",
        "tcr":                      "",
        "avg_iterations":           max(stop_count, 1),
        "ic":                       max(stop_count, 1),
        "lines_generated":          lines_gen,
        "lines_kept":               "",
        "car":                      "",
        "ttwc_claude_min":          duration,
        "ttwc_manual_estimate_min": "",
        "ttwc_ratio":               "",
        "notes":                    "[auto]",
    }


def upsert_csv(row: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    existing: list[dict] = []
    found = False

    if SESSIONS_CSV.exists() and SESSIONS_CSV.stat().st_size > 0:
        with open(SESSIONS_CSV, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                if r.get("session_id") == row["session_id"]:
                    # 保留使用者手動填寫的欄位，只更新自動偵測的欄位
                    merged = dict(r)
                    for auto_key in ("ic", "avg_iterations", "lines_generated", "ttwc_claude_min", "date", "project"):
                        merged[auto_key] = row[auto_key]
                    if not merged.get("notes") or merged["notes"] == "[auto]":
                        merged["notes"] = row["notes"]
                    existing.append(merged)
                    found = True
                else:
                    existing.append(r)

    if not found:
        existing.append(row)

    with open(SESSIONS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing)


def main():
    if len(sys.argv) < 2:
        return
    session_id = sys.argv[1]
    log_file   = SESSION_DIR / f"{session_id}.jsonl"

    if not log_file.exists():
        return

    events = load_events(log_file)
    if not events:
        return

    row = compute(events, session_id)
    upsert_csv(row)


if __name__ == "__main__":
    main()
