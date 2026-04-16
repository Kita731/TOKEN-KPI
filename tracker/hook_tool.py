"""
PostToolUse Hook — 每次 Claude 呼叫工具時自動觸發
記錄：工具名稱、產出行數、檔案路徑、時間戳記
"""
import sys
import json
import time
import os
from pathlib import Path


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)

    session_id = data.get("session_id", "unknown")
    tool_name  = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}

    log_dir  = Path.home() / ".claude" / "kpi-sessions"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{session_id}.jsonl"

    event: dict = {"ts": time.time(), "type": "tool", "tool": tool_name}

    if tool_name == "Write":
        content = tool_input.get("content", "")
        event["file"]  = tool_input.get("file_path", "")
        event["lines"] = len(content.splitlines())

    elif tool_name == "Edit":
        new_str = tool_input.get("new_string", "")
        event["file"]  = tool_input.get("file_path", "")
        event["lines"] = len(new_str.splitlines())

    elif tool_name == "MultiEdit":
        edits = tool_input.get("edits") or []
        total = sum(len(e.get("new_string", "").splitlines()) for e in edits)
        event["file"]  = tool_input.get("file_path", "")
        event["lines"] = total

    # 記錄工作目錄（第一次寫入時）
    if not log_file.exists():
        cwd_event = {
            "ts":   time.time(),
            "type": "cwd",
            "cwd":  os.getcwd(),
        }
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(cwd_event, ensure_ascii=False) + "\n")
        except Exception:
            pass

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()
