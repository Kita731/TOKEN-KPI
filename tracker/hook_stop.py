"""
Stop Hook — 每次 Claude 完成一次回應時觸發
快速記錄 stop 事件，然後在背景計算並儲存 KPI 到 sessions.csv
"""
import sys
import json
import time
import subprocess
from pathlib import Path


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)

    session_id = data.get("session_id", "unknown")
    log_dir    = Path.home() / ".claude" / "kpi-sessions"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file   = log_dir / f"{session_id}.jsonl"

    # 快速：只記錄 stop 事件
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.time(), "type": "stop"}) + "\n")
    except Exception:
        pass

    # 背景：計算並儲存到 sessions.csv（不阻塞 Claude Code）
    bg_script = Path(__file__).parent / "bg_save.py"
    try:
        kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        subprocess.Popen(["py", str(bg_script), session_id], **kwargs)
    except Exception:
        pass


if __name__ == "__main__":
    main()
