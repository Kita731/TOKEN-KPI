#!/usr/bin/env python3
"""週報產生器：彙整本週 sessions.csv 並輸出摘要，同時追加到 weekly.csv"""

import csv
import sys
from datetime import date, timedelta
from pathlib import Path
from statistics import mean

from kpi_core import WEEKLY_FIELDNAMES

DATA_DIR = Path(__file__).parent / "data"
SESSIONS_CSV = DATA_DIR / "sessions.csv"
WEEKLY_CSV = DATA_DIR / "weekly.csv"
PGE_CSV = DATA_DIR / "pge.csv"


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


def collect(rows, key):
    """收集非空數值，略過空字串 / 非數字，避免拉低平均。"""
    vals = []
    for r in rows:
        raw = r.get(key, "")
        if raw == "" or raw is None:
            continue
        try:
            vals.append(float(raw))
        except (ValueError, TypeError):
            continue
    return vals


def fmt_pct(vals):
    return f"{mean(vals):.1%}" if vals else "—"


def fmt_num(vals, spec=".1f"):
    return format(mean(vals), spec) if vals else "—"


def main():
    offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    week_start, week_end = week_range(offset)

    sessions = load_csv(SESSIONS_CSV)
    week_sessions = filter_by_week(sessions, week_start, week_end)

    if not week_sessions:
        print(f"找不到 {week_start} ~ {week_end} 的 session 資料")
        return

    tcr_vals  = collect(week_sessions, "tcr")
    ic_vals   = collect(week_sessions, "ic")
    car_vals  = collect(week_sessions, "car")
    ttwc_vals = collect(week_sessions, "ttwc_ratio")

    print(f"""
╔══════════════════════════════════════════╗
║       TOKEN KPI 週報 {week_start} ~ {week_end}
╚══════════════════════════════════════════╝

Sessions: {len(week_sessions)}

[ 核心指標平均（僅計入非空值）]
  TCR  Task Completion Rate : {fmt_pct(tcr_vals)}  (n={len(tcr_vals)}, 目標 > 70%)
  IC   Iteration Count      : {fmt_num(ic_vals)}   (n={len(ic_vals)}, 目標 < 3)
  CAR  Code Acceptance Rate : {fmt_pct(car_vals)}  (n={len(car_vals)}, 目標 > 60%)
  TTWC Time-to-Working-Code : {fmt_pct(ttwc_vals)}  (n={len(ttwc_vals)}, 目標 < 50%)
""")

    # PGE
    pge_rows = load_csv(PGE_CSV)
    week_pge = filter_by_week(pge_rows, week_start, week_end)
    if week_pge:
        pa_vals  = collect(week_pge, "pa")
        ecr_vals = collect(week_pge, "ecr")
        hl_vals  = collect(week_pge, "hl")
        print(f"""[ PGE 流程指標平均 ]
  PA   Plan Accuracy        : {fmt_pct(pa_vals)}
  ECR  Evaluator Catch Rate : {fmt_pct(ecr_vals)}
  HL   Handoff Loss         : {fmt_num(hl_vals)} 次/session
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
