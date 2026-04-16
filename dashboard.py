#!/usr/bin/env python3
"""終端機儀表板：顯示近期 sessions 趨勢"""

import csv
import sys
from pathlib import Path
from statistics import mean

DATA_DIR = Path(__file__).parent / "data"
SESSIONS_CSV = DATA_DIR / "sessions.csv"
WEEKLY_CSV = DATA_DIR / "weekly.csv"


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def safe_float(v, default=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def bar(value: float, target: float, width=20, invert=False) -> str:
    """產生簡單 ASCII 進度條，invert=True 表示越低越好"""
    filled = min(int(value / 1.0 * width), width) if not invert else min(int((1 - value) * width), width)
    color_ok = value >= target if not invert else value <= target
    marker = "█" * filled + "░" * (width - filled)
    status = "✓" if color_ok else "✗"
    return f"[{marker}] {status}"


def trend(vals: list[float]) -> str:
    if len(vals) < 2:
        return "─"
    delta = vals[-1] - vals[-2]
    if abs(delta) < 0.01:
        return "─"
    return "↑" if delta > 0 else "↓"


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    sessions = load_csv(SESSIONS_CSV)
    recent = sessions[-n:]

    if not recent:
        print("尚無 session 資料，執行 python log_session.py 開始記錄")
        return

    tcr_vals = [safe_float(r["tcr"]) for r in recent]
    ic_vals = [safe_float(r["ic"]) for r in recent]
    car_vals = [safe_float(r["car"]) for r in recent]
    ttwc_vals = [safe_float(r["ttwc_ratio"]) for r in recent]

    avg_tcr = mean(tcr_vals)
    avg_ic = mean(ic_vals)
    avg_car = mean(car_vals)
    avg_ttwc = mean(ttwc_vals)

    print(f"""
╔══════════════════════════════════════════════════════════╗
║              TOKEN KPI Dashboard（近 {n:2d} sessions）       ║
╚══════════════════════════════════════════════════════════╝

指標              近期均值   目標    趨勢  進度
─────────────────────────────────────────────────────────
TCR  完成率       {avg_tcr:6.1%}   >70%    {trend(tcr_vals)}   {bar(avg_tcr, 0.70)}
IC   來回次數     {avg_ic:6.1f}   <3      {trend([-x for x in ic_vals])}   {bar(1 - avg_ic/10, 0.7, invert=False)}
CAR  採用率       {avg_car:6.1%}   >60%    {trend(car_vals)}   {bar(avg_car, 0.60)}
TTWC 時間比率     {avg_ttwc:6.1%}   <50%    {trend([-x for x in ttwc_vals])}   {bar(1 - avg_ttwc, 0.5, invert=False)}
""")

    # 最近 5 筆明細
    print("最近 5 筆 Sessions：")
    print(f"  {'日期':<12} {'專案':<16} {'TCR':>5} {'IC':>5} {'CAR':>5} {'TTWC':>6}")
    print(f"  {'─'*12} {'─'*16} {'─'*5} {'─'*5} {'─'*5} {'─'*6}")
    for r in recent[-5:]:
        print(
            f"  {r.get('date',''):<12} {r.get('project',''):<16} "
            f"{safe_float(r['tcr']):>5.0%} "
            f"{safe_float(r['ic']):>5.1f} "
            f"{safe_float(r['car']):>5.0%} "
            f"{safe_float(r['ttwc_ratio']):>6.0%}"
        )

    # 週報摘要
    weekly = load_csv(WEEKLY_CSV)
    if weekly:
        latest = weekly[-1]
        print(f"""
最新週報 ({latest.get('week_start')} ~ {latest.get('week_end')})：
  BIR 缺陷率 : {latest.get('bir') or '未填'}
  RR  重構率 : {latest.get('rr') or '未填'}
  CE  效率   : {latest.get('ce') or '未填'}
""")


if __name__ == "__main__":
    main()
