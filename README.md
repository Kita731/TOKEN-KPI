# TOKEN KPI — Claude Code 效率追蹤系統

每個 session 結束後花 30 秒填一行 CSV，一週 review 一次。

## 四個維度，十個指標

### 核心指標（每 session 追蹤）

| # | 指標 | 公式 | 目標 |
|---|------|------|------|
| 1 | **TCR** Task Completion Rate | 一次通過任務數 / 總任務數 | > 70% |
| 2 | **IC** Iteration Count | 每個任務平均來回次數 | < 3 |
| 3 | **CAR** Code Acceptance Rate | 最終保留行數 / Claude 產出行數 | > 60% |
| 4 | **TTWC** Time-to-Working-Code | 從 prompt 到 code 能跑的分鐘數（vs 手寫） | < 50% |

### 品質指標（週結算）

| # | 指標 | 說明 |
|---|------|------|
| 5 | **BIR** Bug Injection Rate | Claude code 事後發現 bug 數 / 1000 行 |
| 6 | **RR** Rework Rate | 一週後需重構的比例，> 30% 代表 acceptance criteria 太鬆 |
| 7 | **CE** Context Efficiency | 有效產出 tokens / 總消耗 tokens |

### PGE 流程指標（Planner-Generator-Evaluator）

| # | 指標 | 說明 |
|---|------|------|
| 8 | **PA** Plan Accuracy | Planner 步驟被 Generator 實際採用的比例 |
| 9 | **ECR** Evaluator Catch Rate | Evaluator 抓到的問題 / 最終總問題數 |
| 10 | **HL** Handoff Loss | agent 交接時 context 遺失導致重問次數 |

## 最小可用版本

只追 4 個核心指標：**TCR、IC、CAR、TTWC**

## 使用方式

1. 每個 session 結束後，執行 `python log_session.py` 填寫當次資料
2. 或直接編輯 `data/sessions.csv`
3. 一週後執行 `python weekly_review.py` 產出週報
4. 執行 `python dashboard.py` 在終端機檢視趨勢

## 檔案結構

```
TOKEN-KPI/
├── data/
│   ├── sessions.csv        # 每 session 一行（核心指標）
│   ├── weekly.csv          # 週結算（品質指標）
│   └── pge.csv             # PGE 流程指標
├── log_session.py          # 互動式填寫 session 資料
├── weekly_review.py        # 週報產生器
├── dashboard.py            # 終端機儀表板
├── CHANGELOG.md
└── version_log.csv
```
