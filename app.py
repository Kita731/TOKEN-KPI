import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import date
import kpi_core as kpi

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET") or secrets.token_hex(32)


# ── 頁面路由 ──────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/log", methods=["GET", "POST"])
def log_session():
    if request.method == "POST":
        data = request.form.to_dict()
        row = kpi.calc_session_derived(data)
        kpi.append_csv(kpi.SESSIONS_CSV, kpi.SESSIONS_FIELDNAMES, row)

        if data.get("use_pge") == "on":
            pge_row = kpi.calc_pge_derived({**data, "session_id": row["session_id"], "date": row["date"]})
            kpi.append_csv(kpi.PGE_CSV, kpi.PGE_FIELDNAMES, pge_row)

        flash(f"Session {row['session_id']} 已記錄｜TCR {row['tcr']:.0%}  IC {row['ic']}  CAR {row['car']:.0%}  TTWC {row['ttwc_ratio']:.0%}", "success")
        return redirect(url_for("dashboard"))

    return render_template("log_session.html", today=str(date.today()))


@app.route("/weekly", methods=["GET", "POST"])
def weekly():
    if request.method == "POST":
        data = request.form.to_dict()
        week_start, week_end = kpi.get_week_range()
        sessions = kpi.get_week_sessions(week_start, week_end)
        row = {
            "week_start": week_start,
            "week_end": week_end,
            "total_sessions": len(sessions),
            "bugs_per_1000_lines": data.get("bir", ""),
            "bir": data.get("bir", ""),
            "rework_rate": data.get("rr", ""),
            "rr": data.get("rr", ""),
            "prompt_cache_hit_rate": "",
            "context_efficiency": data.get("ce", ""),
            "ce": data.get("ce", ""),
            "notes": data.get("notes", ""),
        }
        kpi.append_csv(kpi.WEEKLY_CSV, kpi.WEEKLY_FIELDNAMES, row)
        flash("週報已儲存", "success")
        return redirect(url_for("weekly"))

    weekly_data = list(reversed(kpi.load_csv(kpi.WEEKLY_CSV)))
    return render_template("weekly.html", weekly_data=weekly_data)


# ── API 路由 ──────────────────────────────────────────────

@app.route("/api/sessions")
def api_sessions():
    n = request.args.get("n", type=int)
    return jsonify(kpi.get_sessions(n))


@app.route("/api/sessions/recent")
def api_sessions_recent():
    n = request.args.get("n", 10, type=int)
    sessions = kpi.get_sessions(n)
    # 附加 PGE 資料
    result = []
    for s in sessions:
        row = dict(s)
        pge = kpi.get_pge_by_session(s.get("session_id", ""))
        row["pge"] = pge
        result.append(row)
    return jsonify(result)


@app.route("/api/trends")
def api_trends():
    n = request.args.get("n", 20, type=int)
    sessions = kpi.get_sessions(n)
    return jsonify({
        "labels": [r.get("date", "") for r in sessions],
        "datasets": {
            "tcr":        [kpi.safe_float(r["tcr"]) for r in sessions],
            "ic":         [kpi.safe_float(r["ic"]) for r in sessions],
            "car":        [kpi.safe_float(r["car"]) for r in sessions],
            "ttwc_ratio": [kpi.safe_float(r["ttwc_ratio"]) for r in sessions],
        },
        "projects": [r.get("project", "") for r in sessions],
    })


@app.route("/api/health")
def api_health():
    n = request.args.get("n", 10, type=int)
    return jsonify(kpi.get_health_status(n))


@app.route("/api/weekly")
def api_weekly():
    return jsonify(kpi.load_csv(kpi.WEEKLY_CSV))


@app.route("/api/pge")
def api_pge():
    session_id = request.args.get("session_id")
    if session_id:
        row = kpi.get_pge_by_session(session_id)
        return jsonify(row or {})
    return jsonify(kpi.load_csv(kpi.PGE_CSV))


@app.route("/api/week_summary")
def api_week_summary():
    offset = request.args.get("offset", 0, type=int)
    return jsonify(kpi.get_week_summary(offset))


@app.route("/api/config", methods=["GET", "POST"])
def api_config():
    if request.method == "POST":
        data = request.get_json(force=True) or {}
        cfg = kpi.load_config()
        if "retention_days" in data:
            cfg["retention_days"] = int(data["retention_days"])
        kpi.save_config(cfg)
        return jsonify({"ok": True, "config": cfg})
    return jsonify(kpi.load_config())


@app.route("/api/clear", methods=["POST"])
def api_clear():
    data = request.get_json(force=True) or {}
    before = data.get("before")  # ISO date string，空則清除全部

    if before:
        rows = kpi.load_csv(kpi.SESSIONS_CSV)
        kept = [r for r in rows if r.get("date", "") >= before]
        pge_rows = kpi.load_csv(kpi.PGE_CSV)
        kept_pge = [r for r in pge_rows if r.get("date", "") >= before]
    else:
        kept, kept_pge = [], []

    # 重寫 sessions.csv
    import csv as _csv
    with open(kpi.SESSIONS_CSV, "w", newline="", encoding="utf-8") as f:
        w = _csv.DictWriter(f, fieldnames=kpi.SESSIONS_FIELDNAMES)
        w.writeheader()
        w.writerows(kept)

    # 重寫 pge.csv（若有）
    if kpi.PGE_CSV.exists():
        with open(kpi.PGE_CSV, "w", newline="", encoding="utf-8") as f:
            w = _csv.DictWriter(f, fieldnames=kpi.PGE_FIELDNAMES)
            w.writeheader()
            w.writerows(kept_pge)

    return jsonify({"ok": True, "kept": len(kept)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
