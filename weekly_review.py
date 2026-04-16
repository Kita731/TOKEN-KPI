#!/usr/bin/env python3
"""週報產生器：彙整本週 sessions.csv 並輸出摘要，同時追加到 weekly.csv"""

import csv
import sys
from datetime import date, timedelta
from pathlib import Path
from statistics import mean

DATA_DIR = Path(__file__).parent / "data"
SESSIONS_CSV = DATA_DIR / "sessions.csv"
WEEKLY_CSV = DATA_DIR / "weekly.csv"
PGE_CSV = DATA_DIR / "pge.csv"

WEEKLY_FIELDNAMES = [
    "week_start", "week_end", "total_sessions",
    "bugs_per_1000_lines", "bir",
    "rework_rate", "rr",
    "prompt_cache_hit_rate", "context_efficiency", "ce",
    "notes",
]


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def week_range(offset_weeks=0):
    today = date.today()
    monday = today - timedelta(days=today.weekday()) - timedelta(weeks=offset_weeks)
    sunday = monday + timedelta(days=6)
    return str(monday), str(sunday)


def filter_by_week(rows, week_start, week_end):
    return [r for r in rows if week_start <= r.get("date", "") <= week_end]


def safe_float(v, default=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def main():
    offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    week_start, week_end = week_range(offset)

    sessions = load_csv(SESSIONS_CSV)
    week_sessions = filter_by_week(sessions, week_start, week_end)

    if not week_sessions:
        print(f"找不到 {week_start} ~ {week_end} 的 session 資料")
        return

    tcr_vals = [safe_float(r["tcr"]) for r in week_sessions]
    ic_vals = [safe_float(r["ic"]) for r in week_sessions]
    car_vals = [safe_float(r["car"]) for r in week_sessions]
    ttwc_vals = [safe_float(r["ttwc_ratio"]) for r in week_sessions]

    print(f"""
╔══════════════════════════════════════════╗
║       TOKEN KPI 週報 {week_start} ~ {week_end}
╚══════════════════════════════════════════╝

Sessions: {len(week_sessions)}

[ 核心指標平均 ]
  TCR  Task Completion Rate : {mean(tcr_vals):.1%}  (目標 > 70%)
  IC   Iteration Count      : {mean(ic_vals):.1f}   (目標 < 3)
  CAR  Code Acceptance Rate : {mean(car_vals):.1%}  (目標 > 60%)
  TTWC Time-to-Working-Code : {mean(ttwc_vals):.1%}  (目標 < 50%)
""")

    # PGE
    pge_rows = load_csv(PGE_CSV)
    week_pge = filter_by_week(pge_rows, week_start, week_end)
    if week_pge:
        pa_vals = [safe_float(r["pa"]) for r in week_pge]
        ecr_vals = [safe_float(r["ecr"]) for r in week_pge]
        hl_vals = [safe_float(r["hl"]) for r in week_pge]
        print(f"""[ PGE 流程指標平均 ]
  PA   Plan Accuracy        : {mean(pa_vals):.1%}
  ECR  Evaluator Catch Rate : {mean(ecr_vals):.1%}
  HL   Handoff Loss         : {mean(hl_vals):.1f} 次/session
""")

    # 品質指標（手動輸入）
    print("[ 品質指標（需手動輸入）]")
    bir = input("  BIR bugs/1000 行（不知道留空）: ").strip() or ""
    rr = input("  RR  重構比例 0.0~1.0（不知道留空）: ").strip() or ""
    ce = input("  CE  Context Efficiency 0.0~1.0（不知道留空）: ").strip() or ""
    notes = input("  本週備註: ").strip()

    # 寫入 weekly.csv
    row = {
        "week_start": week_start, "week_end": week_end,
        "total_sessions": len(week_sessions),
        "bugs_per_1000_lines": bir, "bir": bir,
        "rework_rate": rr, "rr": rr,
        "prompt_cache_hit_rate": "", "context_efficiency": ce, "ce": ce,
        "notes": notes,
    }
    write_header = not WEEKLY_CSV.exists() or WEEKLY_CSV.stat().st_size == 0
    with open(WEEKLY_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=WEEKLY_FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"\n✓ 週報已追加到 {WEEKLY_CSV}")


if __name__ == "__main__":
    main()
