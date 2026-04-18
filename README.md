<div align="center">

# TOKEN KPI

**Claude Code 效率追蹤系統 · Claude Code Efficiency Tracker**

[![GitHub Pages](https://img.shields.io/badge/Live%20Dashboard-GitHub%20Pages-7c6af7?style=flat-square&logo=github)](https://kita731.github.io/TOKEN-KPI/)
[![Version](https://img.shields.io/badge/version-0.4.0-4ade80?style=flat-square)](CHANGELOG.md)

[🇹🇼 中文版](#-中文版) · [🇺🇸 English](#-english)

</div>

---

## 🇹🇼 中文版

### 這是什麼

TOKEN KPI 是一套 **全自動** 的 Claude Code 效率追蹤系統。  
透過 Claude Code Hooks，它在背景無聲記錄你每次工作的指標，不需要填表、不需要任何手動操作。

**🌐 即時看板**：[kita731.github.io/TOKEN-KPI](https://kita731.github.io/TOKEN-KPI/)

---

### 本地端設定需求

| 項目 | 狀態 |
|------|------|
| Python | 已安裝即可（系統自帶的 `py` 指令） |
| Claude Code Hooks | 執行 `py setup.py` 後自動設定 |
| 手動操作 | **不需要** |

**第一次使用只需要這兩步：**

```bash
git clone https://github.com/kita731/TOKEN-KPI.git <你想要的路徑>
py setup.py
# 完成。從此 Claude Code 的每個 session 都會自動記錄。
```

`setup.py` 會自動偵測 repo 所在位置，寫入 `~/.claude/settings.json`，clone 到任何路徑都不需要手動修改設定。

---

### 自動記錄的指標

每次 Claude Code 回應後，以下指標自動計算並儲存：

| 指標 | 自動？ | 說明 |
|------|--------|------|
| **IC** Iteration Count | ✅ 全自動 | 每次 Claude 回應 = 1 次迭代 |
| **Lines Generated** | ✅ 全自動 | 所有 Write/Edit 工具呼叫的行數總和 |
| **TTWC** Claude 時間 | ✅ 全自動 | Session 第一次工具呼叫到最後回應的時間 |
| **Project** | ✅ 全自動 | 工作目錄名稱 |
| **CAR** Code Acceptance Rate | ⚠️ 選填 | 在 Dashboard 點擊 `—` 補填，或用 `finalize.py` 透過 git diff 估算 |
| **TCR** Task Completion Rate | ⚠️ 選填 | 在 Dashboard 點擊 `?` → 輸入「總任務數 / 通過數」（5 秒） |
| **TTWC ratio** | ⚠️ 選填 | 需要手動估計「如果自己寫要多久」 |

---

### 運作原理

```
你使用 Claude Code
    │
    ├─ PostToolUse hook ──→ 記錄每次工具呼叫（Write/Edit 行數）
    │
    └─ Stop hook ─────────→ 記錄每次回應 → 背景計算 → 寫入 sessions.csv
                                                     → 自動 git push（5 分鐘 debounce）
                                                     → Dashboard 30 秒輪詢拉 GitHub raw
```

資料流：
- `data/sessions.csv` — 本機由 hook 寫入（每次 Claude 回應）
- `git push origin HEAD` — 冷卻期外自動觸發，訊息 `[auto] update kpi sessions`
- Dashboard → `raw.githubusercontent.com/.../sessions.csv` → 瀏覽器 localStorage（merge by session_id）

**停用自動 push**：把 `data/config.json` 的 `auto_push` 設為 `false`（預設 `true`）。

---

### 十個 KPI 指標

#### 核心指標（每 session）

| # | 指標 | 公式 | 目標 | 診斷 |
|---|------|------|------|------|
| 1 | **TCR** Task Completion Rate | 一次通過任務數 / 總任務數 | > 70% | 偏低 → 任務描述不清楚 |
| 2 | **IC** Iteration Count | 每個任務平均來回次數 | < 3 | ≥ 5 → prompt 設計問題 |
| 3 | **CAR** Code Acceptance Rate | 最終保留行數 / 產出行數 | > 60% | < 40% → 在用 Claude 做錯的事 |
| 4 | **TTWC** Time-to-Working-Code | Claude 時間 / 手寫估計時間 | < 50% | > 100% → Claude 沒有加速你 |

#### 品質指標（週結算，選填）

| # | 指標 | 說明 |
|---|------|------|
| 5 | **BIR** Bug Injection Rate | 事後發現 bug 數 / 1000 行 |
| 6 | **RR** Rework Rate | 一週後需重構的比例，> 30% = acceptance criteria 太鬆 |
| 7 | **CE** Context Efficiency | 有效產出 tokens / 總消耗 tokens |

#### PGE 流程指標（選填）

| # | 指標 | 說明 |
|---|------|------|
| 8 | **PA** Plan Accuracy | Planner 步驟被 Generator 採用的比例 |
| 9 | **ECR** Evaluator Catch Rate | Evaluator 抓到的問題 / 最終總問題數 |
| 10 | **HL** Handoff Loss | agent 交接時 context 遺失導致的重問次數 |

---

### 查看資料

#### 選項一：GitHub Pages（推薦，任何地方都能看）

1. 開啟 [kita731.github.io/TOKEN-KPI](https://kita731.github.io/TOKEN-KPI/)
2. 首次使用：點選右上角「匯入」→ 選擇 `data/sessions.csv`
3. 之後：資料存在 localStorage，重開瀏覽器都在

#### 進階結算（手動補充 TCR / CAR）

```bash
py tracker/finalize.py          # 互動模式，透過 git diff 估算 CAR
py tracker/finalize.py 5 4      # 快速模式：5 個任務，4 個通過
py tracker/finalize.py 5 4 --open  # 完成後直接開瀏覽器
```

---

### 檔案結構

```
TOKEN-KPI/
├── tracker/
│   ├── hook_tool.py      # PostToolUse hook（自動，記錄工具呼叫）
│   ├── hook_stop.py      # Stop hook（自動，觸發背景儲存）
│   ├── bg_save.py        # 背景計算工作者（自動，不阻塞 Claude Code）
│   └── finalize.py       # 進階結算腳本（手動選用，補充 TCR/CAR）
│
├── docs/                 # GitHub Pages 靜態網頁
│   ├── index.html        # Dashboard（趨勢圖、Health Cards、Sessions 表格）
│   ├── log.html          # 手動記錄 / URL 參數自動填表
│   ├── weekly.html       # 週報
│   └── js/
│       ├── kpi.js        # 資料層（localStorage + CSV 匯出入）
│       └── i18n.js       # 繁中 / 英文切換
│
├── data/
│   ├── sessions.csv      # 自動儲存（hook 直接寫入）
│   ├── weekly.csv
│   └── pge.csv
│
├── kpi_core.py           # Python 計算層
├── log_session.py        # CLI 手動記錄
└── dashboard.py          # CLI 終端機看板
```

---

<br>

## 🇺🇸 English

### What is this

TOKEN KPI is a **fully automatic** efficiency tracking system for Claude Code.  
It uses Claude Code Hooks to silently record metrics in the background — no forms to fill, no manual steps required.

**🌐 Live Dashboard**: [kita731.github.io/TOKEN-KPI](https://kita731.github.io/TOKEN-KPI/)

---

### Local Setup Requirements

| Requirement | Status |
|-------------|--------|
| Python | Must be installed (uses the `py` command) |
| Claude Code Hooks | Configured automatically by `py setup.py` |
| Manual steps | **None** |

**First-time setup — two steps:**

```bash
git clone https://github.com/kita731/TOKEN-KPI.git <your-preferred-path>
py setup.py
# Done. Every Claude Code session is now tracked automatically.
```

`setup.py` detects the repo's location and writes the correct paths to `~/.claude/settings.json`. Clone anywhere — no manual config editing required.

---

### Auto-Detected Metrics

After each Claude Code response, the following metrics are computed and saved automatically:

| Metric | Auto? | How |
|--------|-------|-----|
| **IC** Iteration Count | ✅ Fully auto | Each Claude response = 1 iteration |
| **Lines Generated** | ✅ Fully auto | Sum of all Write/Edit tool call content |
| **TTWC** Claude Time | ✅ Fully auto | Time from first tool call to last response |
| **Project** | ✅ Fully auto | Working directory name |
| **CAR** Code Acceptance Rate | ⚠️ Optional | Click `—` in Dashboard, or use `finalize.py` (git diff estimate) |
| **TCR** Task Completion Rate | ⚠️ Optional | Click `?` in Dashboard → enter total/passed (5 seconds) |
| **TTWC ratio** | ⚠️ Optional | Needs manual estimate of "how long would this take by hand" |

---

### How It Works

```
You use Claude Code
    │
    ├─ PostToolUse hook ──→ records each tool call (Write/Edit line counts)
    │
    └─ Stop hook ─────────→ records each response → background compute → saves to sessions.csv
                                                           ↑
                                                   fully automatic, non-blocking
```

Data is stored in two places:
- `data/sessions.csv` — local Python version (auto-updated by hooks)
- Browser localStorage — GitHub Pages version (import CSV or use web form)

---

### Viewing Your Data

#### Option 1: GitHub Pages (recommended — accessible anywhere)

1. Open [kita731.github.io/TOKEN-KPI](https://kita731.github.io/TOKEN-KPI/)
2. First time: click **Import** (top-right) → select `data/sessions.csv`
3. After that: data lives in localStorage, persists across browser restarts

#### Advanced: Fill in TCR / CAR

```bash
py tracker/finalize.py          # interactive, estimates CAR via git diff
py tracker/finalize.py 5 4      # quick: 5 total tasks, 4 passed
py tracker/finalize.py 5 4 --open  # open browser when done
```

---

### All Ten KPI Metrics

#### Core Metrics (per session)

| # | Metric | Formula | Target | Diagnostic |
|---|--------|---------|--------|------------|
| 1 | **TCR** Task Completion Rate | Tasks passed first try / Total tasks | > 70% | Low → task descriptions are unclear |
| 2 | **IC** Iteration Count | Avg back-and-forth rounds per task | < 3 | ≥ 5 → prompt design issue, not Claude's fault |
| 3 | **CAR** Code Acceptance Rate | Lines kept / Lines generated | > 60% | < 40% → you're using Claude for the wrong things |
| 4 | **TTWC** Time-to-Working-Code | Claude time / Manual estimate | < 50% | > 100% → Claude isn't actually speeding you up |

#### Quality Metrics (weekly, optional)

| # | Metric | Description |
|---|--------|-------------|
| 5 | **BIR** Bug Injection Rate | Post-merge bugs per 1,000 lines of Claude code |
| 6 | **RR** Rework Rate | % of code needing refactor within a week; > 30% = acceptance criteria too loose |
| 7 | **CE** Context Efficiency | Productive output tokens / Total tokens consumed |

#### PGE Flow Metrics (optional)

| # | Metric | Description |
|---|--------|-------------|
| 8 | **PA** Plan Accuracy | % of Planner steps adopted by Generator |
| 9 | **ECR** Evaluator Catch Rate | Issues caught by Evaluator / Total final issues |
| 10 | **HL** Handoff Loss | Re-prompts caused by context loss at agent handoffs |

---

### File Structure

```
TOKEN-KPI/
├── tracker/
│   ├── hook_tool.py      # PostToolUse hook (auto — records tool calls)
│   ├── hook_stop.py      # Stop hook (auto — triggers background save)
│   ├── bg_save.py        # Background compute worker (auto — non-blocking)
│   └── finalize.py       # Advanced session finalizer (optional — fills TCR/CAR)
│
├── docs/                 # GitHub Pages static site
│   ├── index.html        # Dashboard (trends, health cards, session table)
│   ├── log.html          # Manual log / URL-param auto-fill
│   ├── weekly.html       # Weekly review
│   └── js/
│       ├── kpi.js        # Data layer (localStorage + CSV import/export)
│       └── i18n.js       # Traditional Chinese / English toggle
│
├── data/
│   ├── sessions.csv      # Auto-saved by hooks
│   ├── weekly.csv
│   └── pge.csv
│
├── kpi_core.py           # Shared Python calculation layer
├── log_session.py        # CLI manual logger
└── dashboard.py          # CLI terminal dashboard
```
