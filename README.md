<div align="center">

# TOKEN KPI

**Claude Code 效率追蹤系統 · Claude Code Efficiency Tracker**

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-7c6af7?style=flat-square&logo=github)](https://kita731.github.io/TOKEN-KPI/)
[![Version](https://img.shields.io/badge/version-0.3.0-4ade80?style=flat-square)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

[🇹🇼 中文版](#-中文版) · [🇺🇸 English](#-english)

</div>

---

## 🇹🇼 中文版

### 簡介

TOKEN KPI 是一套專為 Claude Code 工作流設計的效率追蹤系統。  
每次 session 結束後花 **30 秒填表**，一週後就能看出 prompt 設計、任務拆分、使用方式哪裡出了問題。

**🌐 線上版**：[kita731.github.io/TOKEN-KPI](https://kita731.github.io/TOKEN-KPI/)  
資料存在瀏覽器 localStorage，不需後端、不需帳號。

---

### 四個維度，十個指標

#### 核心指標（每 session 追蹤）

| # | 指標 | 公式 | 目標 | 診斷意義 |
|---|------|------|------|----------|
| 1 | **TCR** Task Completion Rate | 一次通過任務數 / 總任務數 | > 70% | 低於門檻 → 任務描述不夠清楚 |
| 2 | **IC** Iteration Count | 每個任務平均來回次數 | < 3 | ≥ 5 次 → prompt 設計問題，不是 Claude 問題 |
| 3 | **CAR** Code Acceptance Rate | 最終保留行數 / 產出行數 | > 60% | < 40% → 你在用 Claude 做錯的事 |
| 4 | **TTWC** Time-to-Working-Code | Claude 完成時間 / 手寫估計時間 | < 50% | > 100% → Claude 沒有加速你的工作 |

#### 品質指標（週結算）

| # | 指標 | 說明 |
|---|------|------|
| 5 | **BIR** Bug Injection Rate | Claude code 事後發現 bug 數 / 1000 行 |
| 6 | **RR** Rework Rate | 一週後需重構的比例，> 30% 代表 acceptance criteria 太鬆 |
| 7 | **CE** Context Efficiency | 有效產出 tokens / 總消耗 tokens |

#### PGE 流程指標（Planner-Generator-Evaluator）

| # | 指標 | 說明 |
|---|------|------|
| 8 | **PA** Plan Accuracy | Planner 步驟被 Generator 實際採用的比例 |
| 9 | **ECR** Evaluator Catch Rate | Evaluator 抓到的問題 / 最終總問題數 |
| 10 | **HL** Handoff Loss | agent 交接時 context 遺失導致的重問次數 |

---

### 功能

| 功能 | 說明 |
|------|------|
| 📊 **Dashboard** | Health Cards（達標 / 注意 / 未達標） + Chart.js 趨勢圖 + Sessions 表格 |
| ✏️ **記錄 Session** | 互動式填表，即時預覽 TCR / IC / CAR / TTWC，PGE 開關 |
| 📅 **週報** | 本週自動彙整 + BIR / RR / CE 手動填寫 + 歷史列表 |
| 🌐 **多語言** | 自動偵測瀏覽器語言（繁中 / 英文），右上角可手動切換 |
| 📥 **匯入 CSV** | 可從 Python 版本（sessions.csv）直接匯入 |
| 📤 **匯出 CSV** | 一鍵備份所有資料 |

---

### 使用方式

#### 網頁版（推薦）

1. 開啟 [kita731.github.io/TOKEN-KPI](https://kita731.github.io/TOKEN-KPI/)
2. 每次 Claude Code session 結束後點 **記錄** → 填寫 30 秒
3. 每週一次點 **週報** → 記錄 BIR / RR / CE 品質指標
4. 在 **Dashboard** 觀察趨勢，找出瓶頸

#### 本地 Python 工具（可選）

```bash
# 安裝依賴
pip install flask

# 互動式 CLI 記錄
python log_session.py

# 終端機儀表板
python dashboard.py

# 週報 CLI
python weekly_review.py

# Flask 網頁版（本地）
python app.py
# → 開啟 http://localhost:5000
```

---

### 資料儲存

| 儲存方式 | 適用情境 |
|----------|----------|
| **瀏覽器 localStorage** | GitHub Pages 網頁版，不需任何後端 |
| **CSV 檔案** (`data/`) | 本地 Python 工具版，可直接用 Excel 開啟 |

兩者可互通：透過網頁版的「匯入 CSV」功能，將本地 CSV 搬入瀏覽器；透過「匯出」下載備份。

---

### 檔案結構

```
TOKEN-KPI/
├── docs/                       # GitHub Pages 靜態網頁
│   ├── index.html              # Dashboard
│   ├── log.html                # 記錄 Session
│   ├── weekly.html             # 週報
│   └── js/
│       ├── kpi.js              # 資料層（localStorage + 計算 + CSV 匯出入）
│       └── i18n.js             # 多語言翻譯
│
├── data/                       # 本地 Python 版資料
│   ├── sessions.csv
│   ├── weekly.csv
│   └── pge.csv
│
├── app.py                      # Flask 本地網頁版
├── kpi_core.py                 # Python 共用計算層
├── log_session.py              # CLI 記錄工具
├── weekly_review.py            # CLI 週報工具
├── dashboard.py                # CLI 終端機儀表板
└── requirements.txt
```

---

### 最小可用版本

只追 4 個核心指標：**TCR、IC、CAR、TTWC**  
剩下 6 個指標有空再填，沒空就略過。

---

<br>

## 🇺🇸 English

### Overview

TOKEN KPI is an efficiency tracking system designed for Claude Code workflows.  
Spend **30 seconds logging** after each session. After a week, you'll see exactly where your prompt design, task decomposition, or usage patterns are breaking down.

**🌐 Live Demo**: [kita731.github.io/TOKEN-KPI](https://kita731.github.io/TOKEN-KPI/)  
Data is stored in your browser's localStorage — no backend, no account needed.

---

### Four Dimensions, Ten Metrics

#### Core Metrics (track every session)

| # | Metric | Formula | Target | Diagnostic Meaning |
|---|--------|---------|--------|--------------------|
| 1 | **TCR** Task Completion Rate | Tasks passed first try / Total tasks | > 70% | Below target → task descriptions are unclear |
| 2 | **IC** Iteration Count | Avg back-and-forth rounds per task | < 3 | ≥ 5 → prompt design problem, not Claude's fault |
| 3 | **CAR** Code Acceptance Rate | Lines kept / Lines generated | > 60% | < 40% → you're using Claude for the wrong things |
| 4 | **TTWC** Time-to-Working-Code | Claude time / Manual estimate | < 50% | > 100% → Claude is not actually speeding you up |

#### Quality Metrics (weekly)

| # | Metric | Description |
|---|--------|-------------|
| 5 | **BIR** Bug Injection Rate | Bugs found post-merge per 1,000 lines of Claude code |
| 6 | **RR** Rework Rate | % of code needing refactor within a week; > 30% = acceptance criteria too loose |
| 7 | **CE** Context Efficiency | Productive output tokens / Total tokens consumed |

#### PGE Flow Metrics (Planner-Generator-Evaluator)

| # | Metric | Description |
|---|--------|-------------|
| 8 | **PA** Plan Accuracy | % of Planner steps actually adopted by Generator |
| 9 | **ECR** Evaluator Catch Rate | Issues caught by Evaluator / Total final issues |
| 10 | **HL** Handoff Loss | Re-prompts caused by context loss at agent handoffs |

---

### Features

| Feature | Description |
|---------|-------------|
| 📊 **Dashboard** | Health cards (On Track / Warning / Off Track) + Chart.js trend lines + session table |
| ✏️ **Log Session** | Interactive form with live metric preview, PGE toggle |
| 📅 **Weekly Review** | Auto-summary of the current week + manual BIR / RR / CE entry + history |
| 🌐 **Bilingual** | Auto-detects browser language (Traditional Chinese / English), toggle in top-right |
| 📥 **Import CSV** | Import existing `sessions.csv` from the Python version |
| 📤 **Export CSV** | One-click backup of all data |

---

### Usage

#### Web App (Recommended)

1. Open [kita731.github.io/TOKEN-KPI](https://kita731.github.io/TOKEN-KPI/)
2. After each Claude Code session, click **Log** → fill in 30 seconds
3. Once a week, click **Weekly** → record quality metrics (BIR / RR / CE)
4. Check **Dashboard** to spot trends and bottlenecks

#### Local Python Tools (Optional)

```bash
# Install dependency
pip install flask

# Interactive CLI logger
python log_session.py

# Terminal dashboard
python dashboard.py

# Weekly review CLI
python weekly_review.py

# Local Flask web server
python app.py
# → open http://localhost:5000
```

---

### Data Storage

| Storage | Use Case |
|---------|----------|
| **Browser localStorage** | GitHub Pages web app — no backend required |
| **CSV files** (`data/`) | Local Python tools — compatible with Excel / Google Sheets |

Both are interoperable: use **Import CSV** in the web app to bring local data into the browser, and **Export** to download backups.

---

### File Structure

```
TOKEN-KPI/
├── docs/                       # GitHub Pages static site
│   ├── index.html              # Dashboard
│   ├── log.html                # Log Session
│   ├── weekly.html             # Weekly Review
│   └── js/
│       ├── kpi.js              # Data layer (localStorage + calculations + CSV I/O)
│       └── i18n.js             # Translations (zh / en)
│
├── data/                       # Local Python tool data
│   ├── sessions.csv
│   ├── weekly.csv
│   └── pge.csv
│
├── app.py                      # Local Flask web server
├── kpi_core.py                 # Shared Python calculation layer
├── log_session.py              # CLI logging tool
├── weekly_review.py            # CLI weekly review tool
├── dashboard.py                # CLI terminal dashboard
└── requirements.txt
```

---

### Minimum Viable Tracking

Track only the 4 core metrics: **TCR, IC, CAR, TTWC**  
The remaining 6 are optional — fill them in when you have time, skip them when you don't.
