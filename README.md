<div align="center">

# TOKEN KPI

**Claude Code 效率追蹤 · 零設定，看板即時**

[![GitHub Pages](https://img.shields.io/badge/Live%20Dashboard-GitHub%20Pages-7c6af7?style=flat-square&logo=github)](https://kita731.github.io/TOKEN-KPI/)
[![Version](https://img.shields.io/badge/version-0.5.6-4ade80?style=flat-square)](CHANGELOG.md)

[🇹🇼 中文](#-中文) · [🇺🇸 English](#-english)

</div>

---

## 🇹🇼 中文

### 這是什麼

每次用 Claude Code 工作後，hook 自動計算指標 → 寫入 `data/sessions.csv` → 自動 `git push` → 看板從 GitHub 直接讀取。不需要填表、不需要任何手動操作。

🌐 **看板**：<https://kita731.github.io/TOKEN-KPI/>

---

### 快速開始

```bash
git clone https://github.com/kita731/TOKEN-KPI.git
cd TOKEN-KPI
py setup.py
```

`setup.py` 會把路徑寫入 `~/.claude/settings.json` 註冊 hooks。完成。

---

### 運作原理

```
Claude Code 結束 session
       │
  Stop hook ──▶ tracker/bg_save.py（背景，不阻塞）
                       │
                       ├─ 寫入 data/sessions.csv（FileLock + 原子寫入）
                       └─ git add/commit/push（5 分鐘 debounce）
                                │
                                ▼
              kita731.github.io/TOKEN-KPI（30 秒輪詢 GitHub raw）
                                │
                                ▼
                    localStorage（merge by session_id）
```

`data/config.json` 兩個可調開關：

| 設定 | 預設 | 作用 |
|------|------|------|
| `auto_push` | `true` | 關掉後 hook 只寫本地不 push |
| `retention_days` | `30` | 看板只保留這幾天內的資料 |

---

### 指標

#### 自動偵測（什麼都不用做）

| 指標 | 怎麼算 |
|------|--------|
| **IC** 迭代次數 | Claude Stop 事件計數 |
| **Lines Generated** | Write/Edit 工具產出總行數 |
| **TTWC** Claude 時間 | 首個工具呼叫到最後回應的分鐘數 |
| **Project** | 工作目錄名稱 |

#### 需要你補（Dashboard 點一下，5 秒）

| 指標 | 怎麼補 |
|------|--------|
| **TCR** 任務完成率 | 表格裡點 `?` → 輸入「總任務 / 通過數」 |
| **CAR** 程式接受率 | 表格裡點 `—` → 填「保留行數」，或 `py tracker/finalize.py` 用 git diff 估算 |
| **TTWC ratio** | 估「如果自己寫要多久」，填進 log.html |

#### 十個 KPI 完整表

| # | 指標 | 目標 | 偏離時的診斷 |
|---|------|------|-------------|
| 1 | **TCR** Task Completion Rate | > 70% | 任務描述不夠清楚 |
| 2 | **IC** Iteration Count | < 3 | prompt 設計問題，不是 Claude 的鍋 |
| 3 | **CAR** Code Acceptance Rate | > 60% | 在用 Claude 做錯的事 |
| 4 | **TTWC** Time-to-Working-Code | < 50% | Claude 沒加速你 |
| 5 | **BIR** Bug Injection Rate | — | 每 1000 行事後 bug 數 |
| 6 | **RR** Rework Rate | < 30% | 一週內需重構的比例，過高代表驗收標準太鬆 |
| 7 | **CE** Context Efficiency | — | 有效產出 tokens / 總消耗 |
| 8 | **PA** Plan Accuracy | — | Planner 步驟被 Generator 採用比例 |
| 9 | **ECR** Evaluator Catch Rate | — | Evaluator 抓到的問題 / 最終問題總數 |
| 10 | **HL** Handoff Loss | — | agent 交接 context 遺失造成的重問次數 |

5–10 為選填，留給週報（`weekly_review.py`）與 PGE 流程使用。

---

### CLI 工具（選用）

| 指令 | 用途 |
|------|------|
| `py tracker/finalize.py [total] [passed]` | 單 session 結算，用 git diff 估 CAR |
| `py weekly_review.py` | 週報平均（空值不拉低平均） |
| `py log_session.py` | 互動式手動記錄 |
| `py dashboard.py` | 終端機 ASCII 看板 |

---

### 檔案結構

```
TOKEN-KPI/
├── tracker/
│   ├── hook_tool.py    # PostToolUse hook（記錄工具呼叫）
│   ├── hook_stop.py    # Stop hook（輕量觸發器）
│   ├── bg_save.py      # 背景寫入 + 自動 push
│   └── finalize.py     # 進階結算
├── docs/               # GitHub Pages 看板（index / log / weekly）
├── data/
│   ├── sessions.csv    # 自動記錄（主要資料）
│   ├── weekly.csv      # 週報
│   ├── pge.csv         # PGE 指標
│   └── config.json     # retention_days / auto_push
├── kpi_core.py         # FIELDNAMES / THRESHOLDS / 計算層
├── log_session.py      # CLI 手動填
├── weekly_review.py    # CLI 週報
└── dashboard.py        # CLI 看板
```

---

<br>

## 🇺🇸 English

### What is it

Every time you use Claude Code, a hook computes your efficiency metrics → writes to `data/sessions.csv` → auto `git push` → the dashboard reads straight from GitHub. No forms, no manual steps.

🌐 **Dashboard**: <https://kita731.github.io/TOKEN-KPI/>

---

### Quick Start

```bash
git clone https://github.com/kita731/TOKEN-KPI.git
cd TOKEN-KPI
py setup.py
```

`setup.py` writes paths into `~/.claude/settings.json` and registers the hooks. Done.

---

### How It Works

```
Claude Code session ends
       │
  Stop hook ──▶ tracker/bg_save.py (background, non-blocking)
                       │
                       ├─ writes data/sessions.csv (FileLock + atomic)
                       └─ git add/commit/push (5-minute debounce)
                                │
                                ▼
              kita731.github.io/TOKEN-KPI (30s polling GitHub raw)
                                │
                                ▼
                    localStorage (merged by session_id)
```

Two toggles in `data/config.json`:

| Setting | Default | Effect |
|---------|---------|--------|
| `auto_push` | `true` | Disable → hook only writes locally |
| `retention_days` | `30` | Dashboard keeps only the last N days |

---

### Metrics

#### Auto-detected (do nothing)

| Metric | How |
|--------|-----|
| **IC** Iteration Count | Claude Stop events |
| **Lines Generated** | Sum of Write/Edit tool output |
| **TTWC** Claude Time | Minutes from first tool call to last response |
| **Project** | Working directory name |

#### You fill in (one click in Dashboard, 5 seconds)

| Metric | How |
|--------|-----|
| **TCR** Task Completion Rate | Click `?` in the table → enter total/passed |
| **CAR** Code Acceptance Rate | Click `—` → enter lines kept, or `py tracker/finalize.py` (git diff estimate) |
| **TTWC ratio** | Estimate "how long would this take by hand" via log.html |

#### All Ten KPIs

| # | Metric | Target | Diagnostic |
|---|--------|--------|-----------|
| 1 | **TCR** Task Completion Rate | > 70% | Task descriptions unclear |
| 2 | **IC** Iteration Count | < 3 | Prompt design issue, not Claude's fault |
| 3 | **CAR** Code Acceptance Rate | > 60% | Using Claude for the wrong things |
| 4 | **TTWC** Time-to-Working-Code | < 50% | Claude isn't speeding you up |
| 5 | **BIR** Bug Injection Rate | — | Post-merge bugs per 1,000 lines |
| 6 | **RR** Rework Rate | < 30% | % needing refactor in a week; too high = loose acceptance |
| 7 | **CE** Context Efficiency | — | Productive tokens / total consumed |
| 8 | **PA** Plan Accuracy | — | % of Planner steps adopted by Generator |
| 9 | **ECR** Evaluator Catch Rate | — | Issues caught by Evaluator / total final issues |
| 10 | **HL** Handoff Loss | — | Re-prompts caused by context loss at handoffs |

5–10 are optional, used by `weekly_review.py` and the PGE flow.

---

### CLI Tools (optional)

| Command | Purpose |
|---------|---------|
| `py tracker/finalize.py [total] [passed]` | Per-session finalizer with git diff CAR estimate |
| `py weekly_review.py` | Weekly averages (skips empty values) |
| `py log_session.py` | Interactive manual logger |
| `py dashboard.py` | Terminal ASCII dashboard |

---

### File Structure

```
TOKEN-KPI/
├── tracker/
│   ├── hook_tool.py    # PostToolUse hook (records tool calls)
│   ├── hook_stop.py    # Stop hook (lightweight trigger)
│   ├── bg_save.py      # Background writer + auto push
│   └── finalize.py     # Advanced session finalizer
├── docs/               # GitHub Pages dashboard (index / log / weekly)
├── data/
│   ├── sessions.csv    # Auto-recorded (primary data)
│   ├── weekly.csv      # Weekly reports
│   ├── pge.csv         # PGE metrics
│   └── config.json     # retention_days / auto_push
├── kpi_core.py         # FIELDNAMES / THRESHOLDS / calc layer
├── log_session.py      # CLI manual logger
├── weekly_review.py    # CLI weekly report
└── dashboard.py        # CLI dashboard
```
