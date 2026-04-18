#!/usr/bin/env python3
"""互動式填寫 session KPI 資料（30 秒完成）"""

import csv
import uuid
from datetime import date
from pathlib import Path

from kpi_core import (
    SESSIONS_FIELDNAMES as FIELDNAMES_SESSION,
    PGE_FIELDNAMES as FIELDNAMES_PGE,
)

DATA_DIR = Path(__file__).parent / "data"
SESSIONS_CSV = DATA_DIR / "sessions.csv"
PGE_CSV = DATA_DIR / "pge.csv"


def ask(prompt, default=None, cast=float):
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"  {prompt}{suffix}: ").strip()
    if not raw and default is not None:
        return default
    try:
        return cast(raw)
    except ValueError:
        print(f"  ⚠ 輸入無效，使用預設值 {default}")
        return default


def main():
    print("\n=== TOKEN KPI — Session 記錄 ===")
    today = str(date.today())
    session_id = input(f"  session ID（空白自動產生）: ").strip() or str(uuid.uuid4())[:8]
    project = input("  專案名稱: ").strip() or "未命名"

    print("\n[ 核心指標 ]")
    total_tasks = ask("總任務數", 1, int)
    passed = ask("一次通過數", 0, int)
    tcr = round(passed / total_tasks, 3) if total_tasks else 0

    avg_iter = ask("平均來回次數 (IC)", 2.0)
    lines_gen = ask("Claude 產出行數", 100, int)
    lines_kept = ask("最終保留行數", 80, int)
    car = round(lines_kept / lines_gen, 3) if lines_gen else 0

    ttwc_claude = ask("Claude 完成時間（分鐘）", 10.0)
    ttwc_manual = ask("手寫估計時間（分鐘）", 30.0)
    ttwc_ratio = round(ttwc_claude / ttwc_manual, 3) if ttwc_manual else 0

    notes = input("  備註（空白略過）: ").strip()

    row_session = {
        "date": today, "session_id": session_id, "project": project,
        "total_tasks": total_tasks, "passed_first_try": passed, "tcr": tcr,
        "avg_iterations": avg_iter, "ic": avg_iter,
        "lines_generated": lines_gen, "lines_kept": lines_kept, "car": car,
        "ttwc_claude_min": ttwc_claude, "ttwc_manual_estimate_min": ttwc_manual, "ttwc_ratio": ttwc_ratio,
        "notes": notes,
    }

    # PGE 可選
    use_pge = input("\n  記錄 PGE 指標？(y/N): ").strip().lower() == "y"
    if use_pge:
        print("\n[ PGE 流程指標 ]")
        plan_total = ask("Planner 步驟總數", 5, int)
        plan_adopted = ask("Generator 採用步驟數", 5, int)
        pa = round(plan_adopted / plan_total, 3) if plan_total else 0

        caught = ask("Evaluator 抓到的問題數", 0, int)
        total_issues = ask("最終總問題數", 0, int)
        ecr = round(caught / total_issues, 3) if total_issues else 1.0

        hl = ask("Handoff Loss 次數", 0, int)
        pge_notes = input("  備註: ").strip()

        row_pge = {
            "date": today, "session_id": session_id,
            "plan_steps_total": plan_total, "plan_steps_adopted": plan_adopted, "pa": pa,
            "issues_caught_by_evaluator": caught, "total_final_issues": total_issues, "ecr": ecr,
            "handoff_loss_count": hl, "hl": hl,
            "notes": pge_notes,
        }
        _append_csv(PGE_CSV, FIELDNAMES_PGE, row_pge)

    _append_csv(SESSIONS_CSV, FIELDNAMES_SESSION, row_session)

    print(f"""
✓ 已記錄 session {session_id}
  TCR={tcr:.0%}  IC={avg_iter}  CAR={car:.0%}  TTWC={ttwc_ratio:.0%}
""")

    _print_warnings(tcr, avg_iter, car, ttwc_ratio)


def _append_csv(path: Path, fieldnames: list, row: dict):
    write_header = not path.exists() or path.stat().st_size == 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def _print_warnings(tcr, ic, car, ttwc_ratio):
    warnings = []
    if tcr < 0.70:
        warnings.append(f"⚠ TCR {tcr:.0%} < 70%：任務描述可能不夠清楚")
    if ic >= 5:
        warnings.append(f"⚠ IC {ic} ≥ 5：prompt 設計有問題，不是 Claude 問題")
    elif ic >= 3:
        warnings.append(f"⚠ IC {ic} ≥ 3：來回次數偏高，考慮拆分任務")
    if car < 0.40:
        warnings.append(f"⚠ CAR {car:.0%} < 40%：你在用 Claude 做錯的事")
    elif car < 0.60:
        warnings.append(f"⚠ CAR {car:.0%} < 60%：產出品質待提升")
    if ttwc_ratio >= 0.50:
        warnings.append(f"⚠ TTWC {ttwc_ratio:.0%} ≥ 50%：Claude 沒有加速你的工作")

    if warnings:
        print("診斷提示：")
        for w in warnings:
            print(f"  {w}")
    else:
        print("  所有指標達標！")


if __name__ == "__main__":
    main()
