## [0.5.7] - 2026-04-18
- README：重寫為精簡雙語版，版本 badge 更新到 0.5.6，新增 `auto_push` / `retention_days` 設定表、CLI 工具表
- README：移除過時的「首次使用點匯入」說明（Dashboard 現在自動從 GitHub 同步），運作原理圖改畫完整資料流

## [0.5.6] - 2026-04-18
- kpi_core：SESSIONS_FIELDNAMES / PGE_FIELDNAMES / WEEKLY_FIELDNAMES 成為唯一真相來源
- log_session / weekly_review / tracker/bg_save / tracker/finalize：移除重複定義，改 import
- weekly_review：核心指標 / PGE 平均改為「略過空值」，並顯示 n 值；全空時顯示 `—` 不再印 0

## [0.5.5] - 2026-04-18
- 棄用本地 Flask 伺服器：刪除 `app.py` / `requirements.txt` / `templates/`（GitHub Pages + Dashboard 已覆蓋所有功能；連帶撤銷 0.5.4 的 `app.py` secret_key 改動）
- README：移除選項二 Flask 說明與檔案結構中的 Flask 相關項目
- kpi.js：`syncFromRemote` 新增 `applyRetention`，從 `config.json` 讀取 `retention_days` 後修剪 localStorage 過期資料

## [0.5.4] - 2026-04-18
- docs/js/kpi.js：重寫 `parseCSV` 為狀態機，正確處理引號內換行（修 #8）
- app.py：`secret_key` 改用 `os.environ["FLASK_SECRET"]` 或 `secrets.token_hex(32)` 隨機值，不再硬編碼（修 #10）
- version_log.csv：補上 0.4.1 / 0.5.0 / 0.5.1 遺漏版本（修 #9）

## [0.5.3] - 2026-04-18
- bg_save.py：upsert 成功後自動 `git add + commit + push origin HEAD`，5 分鐘 debounce，訊息 `[auto] update kpi sessions`
- 修復資料流斷鏈：先前 hook 只寫本機 CSV，dashboard 讀 GitHub raw，永遠看不到新資料；本版本讓兩端自動同步
- bg_save.py：補上遺漏的 `import subprocess`（原 PR 漏帶，push_to_remote 會 NameError 被 try/except 吞掉）
- config.json 新增 `auto_push` 開關（預設 true），可停用自動推送
- .gitignore：排除 `data/.last_push`（debounce 時間戳）
- README：更新「運作原理」段落，標記資料流 hook → auto push → dashboard

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
