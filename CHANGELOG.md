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
