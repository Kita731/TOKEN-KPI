/**
 * TOKEN KPI — i18n 多語言系統
 * 自動偵測 navigator.language，支援手動切換，存入 localStorage
 */
const I18N = {
  lang: 'zh',

  translations: {
    zh: {
      // ── Nav ───────────────────────────────────────────────
      'nav.dashboard':  'Dashboard',
      'nav.log':        '記錄',
      'nav.weekly':     '週報',
      'nav.import':     '匯入',
      'nav.export':     '匯出',
      'nav.lang':       'EN',

      // ── Status ────────────────────────────────────────────
      'status.pass':    '達標',
      'status.warn':    '注意',
      'status.fail':    '未達標',

      // ── Metric 標籤 ───────────────────────────────────────
      'metric.tcr.label':   'TCR — 一次通過率',
      'metric.tcr.target':  '目標 > 70%',
      'metric.ic.label':    'IC — 平均來回次數',
      'metric.ic.target':   '目標 < 3',
      'metric.car.label':   'CAR — 程式碼採用率',
      'metric.car.target':  '目標 > 60%',
      'metric.ttwc.label':  'TTWC — 時間效益比',
      'metric.ttwc.target': '目標 < 50%',

      // ── Metric 詳細說明（tooltip 用）─────────────────────
      'desc.tcr':
        'TCR（Task Completion Rate，一次通過率）\n' +
        '公式：一次通過任務數 ÷ 總任務數\n\n' +
        '衡量你的任務描述是否夠清楚。Claude 能在不需任何修正的情況下完成任務的比例。\n\n' +
        '診斷：\n' +
        '• < 70% → prompt 或 acceptance criteria 需要更具體\n' +
        '• 持續偏低 → 試著在 prompt 中加入「完成條件」',

      'desc.ic':
        'IC（Iteration Count，平均來回次數）\n' +
        '公式：各任務來回次數之平均\n\n' +
        '每個「你說 → Claude 回應」= 1 回合。來回越少代表 prompt 越精準。\n\n' +
        '診斷：\n' +
        '• ≥ 5 → 通常是 prompt 設計問題，不是 Claude 的限制\n' +
        '• 3~5 → 考慮把任務拆成更小的子任務\n' +
        '• < 3 → 良好',

      'desc.car':
        'CAR（Code Acceptance Rate，程式碼採用率）\n' +
        '公式：最終保留行數 ÷ Claude 產出行數\n\n' +
        '衡量 Claude 的產出是否切中你的需求。丟棄越多，代表方向偏差越大。\n\n' +
        '診斷：\n' +
        '• < 40% → 你在用 Claude 做不適合的事，或任務描述嚴重偏離需求\n' +
        '• 40~60% → 有改善空間，檢查任務邊界是否清楚\n' +
        '• > 60% → 良好',

      'desc.ttwc':
        'TTWC（Time-to-Working-Code ratio，時間效益比）\n' +
        '公式：Claude 完成時間 ÷ 你自己手寫的估計時間\n\n' +
        '衡量 Claude 是否真的加速了你的工作。\n\n' +
        '診斷：\n' +
        '• > 100% → Claude 沒有節省時間，考慮重新評估使用方式\n' +
        '• 50~100% → 有加速但效益有限\n' +
        '• < 50% → 良好，Claude 大幅提升效率',

      'desc.bir':
        'BIR（Bug Injection Rate，缺陷注入率）\n' +
        '公式：事後發現的 bug 數 ÷ Claude 產出行數 × 1000\n\n' +
        '每 1000 行 Claude 產出的程式碼中，事後（merge 後、上線後）發現的 bug 數量。\n' +
        '建議對比你自己手寫程式碼的缺陷率作為基準線。',

      'desc.rr':
        'RR（Rework Rate，重構率）\n' +
        '公式：一週後需重寫的程式碼比例\n\n' +
        '衡量 Claude 產出的程式碼品質是否能支撐實際需求。\n\n' +
        '診斷：\n' +
        '• > 30% → acceptance criteria 寫太鬆，或沒有說明架構與設計約束\n' +
        '• 建議：在 prompt 中明確描述「這段程式碼需要被維護多久」',

      'desc.ce':
        'CE（Context Efficiency，Context 效率）\n' +
        '公式：有效產出 token ÷ 總消耗 token\n\n' +
        '衡量你的 context 設計有多精省。包含 prompt caching 命中率的影響。\n\n' +
        'Token 是 Claude API 計費的基本單位，約 1 token ≈ 0.75 個英文單字。' +
        '有效產出 token 指直接對結果有貢獻的部分，而非反覆重複的背景說明。',

      'desc.pa':
        'PA（Plan Accuracy，計畫採用率）\n' +
        '公式：Generator 實際採用的步驟數 ÷ Planner 規劃的步驟總數\n\n' +
        '適用於 PGE（Planner-Generator-Evaluator）多 agent 架構。\n' +
        '衡量 Planner 的規劃有多少被 Generator 實際執行。\n\n' +
        '低比例代表 Planner 和 Generator 之間的 context 傳遞有問題，或規劃粒度不對。',

      'desc.ecr':
        'ECR（Evaluator Catch Rate，Evaluator 捕獲率）\n' +
        '公式：Evaluator 發現的問題數 ÷ 最終所有問題數\n\n' +
        '適用於 PGE 架構。衡量 Evaluator agent 在 review 階段的品質把關效力。\n\n' +
        '越高代表 Evaluator 越有效，問題在進入 production 前就被攔截。',

      'desc.hl':
        'HL（Handoff Loss，交接遺失）\n' +
        '單位：次數 / session\n\n' +
        '在多 agent 系統中，agent 交接時因 context 遺失而需要重新說明的次數。\n\n' +
        '診斷：\n' +
        '• 越高 → agent 間的 context 傳遞格式或摘要機制需要改善\n' +
        '• 建議：在每個 agent 的輸出末尾加上結構化的「接力摘要」',

      // ── Dashboard ─────────────────────────────────────────
      'dash.title':        'Dashboard',
      'dash.last':         '近',
      'dash.sessions':     '筆 sessions',
      'dash.trend':        '趨勢圖',
      'dash.recent':       '最近 Sessions',
      'dash.col.date':     '日期',
      'dash.col.project':  '專案',
      'dash.col.notes':    '備註',
      'dash.empty.text':   '尚無資料',
      'dash.empty.cta':    '記錄第一筆 Session →',
      'dash.import.title': '匯入 CSV 資料',
      'dash.import.type':  '資料類型',
      'dash.import.file':  '選擇 CSV 檔案',
      'dash.import.note':  '重複的 session_id 不會被匯入（merge 模式）',
      'dash.import.cancel':'取消',
      'dash.import.btn':   '匯入',
      'dash.opt.sessions': 'Sessions（核心指標）',
      'dash.opt.weekly':   'Weekly（週報）',
      'dash.opt.pge':      'PGE（流程指標）',

      // ── Log 表單標籤 ──────────────────────────────────────
      'log.title':         '記錄 Session',
      'log.basic':         '基本資訊',
      'log.project.label': '專案名稱',
      'log.project.ph':    '例：TOKEN-KPI',
      'log.date':          '日期',
      'log.core':          '核心指標',
      'log.total':         '總任務數',
      'log.passed':        '一次通過數',
      'log.ic':            'IC — 平均來回次數',
      'log.lines_gen':     '產出行數（自動偵測）',
      'log.lines_kept':    '保留行數',
      'log.ttwc_claude':   'Claude 完成時間（分）',
      'log.ttwc_manual':   '手寫估計時間（分）',
      'log.notes.label':   '備註',
      'log.notes.ph':      '（選填）這次 session 的觀察…',
      'log.pge':           'PGE 流程指標（選填）',
      'log.pge.toggle':    '記錄 PGE',
      'log.plan_total':    'Planner 步驟總數',
      'log.plan_adopted':  'Generator 採用步驟數',
      'log.eval_caught':   'Evaluator 發現的問題數',
      'log.eval_total':    '最終總問題數',
      'log.hl':            'HL — Handoff Loss 次數',
      'log.pge_notes':     'PGE 備註',
      'log.pge_notes.ph':  '（選填）',
      'log.save':          '儲存 Session',
      'log.cancel':        '取消',
      'log.p.tcr':         'TCR 預覽（目標 > 70%）',
      'log.p.ic':          'IC 狀態（目標 < 3）',
      'log.p.car':         'CAR 預覽（目標 > 60%）',
      'log.p.ttwc':        'TTWC 預覽（目標 < 50%）',
      'log.p.pa':          'PA — 計畫採用率',
      'log.p.ecr':         'ECR — Evaluator 捕獲率',

      // ── Log 表單說明文字（欄位下方小字）────────────────────
      'help.total':
        '一個「任務」＝ 一個完整的工作目標（例：「實作登入功能」），不是每條 prompt 都算。',
      'help.passed':
        '不需任何修正、追問或重新 prompt，Claude 直接一次完成的任務數量。',
      'help.ic':
        '所有任務的來回次數平均值。「一回合」= 你發一條 prompt + Claude 回應一次。',
      'help.lines_gen':
        '由 Claude Code hooks 自動記錄（Write / Edit 工具呼叫的行數總和）。若為手動填寫，請估計 Claude 在本 session 寫入的程式碼行數。',
      'help.lines_kept':
        '可用 git diff 估算：session 結束後執行 git diff HEAD，查看 +lines 加總。',
      'help.ttwc_claude':
        'hooks 自動記錄：從第一個工具呼叫到最後一次 Claude 回應的時間。',
      'help.ttwc_manual':
        '如果這些任務由你自己手動實作，估計需要幾分鐘。這是 TTWC 比率的分母，直接影響你對 Claude 效益的判斷。',
      'help.plan_total':
        'Planner agent 在規劃階段輸出的獨立步驟數量。',
      'help.plan_adopted':
        'Generator agent 實際執行的步驟數。若 Generator 跳過或合併了某些步驟，此數字會低於 plan_total。',
      'help.eval_caught':
        'Evaluator agent 在 review 階段主動發現、需要修正的問題數量。',
      'help.eval_total':
        '包含所有來源（Evaluator 發現 + 最終 user review 發現）的問題總數。',

      // ── Weekly 表單 ───────────────────────────────────────
      'weekly.title':      '週報',
      'weekly.summary':    '本週自動彙整',
      'weekly.loading':    '計算中…',
      'weekly.no_data':    '本週尚無 session 資料',
      'weekly.record':     '記錄品質指標',
      'weekly.bir':        'BIR — 缺陷注入率',
      'weekly.bir.ph':     '例：2.5（每 1000 行的 bug 數）',
      'weekly.rr':         'RR — 重構率',
      'weekly.rr.ph':      '0.0 ~ 1.0（30% 填 0.3）',
      'weekly.ce':         'CE — Context 效率',
      'weekly.ce.ph':      '0.0 ~ 1.0',
      'weekly.notes':      '本週備註',
      'weekly.notes.ph':   '（選填）本週觀察、調整方向…',
      'weekly.save':       '儲存週報',
      'weekly.history':    '歷史週報',
      'weekly.col.week':   '週次',
      'weekly.col.sess':   'Sessions',
      'weekly.col.bir':    'BIR',
      'weekly.col.rr':     'RR',
      'weekly.col.ce':     'CE',
      'weekly.col.notes':  '備註',
      'weekly.empty':      '尚無週報記錄',
      'weekly.saved':      '週報已儲存',
      'weekly.pge':        'PGE 流程指標',

      // ── Weekly 表單說明文字 ───────────────────────────────
      'help.bir':
        '事後（merge / 上線後）發現的 bug 數 ÷ Claude 產出行數 × 1000。建議每週統計一次，累積後與自己的基準線對比。',
      'help.rr':
        '一週後發現需要重新設計或大幅改寫的程式碼比例。持續 > 30% 代表你的 prompt 裡缺少架構與設計需求的說明。',
      'help.ce':
        '有效產出 token ÷ 總消耗 token。可從 Claude API 用量報表取得，或估算 prompt 中的「有效指令」佔比。',

      // ── Mini cards ────────────────────────────────────────
      'mini.tcr.note':     '目標 > 70%',
      'mini.ic.note':      '目標 < 3',
      'mini.car.note':     '目標 > 60%',
      'mini.ttwc.note':    '目標 < 50%',
      'mini.pa.note':      'Plan Accuracy',
      'mini.ecr.note':     'Catch Rate',
      'mini.hl':           'HL / session',
    },

    en: {
      // ── Nav ───────────────────────────────────────────────
      'nav.dashboard':  'Dashboard',
      'nav.log':        'Log',
      'nav.weekly':     'Weekly',
      'nav.import':     'Import',
      'nav.export':     'Export',
      'nav.lang':       '中',

      // ── Status ────────────────────────────────────────────
      'status.pass':    'On Track',
      'status.warn':    'Warning',
      'status.fail':    'Off Track',

      // ── Metric labels ─────────────────────────────────────
      'metric.tcr.label':   'TCR — Task Completion Rate',
      'metric.tcr.target':  'Target > 70%',
      'metric.ic.label':    'IC — Iteration Count',
      'metric.ic.target':   'Target < 3',
      'metric.car.label':   'CAR — Code Acceptance Rate',
      'metric.car.target':  'Target > 60%',
      'metric.ttwc.label':  'TTWC — Time-to-Working-Code',
      'metric.ttwc.target': 'Target < 50%',

      // ── Metric descriptions ───────────────────────────────
      'desc.tcr':
        'TCR — Task Completion Rate\n' +
        'Formula: tasks passed first try ÷ total tasks\n\n' +
        'Measures whether your task descriptions are clear enough for Claude to succeed without corrections.\n\n' +
        'Diagnostics:\n' +
        '• < 70% → add explicit acceptance criteria to your prompts\n' +
        '• Consistently low → describe "definition of done" upfront',

      'desc.ic':
        'IC — Iteration Count\n' +
        'Formula: average rounds of back-and-forth per task\n\n' +
        'One "round" = you send a message + Claude responds. Fewer rounds = more precise prompts.\n\n' +
        'Diagnostics:\n' +
        '• ≥ 5 → prompt design problem, not a Claude limitation\n' +
        '• 3–5 → try splitting tasks into smaller sub-tasks\n' +
        '• < 3 → healthy',

      'desc.car':
        'CAR — Code Acceptance Rate\n' +
        'Formula: lines kept ÷ lines generated by Claude\n\n' +
        'Measures how well Claude\'s output matches your actual needs. High discard = high mismatch.\n\n' +
        'Diagnostics:\n' +
        '• < 40% → you\'re using Claude for the wrong tasks, or task descriptions are way off\n' +
        '• 40–60% → room for improvement; clarify task boundaries\n' +
        '• > 60% → healthy',

      'desc.ttwc':
        'TTWC — Time-to-Working-Code ratio\n' +
        'Formula: Claude\'s time ÷ your manual time estimate\n\n' +
        'Measures whether Claude is actually accelerating your work.\n\n' +
        'Diagnostics:\n' +
        '• > 100% → Claude isn\'t saving time; reconsider the use case\n' +
        '• 50–100% → some speedup but limited\n' +
        '• < 50% → Claude is significantly faster',

      'desc.bir':
        'BIR — Bug Injection Rate\n' +
        'Formula: post-merge bugs ÷ lines generated × 1000\n\n' +
        'Bugs discovered after merging per 1,000 lines of Claude-generated code. ' +
        'Compare against your own baseline code to assess relative quality.',

      'desc.rr':
        'RR — Rework Rate\n' +
        'Formula: code needing redesign within 1 week ÷ total code\n\n' +
        'Measures whether Claude\'s output has long-term structural soundness.\n\n' +
        'Diagnostics:\n' +
        '• > 30% → your prompts are missing architectural constraints and design requirements\n' +
        '• Fix: specify "this code will be maintained for X months" in your prompt',

      'desc.ce':
        'CE — Context Efficiency\n' +
        'Formula: productive output tokens ÷ total tokens consumed\n\n' +
        'Measures how efficiently you use your context window. Includes the effect of prompt cache hit rate.\n\n' +
        'Tokens are the billing unit of the Claude API (~0.75 words per token). ' +
        '"Productive" tokens directly contribute to the output; repeated background context is waste.',

      'desc.pa':
        'PA — Plan Accuracy\n' +
        'Formula: steps Generator adopted ÷ steps Planner specified\n\n' +
        'Applies to the PGE (Planner-Generator-Evaluator) multi-agent pattern. ' +
        'Measures how much of the Planner\'s output the Generator actually follows.\n\n' +
        'Low values indicate a disconnect between planning and execution, or wrong granularity in the plan.',

      'desc.ecr':
        'ECR — Evaluator Catch Rate\n' +
        'Formula: issues caught by Evaluator ÷ total issues found\n\n' +
        'Applies to the PGE pattern. Measures the effectiveness of your Evaluator agent as a quality gate.\n\n' +
        'High ECR means problems are caught before production; low ECR means the Evaluator is missing things.',

      'desc.hl':
        'HL — Handoff Loss\n' +
        'Unit: occurrences per session\n\n' +
        'In multi-agent systems, the number of times context was lost at agent handoffs, ' +
        'requiring the user or next agent to re-explain something.\n\n' +
        'Fix: include a structured "relay summary" at the end of each agent\'s output.',

      // ── Dashboard ─────────────────────────────────────────
      'dash.title':        'Dashboard',
      'dash.last':         'Last',
      'dash.sessions':     'sessions',
      'dash.trend':        'Trends',
      'dash.recent':       'Recent Sessions',
      'dash.col.date':     'Date',
      'dash.col.project':  'Project',
      'dash.col.notes':    'Notes',
      'dash.empty.text':   'No data yet',
      'dash.empty.cta':    'Log your first session →',
      'dash.import.title': 'Import CSV',
      'dash.import.type':  'Data type',
      'dash.import.file':  'Select CSV file',
      'dash.import.note':  'Duplicate session_ids will be skipped (merge mode)',
      'dash.import.cancel':'Cancel',
      'dash.import.btn':   'Import',
      'dash.opt.sessions': 'Sessions (core metrics)',
      'dash.opt.weekly':   'Weekly report',
      'dash.opt.pge':      'PGE (flow metrics)',

      // ── Log form labels ───────────────────────────────────
      'log.title':         'Log Session',
      'log.basic':         'Basic Info',
      'log.project.label': 'Project Name',
      'log.project.ph':    'e.g. TOKEN-KPI',
      'log.date':          'Date',
      'log.core':          'Core Metrics',
      'log.total':         'Total Tasks',
      'log.passed':        'Passed First Try',
      'log.ic':            'IC — Avg Iterations',
      'log.lines_gen':     'Lines Generated (auto)',
      'log.lines_kept':    'Lines Kept',
      'log.ttwc_claude':   'Claude Time (min)',
      'log.ttwc_manual':   'Manual Estimate (min)',
      'log.notes.label':   'Notes',
      'log.notes.ph':      '(Optional) Observations from this session…',
      'log.pge':           'PGE Flow Metrics (Optional)',
      'log.pge.toggle':    'Track PGE',
      'log.plan_total':    'Planner Steps Total',
      'log.plan_adopted':  'Steps Adopted by Generator',
      'log.eval_caught':   'Issues Caught by Evaluator',
      'log.eval_total':    'Total Final Issues',
      'log.hl':            'HL — Handoff Loss Count',
      'log.pge_notes':     'PGE Notes',
      'log.pge_notes.ph':  '(Optional)',
      'log.save':          'Save Session',
      'log.cancel':        'Cancel',
      'log.p.tcr':         'TCR Preview (target > 70%)',
      'log.p.ic':          'IC Status (target < 3)',
      'log.p.car':         'CAR Preview (target > 60%)',
      'log.p.ttwc':        'TTWC Preview (target < 50%)',
      'log.p.pa':          'PA — Plan Accuracy',
      'log.p.ecr':         'ECR — Evaluator Catch Rate',

      // ── Log form help text ────────────────────────────────
      'help.total':
        'One "task" = one complete goal (e.g. "implement login"). Not every individual prompt counts.',
      'help.passed':
        'Tasks completed without any corrections, follow-ups, or re-prompting.',
      'help.ic':
        'Average rounds across all tasks. One "round" = you send a message + Claude responds once.',
      'help.lines_gen':
        'Auto-tracked by Claude Code hooks (sum of Write/Edit content). If entering manually, estimate lines Claude wrote this session.',
      'help.lines_kept':
        'Estimate via git: after the session, run git diff HEAD and sum the + lines.',
      'help.ttwc_claude':
        'Auto-tracked by hooks: time from the first tool call to the last Claude response.',
      'help.ttwc_manual':
        'Your estimate of how long these tasks would take you to implement by hand. This is the denominator for the TTWC ratio.',
      'help.plan_total':
        'Number of discrete steps the Planner agent output in its planning phase.',
      'help.plan_adopted':
        'Steps the Generator actually executed. Lower than plan_total if steps were skipped or merged.',
      'help.eval_caught':
        'Issues the Evaluator agent proactively identified during its review phase.',
      'help.eval_total':
        'All issues from all sources: Evaluator-caught + any found during final user review.',

      // ── Weekly form ───────────────────────────────────────
      'weekly.title':      'Weekly Review',
      'weekly.summary':    'This Week Auto-Summary',
      'weekly.loading':    'Calculating…',
      'weekly.no_data':    'No session data this week',
      'weekly.record':     'Record Quality Metrics',
      'weekly.bir':        'BIR — Bug Injection Rate',
      'weekly.bir.ph':     'e.g. 2.5 (bugs per 1000 lines)',
      'weekly.rr':         'RR — Rework Rate',
      'weekly.rr.ph':      '0.0 – 1.0  (30% → enter 0.3)',
      'weekly.ce':         'CE — Context Efficiency',
      'weekly.ce.ph':      '0.0 – 1.0',
      'weekly.notes':      'Weekly Notes',
      'weekly.notes.ph':   '(Optional) Observations, adjustments…',
      'weekly.save':       'Save Weekly Report',
      'weekly.history':    'Weekly History',
      'weekly.col.week':   'Week',
      'weekly.col.sess':   'Sessions',
      'weekly.col.bir':    'BIR',
      'weekly.col.rr':     'RR',
      'weekly.col.ce':     'CE',
      'weekly.col.notes':  'Notes',
      'weekly.empty':      'No weekly records yet',
      'weekly.saved':      'Weekly report saved',
      'weekly.pge':        'PGE Flow Metrics',

      // ── Weekly form help text ─────────────────────────────
      'help.bir':
        'Post-merge/post-deploy bugs ÷ Claude lines × 1000. Tally weekly and compare against your personal baseline.',
      'help.rr':
        'Code that required significant redesign within a week. Above 30% means your prompts are missing architectural and design constraints.',
      'help.ce':
        'Productive output tokens ÷ total tokens. Available from the Claude API usage dashboard, or estimate the ratio of "active instructions" in your prompts.',

      // ── Mini cards ────────────────────────────────────────
      'mini.tcr.note':     'Target > 70%',
      'mini.ic.note':      'Target < 3',
      'mini.car.note':     'Target > 60%',
      'mini.ttwc.note':    'Target < 50%',
      'mini.pa.note':      'Plan Accuracy',
      'mini.ecr.note':     'Catch Rate',
      'mini.hl':           'HL / session',
    },
  },

  t(key) {
    return this.translations[this.lang]?.[key] ?? key;
  },

  applyAll() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key  = el.dataset.i18n;
      const attr = el.dataset.i18nAttr;
      if (attr) {
        el.setAttribute(attr, this.t(key));
      } else {
        el.textContent = this.t(key);
      }
    });
    document.documentElement.lang = this.lang === 'zh' ? 'zh-Hant' : 'en';
  },

  setLang(lang) {
    this.lang = lang;
    localStorage.setItem('kpi_lang', lang);
    this.applyAll();
    if (typeof onLangChange === 'function') onLangChange(lang);
  },

  toggleLang() {
    this.setLang(this.lang === 'zh' ? 'en' : 'zh');
  },

  init() {
    const saved = localStorage.getItem('kpi_lang');
    if (saved) {
      this.lang = saved;
    } else {
      const sys = navigator.language || navigator.userLanguage || 'zh';
      this.lang = sys.startsWith('zh') ? 'zh' : 'en';
    }
    this.applyAll();
  },
};
