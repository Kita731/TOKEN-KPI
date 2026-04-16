"""共用資料層：CSV 讀寫、指標計算、健康狀態判斷"""

import csv
import uuid
from datetime import date, timedelta
from pathlib import Path
from statistics import mean

DATA_DIR = Path(__file__).parent / "data"
SESSIONS_CSV = DATA_DIR / "sessions.csv"
WEEKLY_CSV = DATA_DIR / "weekly.csv"
PGE_CSV = DATA_DIR / "pge.csv"

# 指標目標門檻
THRESHOLDS = {
    "tcr":  {"target": 0.70, "invert": False, "warn": 0.60, "unit": "%"},
    "ic":   {"target": 3.0,  "invert": True,  "warn": 4.0,  "unit": ""},
    "car":  {"target": 0.60, "invert": False, "warn": 0.40, "unit": "%"},
    "ttwc": {"target": 0.50, "invert": True,  "warn": 0.70, "unit": "%"},
}

SESSIONS_FIELDNAMES = [
    "date", "session_id", "project",
    "total_tasks", "passed_first_try", "tcr",
    "avg_iterations", "ic",
    "lines_generated", "lines_kept", "car",
    "ttwc_claude_min", "ttwc_manual_estimate_min", "ttwc_ratio",
    "notes",
]

WEEKLY_FIELDNAMES = [
    "week_start", "week_end", "total_sessions",
    "bugs_per_1000_lines", "bir",
    "rework_rate", "rr",
    "prompt_cache_hit_rate", "context_efficiency", "ce",
    "notes",
]

PGE_FIELDNAMES = [
    "date", "session_id",
    "plan_steps_total", "plan_steps_adopted", "pa",
    "issues_caught_by_evaluator", "total_final_issues", "ecr",
    "handoff_loss_count", "hl",
    "notes",
]


def safe_float(v, default=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def load_csv(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_csv(path: Path, fieldnames: list, row: dict):
    write_header = not path.exists() or path.stat().st_size == 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def calc_session_derived(data: dict) -> dict:
    """從原始欄位計算衍生指標，回傳完整 row"""
    total = int(data.get("total_tasks") or 1)
    passed = int(data.get("passed_first_try") or 0)
    lines_gen = int(data.get("lines_generated") or 0)
    lines_kept = int(data.get("lines_kept") or 0)
    ttwc_claude = safe_float(data.get("ttwc_claude_min"))
    ttwc_manual = safe_float(data.get("ttwc_manual_estimate_min"))
    avg_iter = safe_float(data.get("avg_iterations", 2.0))

    tcr = round(passed / total, 3) if total else 0.0
    car = round(lines_kept / lines_gen, 3) if lines_gen else 0.0
    ttwc_ratio = round(ttwc_claude / ttwc_manual, 3) if ttwc_manual else 0.0

    return {
        "date": data.get("date", str(date.today())),
        "session_id": data.get("session_id") or str(uuid.uuid4())[:8],
        "project": data.get("project", ""),
        "total_tasks": total,
        "passed_first_try": passed,
        "tcr": tcr,
        "avg_iterations": avg_iter,
        "ic": avg_iter,
        "lines_generated": lines_gen,
        "lines_kept": lines_kept,
        "car": car,
        "ttwc_claude_min": ttwc_claude,
        "ttwc_manual_estimate_min": ttwc_manual,
        "ttwc_ratio": ttwc_ratio,
        "notes": data.get("notes", ""),
    }


def calc_pge_derived(data: dict) -> dict:
    plan_total = int(data.get("plan_steps_total") or 0)
    plan_adopted = int(data.get("plan_steps_adopted") or 0)
    caught = int(data.get("issues_caught_by_evaluator") or 0)
    total_issues = int(data.get("total_final_issues") or 0)
    hl = int(data.get("handoff_loss_count") or 0)

    pa = round(plan_adopted / plan_total, 3) if plan_total else 0.0
    ecr = round(caught / total_issues, 3) if total_issues else 1.0

    return {
        "date": data.get("date", str(date.today())),
        "session_id": data.get("session_id", ""),
        "plan_steps_total": plan_total,
        "plan_steps_adopted": plan_adopted,
        "pa": pa,
        "issues_caught_by_evaluator": caught,
        "total_final_issues": total_issues,
        "ecr": ecr,
        "handoff_loss_count": hl,
        "hl": hl,
        "notes": data.get("pge_notes", ""),
    }


def get_sessions(n: int = None) -> list[dict]:
    rows = load_csv(SESSIONS_CSV)
    rows.sort(key=lambda r: r.get("date", ""))
    return rows[-n:] if n else rows


def get_pge_by_session(session_id: str) -> dict | None:
    rows = load_csv(PGE_CSV)
    for r in rows:
        if r.get("session_id") == session_id:
            return r
    return None


def get_health_status(n: int = 10) -> dict:
    sessions = get_sessions(n)
    if not sessions:
        return {"sessions_count": 0, "metrics": {}}

    tcr_vals = [safe_float(r["tcr"]) for r in sessions]
    ic_vals = [safe_float(r["ic"]) for r in sessions]
    car_vals = [safe_float(r["car"]) for r in sessions]
    ttwc_vals = [safe_float(r["ttwc_ratio"]) for r in sessions]

    def _status(val, key):
        t = THRESHOLDS[key]
        invert = t["invert"]
        if not invert:
            if val >= t["target"]:
                return "pass"
            elif val >= t["warn"]:
                return "warn"
            return "fail"
        else:
            if val <= t["target"]:
                return "pass"
            elif val <= t["warn"]:
                return "warn"
            return "fail"

    def _trend(vals):
        if len(vals) < 2:
            return "stable"
        delta = vals[-1] - vals[-2]
        if abs(delta) < 0.02:
            return "stable"
        return "up" if delta > 0 else "down"

    avg_tcr = mean(tcr_vals)
    avg_ic = mean(ic_vals)
    avg_car = mean(car_vals)
    avg_ttwc = mean(ttwc_vals)

    return {
        "sessions_count": len(sessions),
        "metrics": {
            "tcr":  {"value": round(avg_tcr, 3),  "target": 0.70, "status": _status(avg_tcr, "tcr"),   "trend": _trend(tcr_vals)},
            "ic":   {"value": round(avg_ic, 2),   "target": 3.0,  "status": _status(avg_ic, "ic"),    "trend": _trend(ic_vals)},
            "car":  {"value": round(avg_car, 3),  "target": 0.60, "status": _status(avg_car, "car"),   "trend": _trend(car_vals)},
            "ttwc": {"value": round(avg_ttwc, 3), "target": 0.50, "status": _status(avg_ttwc, "ttwc"), "trend": _trend(ttwc_vals)},
        },
    }


def get_week_range(offset_weeks: int = 0):
    today = date.today()
    monday = today - timedelta(days=today.weekday()) - timedelta(weeks=offset_weeks)
    sunday = monday + timedelta(days=6)
    return str(monday), str(sunday)


def get_week_sessions(week_start: str, week_end: str) -> list[dict]:
    return [r for r in load_csv(SESSIONS_CSV) if week_start <= r.get("date", "") <= week_end]


def get_week_summary(offset_weeks: int = 0) -> dict:
    week_start, week_end = get_week_range(offset_weeks)
    sessions = get_week_sessions(week_start, week_end)

    summary = {
        "week_start": week_start,
        "week_end": week_end,
        "total_sessions": len(sessions),
        "avg_tcr": None, "avg_ic": None, "avg_car": None, "avg_ttwc": None,
        "has_pge": False,
        "avg_pa": None, "avg_ecr": None, "avg_hl": None,
    }

    if sessions:
        summary["avg_tcr"] = round(mean(safe_float(r["tcr"]) for r in sessions), 3)
        summary["avg_ic"] = round(mean(safe_float(r["ic"]) for r in sessions), 2)
        summary["avg_car"] = round(mean(safe_float(r["car"]) for r in sessions), 3)
        summary["avg_ttwc"] = round(mean(safe_float(r["ttwc_ratio"]) for r in sessions), 3)

    pge_rows = [r for r in load_csv(PGE_CSV) if week_start <= r.get("date", "") <= week_end]
    if pge_rows:
        summary["has_pge"] = True
        summary["avg_pa"] = round(mean(safe_float(r["pa"]) for r in pge_rows), 3)
        summary["avg_ecr"] = round(mean(safe_float(r["ecr"]) for r in pge_rows), 3)
        summary["avg_hl"] = round(mean(safe_float(r["hl"]) for r in pge_rows), 2)

    return summary
