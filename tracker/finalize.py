"""
Session 結算腳本 — 在 session 結束後執行

自動計算：
  IC   來回次數（stop 事件數）
  Lines Generated（Write / Edit 行數總和）
  CAR  透過 git diff 估算保留行數
  TTWC Claude 花費時間（分鐘）
  Project（工作目錄名稱）

只需手動輸入：
  total_tasks / passed_first_try（用於 TCR）
  手寫估計時間（用於 TTWC ratio）

用法：
  python tracker/finalize.py                    # 互動模式
  python tracker/finalize.py 5 4                # total=5, passed=4
  python tracker/finalize.py 5 4 --open         # 完成後開瀏覽器
"""

import argparse
import json
import os
import subprocess
import sys
import time
import webbrowser
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlencode

# ── 路徑設定 ──────────────────────────────────────────────
KPI_DIR      = Path(__file__).parent.parent
DATA_DIR     = KPI_DIR / "data"
SESSION_DIR  = Path.home() / ".claude" / "kpi-sessions"
SESSIONS_CSV = DATA_DIR / "sessions.csv"

PAGES_URL    = "https://kita731.github.io/TOKEN-KPI/log.html"
LOCAL_URL    = "http://localhost:5000/log"

WRITE_TOOLS  = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


# ── 解析 session 日誌 ─────────────────────────────────────

def find_latest_session() -> Path | None:
    if not SESSION_DIR.exists():
        return None
    files = sorted(SESSION_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    # 取最近 6 小時內的
    cutoff = time.time() - 6 * 3600
    for f in files:
        if f.stat().st_mtime > cutoff:
            return f
    return files[0] if files else None


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


def compute_from_events(events: list[dict]) -> dict:
    stop_count   = sum(1 for e in events if e.get("type") == "stop")
    lines_gen    = sum(e.get("lines", 0) for e in events if e.get("type") == "tool" and e.get("tool") in WRITE_TOOLS)
    timestamps   = [e["ts"] for e in events if "ts" in e]
    duration_min = round((max(timestamps) - min(timestamps)) / 60, 1) if len(timestamps) >= 2 else 0

    cwd_event = next((e for e in events if e.get("type") == "cwd"), None)
    project   = Path(cwd_event["cwd"]).name if cwd_event else ""

    # 取所有寫入的唯一檔案（用於 git diff）
    written_files = list({e.get("file") for e in events if e.get("type") == "tool" and e.get("tool") in WRITE_TOOLS and e.get("file")})

    return {
        "ic":           max(stop_count, 1),
        "lines_gen":    lines_gen,
        "duration_min": duration_min,
        "project":      project,
        "written_files": written_files,
        "cwd":          cwd_event.get("cwd", "") if cwd_event else "",
    }


# ── Git diff 估算保留行數 ─────────────────────────────────

def estimate_lines_kept(cwd: str, written_files: list[str]) -> int | None:
    if not cwd or not written_files:
        return None
    try:
        result = subprocess.run(
            ["git", "diff", "--numstat", "HEAD"],
            capture_output=True, text=True, cwd=cwd, timeout=5
        )
        if result.returncode != 0:
            # 嘗試 diff with working tree
            result = subprocess.run(
                ["git", "diff", "--numstat"],
                capture_output=True, text=True, cwd=cwd, timeout=5
            )
        if result.returncode != 0:
            return None

        total_added = 0
        for line in result.stdout.strip().splitlines():
            parts = line.split("\t")
            if len(parts) >= 3:
                try:
                    total_added += int(parts[0])
                except ValueError:
                    pass
        return total_added if total_added > 0 else None
    except Exception:
        return None


# ── CSV 寫入 ──────────────────────────────────────────────

import csv
import uuid as _uuid

FIELDNAMES = [
    "date", "session_id", "project",
    "total_tasks", "passed_first_try", "tcr",
    "avg_iterations", "ic",
    "lines_generated", "lines_kept", "car",
    "ttwc_claude_min", "ttwc_manual_estimate_min", "ttwc_ratio",
    "notes",
]


def append_csv(row: dict):
    DATA_DIR.mkdir(exist_ok=True)
    write_header = not SESSIONS_CSV.exists() or SESSIONS_CSV.stat().st_size == 0
    with open(SESSIONS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


# ── 主程式 ────────────────────────────────────────────────

def sf(v, default=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def main():
    parser = argparse.ArgumentParser(description="TOKEN KPI — Session 結算")
    parser.add_argument("total",   nargs="?", type=int, help="總任務數")
    parser.add_argument("passed",  nargs="?", type=int, help="一次通過數")
    parser.add_argument("--open",  action="store_true", help="完成後開啟瀏覽器")
    parser.add_argument("--local", action="store_true", help="使用本地 Flask 伺服器")
    parser.add_argument("--session", type=str,  help="指定 session 檔案路徑")
    args = parser.parse_args()

    print("\n=== TOKEN KPI — 自動 Session 結算 ===\n")

    # 找 session 檔案
    if args.session:
        log_path = Path(args.session)
    else:
        log_path = find_latest_session()

    if not log_path or not log_path.exists():
        print("找不到近 6 小時內的 session 記錄。")
        print(f"請確認 Claude Code hooks 已設定，或檢查：{SESSION_DIR}")
        sys.exit(1)

    print(f"Session 檔案：{log_path.name}")
    events = load_events(log_path)
    if not events:
        print("Session 檔案為空，請確認 hooks 是否正確設定。")
        sys.exit(1)

    auto = compute_from_events(events)

    print(f"\n[ 自動偵測結果 ]")
    print(f"  專案         : {auto['project'] or '（未知）'}")
    print(f"  IC 來回次數  : {auto['ic']}")
    print(f"  產出行數     : {auto['lines_gen']}")
    print(f"  Session 時間 : {auto['duration_min']} 分鐘")

    # 嘗試 git diff 估算 CAR
    lines_kept = estimate_lines_kept(auto["cwd"], auto["written_files"])
    car = None
    if lines_kept is not None and auto["lines_gen"] > 0:
        car = round(lines_kept / auto["lines_gen"], 3)
        print(f"  保留行數（git diff 估算）: {lines_kept}")
        print(f"  CAR              : {car:.1%}")
    else:
        print(f"  CAR              : 無法從 git 估算，將手動輸入")

    # 手動輸入（最少化）
    print("\n[ 需要你提供的資訊（2~3 個數字）]")

    project = input(f"  專案名稱 [{auto['project'] or '輸入名稱'}]: ").strip() or auto["project"] or "未命名"

    if args.total is not None:
        total_tasks = args.total
        print(f"  總任務數: {total_tasks}")
    else:
        try:
            total_tasks = int(input("  總任務數（共做了幾個任務）: ").strip())
        except (ValueError, EOFError):
            total_tasks = 1

    if args.passed is not None:
        passed = args.passed
        print(f"  一次通過數: {passed}")
    else:
        try:
            passed = int(input(f"  一次通過數（不需修正直接成功）[最多 {total_tasks}]: ").strip())
        except (ValueError, EOFError):
            passed = total_tasks

    try:
        manual_min = sf(input(f"  手寫估計時間（分）[不知道按 Enter]: ").strip())
    except EOFError:
        manual_min = 0

    notes = input("  備註（選填，直接 Enter 略過）: ").strip()

    # CAR 手動補充
    if car is None:
        try:
            kept_input = input(f"  最終保留行數（估計值，Claude 產出 {auto['lines_gen']} 行）: ").strip()
            if kept_input:
                lines_kept = int(kept_input)
                car = round(lines_kept / auto["lines_gen"], 3) if auto["lines_gen"] > 0 else 0
            else:
                lines_kept = auto["lines_gen"]
                car = 1.0
        except (ValueError, EOFError):
            lines_kept = auto["lines_gen"]
            car = 1.0

    # 計算衍生指標
    tcr        = round(passed / total_tasks, 3) if total_tasks > 0 else 0
    ttwc_ratio = round(auto["duration_min"] / manual_min, 3) if manual_min > 0 else 0
    session_id = str(_uuid.uuid4())[:8]

    row = {
        "date":                     str(date.today()),
        "session_id":               session_id,
        "project":                  project,
        "total_tasks":              total_tasks,
        "passed_first_try":         passed,
        "tcr":                      tcr,
        "avg_iterations":           auto["ic"],
        "ic":                       auto["ic"],
        "lines_generated":          auto["lines_gen"],
        "lines_kept":               lines_kept or auto["lines_gen"],
        "car":                      car or 1.0,
        "ttwc_claude_min":          auto["duration_min"],
        "ttwc_manual_estimate_min": manual_min,
        "ttwc_ratio":               ttwc_ratio,
        "notes":                    notes,
    }

    # 寫入 CSV
    append_csv(row)

    print(f"""
╔══════════════════════════════════════╗
║       Session {session_id} 已記錄          ║
╚══════════════════════════════════════╝

  TCR  {tcr:.0%}   IC  {auto['ic']}   CAR  {car:.0%}   TTWC  {f"{ttwc_ratio:.0%}" if ttwc_ratio else "N/A"}
""")

    # 診斷提示
    if tcr < 0.70: print(f"  ⚠ TCR {tcr:.0%} < 70% — 任務描述可能不夠清楚")
    if auto["ic"] >= 5: print(f"  ⚠ IC {auto['ic']} ≥ 5 — prompt 設計問題")
    if car and car < 0.40: print(f"  ⚠ CAR {car:.0%} < 40% — 你在用 Claude 做錯的事")
    if ttwc_ratio and ttwc_ratio >= 1.0: print(f"  ⚠ TTWC {ttwc_ratio:.0%} — Claude 沒有加速你的工作")

    # 開啟瀏覽器
    base_url = LOCAL_URL if args.local else PAGES_URL
    params = {
        "project":      project,
        "ic":           auto["ic"],
        "lines_gen":    auto["lines_gen"],
        "lines_kept":   lines_kept or auto["lines_gen"],
        "ttwc_claude":  auto["duration_min"],
        "ttwc_manual":  manual_min or "",
        "total_tasks":  total_tasks,
        "passed":       passed,
        "notes":        notes,
        "auto":         "1",
        "session_id":   session_id,
    }
    url = base_url + "?" + urlencode({k: v for k, v in params.items() if v != ""})

    if args.open:
        print(f"  開啟瀏覽器：{url}\n")
        webbrowser.open(url)
    else:
        open_it = input("\n  開啟網頁確認？(Y/n): ").strip().lower()
        if open_it != "n":
            webbrowser.open(url)

    print("  資料已寫入 data/sessions.csv ✓\n")


if __name__ == "__main__":
    main()
