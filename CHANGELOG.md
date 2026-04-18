## [0.5.4] - 2026-04-18
- docs/js/kpi.js：重寫 `parseCSV` 為狀態機，正確處理引號內換行（修 #8）
- app.py：`secret_key` 改用 `os.environ["FLASK_SECRET"]` 或 `secrets.token_hex(32)` 隨機值，不再硬編碼（修 #10）
- version_log.csv：補上 0.4.1 / 0.5.0 / 0.5.1 遺漏版本（修 #9）

## [0.5.2] - 2026-04-18
- index.html：加入 30 秒自動輪詢與倒數顯示（修正 ec8c211 誤改到已停用的 templates/dashboard.html）
- index.html：簡化同步流程 — 移除匯入 modal 與本機 CSV 路徑記憶，改為「GitHub 自動同步 + 右上角手動同步按鈕」
- index.html：空狀態 UI 重寫，改為引導「git push 後重新同步」或手動匯入
- kpi.js：移除未採用的 File System Access API（openLocalFile / syncFromLocalFile / IndexedDB handle）
- data/config.json：新增 retention_days 設定檔

## [0.5.1] - 2026-04-17
- setup.py：自動偵測 repo 路徑並寫入 ~/.claude/settings.json，clone 到任何路徑無需手動修改
- 保留使用者現有其他 hooks（merge 模式），路徑相同時不重複寫入
- README：setup 步驟改為 `git clone + py setup.py`，移除手動修改路徑的說明

## [0.5.0] - 2026-04-17
- i18n.js：新增 10 條 desc.* 指標詳細說明 + 11 條 help.* 欄位說明（中英各一份）
- index.html：Health Card 加 ⓘ tooltip，點擊顯示指標說明，語言切換即時更新
- log.html：所有核心指標與 PGE 欄位加上說明小字（.field-help）
- weekly.html：BIR / RR / CE 欄位加上說明小字，label 改為中文名稱

## [0.4.1] - 2026-04-17
- bg_save.py：Stop hook 改為背景自動計算並 upsert sessions.csv，不阻塞 Claude Code
- hook_stop.py：重構為輕量觸發器，立即返回後背景執行計算
- Dashboard：支援顯示自動記錄的 sessions（AUTO tag、空值處理、TCR 快速填入 popover）
- README：重寫中英文版，強調零設定、全自動流程

## [0.2.0] - 2026-04-17
- Flask 網頁儀表板：Dashboard / 記錄 Session / 週報 三個頁面
- kpi_core.py：共用資料層（CSV 讀寫、指標計算、健康狀態判斷）
- 即時 JS 指標預覽（填表時即時看 TCR/CAR/TTWC/PA/ECR）
- Chart.js 趨勢折線圖，支援切換 10/20/30 筆視窗
- 深色主題 UI（Bootstrap 5 + 自訂 CSS）

## [0.1.0] - 2026-04-17
- 初始版本：實作四維度十指標 KPI 系統
- log_session.py：互動式 session 記錄（核心 + PGE 指標）
- weekly_review.py：週報彙整，寫入 weekly.csv
- dashboard.py：終端機儀表板，含 ASCII 進度條與趨勢箭頭
- 範例資料：sessions.csv、weekly.csv、pge.csv
