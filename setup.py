#!/usr/bin/env python3
"""
TOKEN KPI — 一鍵安裝 Hook
自動偵測 repo 路徑，寫入 ~/.claude/settings.json，不需要手動編輯設定。

用法：
    py setup.py
"""
import json
import sys
from pathlib import Path

# Windows terminal encoding fix
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

REPO     = Path(__file__).parent.resolve()
SETTINGS = Path.home() / '.claude' / 'settings.json'


def make_kpi_hooks(repo_posix: str) -> dict:
    """回傳 TOKEN KPI 所需的 hooks 設定（使用絕對路徑）。"""
    return {
        "PostToolUse": [
            {
                "matcher": ".*",
                "hooks": [{"type": "command", "command": f'py "{repo_posix}/tracker/hook_tool.py"'}]
            }
        ],
        "Stop": [
            {
                "hooks": [{"type": "command", "command": f'py "{repo_posix}/tracker/hook_stop.py"'}]
            }
        ]
    }


def is_kpi_hook(entry: dict) -> bool:
    """判斷某個 hook entry 是否屬於 TOKEN KPI（含任何路徑）。"""
    return 'tracker/hook_' in json.dumps(entry)


def merge_hooks(existing: dict, repo_posix: str) -> dict:
    """
    將 TOKEN KPI hooks 合併進現有的 hooks 設定中。
    - 移除舊的 TOKEN KPI hook（來自不同路徑）
    - 加入新路徑的 hook
    - 保留使用者自己的其他 hooks
    """
    new_kpi = make_kpi_hooks(repo_posix)
    merged  = {}

    for event in set(list(existing.keys()) + list(new_kpi.keys())):
        old_entries = existing.get(event, [])
        kpi_entries = new_kpi.get(event, [])

        # 移除所有舊的 TOKEN KPI hook
        user_entries = [e for e in old_entries if not is_kpi_hook(e)]

        # 加上新路徑的 TOKEN KPI hook
        merged[event] = user_entries + kpi_entries

    return merged


def main():
    repo_posix = REPO.as_posix()

    # 讀取現有 settings（若不存在則建立）
    if SETTINGS.exists():
        with open(SETTINGS, encoding='utf-8') as f:
            settings = json.load(f)
    else:
        settings = {}
        SETTINGS.parent.mkdir(parents=True, exist_ok=True)

    # 已安裝且路徑相同 → 不重複寫入
    existing_hooks = settings.get('hooks', {})
    try:
        cur_cmd = existing_hooks['PostToolUse'][0]['hooks'][0]['command']
        if repo_posix in cur_cmd:
            print('✅ TOKEN KPI hooks 已安裝（路徑相同，不重複寫入）')
            print(f'   {repo_posix}')
            return
    except (KeyError, IndexError, TypeError):
        pass

    # 合併 hooks（保留使用者其他 hooks）
    settings['hooks'] = merge_hooks(existing_hooks, repo_posix)

    with open(SETTINGS, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

    print('✅ TOKEN KPI hooks 安裝完成！')
    print(f'   Repo    : {repo_posix}')
    print(f'   Settings: {SETTINGS}')
    print()
    print('重新啟動 Claude Code 後，每個 session 都會自動記錄。')


if __name__ == '__main__':
    main()
