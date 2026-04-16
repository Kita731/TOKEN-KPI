"""
背景儲存工作者 — 由 hook_stop.py 呼叫，在背景計算並 upsert 到 sessions.csv
不會阻塞 Claude Code 的回應速度
"""
import csv
import json
import os
import sys
import tempfile
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


class _FileLock:
    """跨平台 CSV 檔案鎖，防止多個 bg_save worker 同時寫入造成資料損壞。"""

    def __init__(self, lock_path: Path, timeout: float = 15.0):
        self.lock_path = lock_path
        self.timeout = timeout

    def __enter__(self):
        deadline = time.time() + self.timeout
        while True:
            try:
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    age = time.time() - self.lock_path.stat().st_mtime
                    if age > 60:  # 超過 60 秒視為殭屍鎖，強制清除
                        self.lock_path.unlink(missing_ok=True)
                        continue
                except OSError:
                    pass
                if time.time() >= deadline:
                    self.lock_path.unlink(missing_ok=True)
                    continue
                time.sleep(0.05)

    def __exit__(self, *_):
        self.lock_path.unlink(missing_ok=True)


def upsert_csv(row: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    lock_path = DATA_DIR / "sessions.csv.lock"

    with _FileLock(lock_path):
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

        # 原子性寫入：先寫暫存檔，成功後才替換原檔，crash 不會損毀資料
        tmp_fd, tmp_path = tempfile.mkstemp(dir=DATA_DIR, suffix=".tmp")
        try:
            with os.fdopen(tmp_fd, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(existing)
            os.replace(tmp_path, SESSIONS_CSV)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise


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
