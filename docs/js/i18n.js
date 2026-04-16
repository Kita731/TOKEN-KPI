/**
 * TOKEN KPI — i18n 多語言系統
 * 自動偵測 navigator.language，支援手動切換，存入 localStorage
 */
const I18N = {
  lang: 'zh',

  translations: {
    zh: {
      // Nav
      'nav.dashboard':  'Dashboard',
      'nav.log':        '記錄',
      'nav.weekly':     '週報',
      'nav.import':     '匯入',
      'nav.export':     '匯出',
      'nav.lang':       'EN',

      // Status
      'status.pass':    '達標',
      'status.warn':    '注意',
      'status.fail':    '未達標',

      // Metrics
      'metric.tcr.label':  'TCR — Task Completion Rate',
      'metric.tcr.target': '目標 > 70%',
      'metric.ic.label':   'IC — Iteration Count',
      'metric.ic.target':  '目標 < 3',
      'metric.car.label':  'CAR — Code Acceptance Rate',
      'metric.car.target': '目標 > 60%',
      'metric.ttwc.label': 'TTWC — Time-to-Working-Code',
      'metric.ttwc.target':'目標 < 50%',

      // Dashboard
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

      // Log
      'log.title':         '記錄 Session',
      'log.basic':         '基本資訊',
      'log.project.label': '專案名稱',
      'log.project.ph':    '例：TOKEN-KPI',
      'log.date':          '日期',
      'log.core':          '核心指標',
      'log.total':         '總任務數',
      'log.passed':        '一次通過數',
      'log.ic':            '平均來回次數（IC）',
      'log.lines_gen':     'Claude 產出行數',
      'log.lines_kept':    '最終保留行數',
      'log.ttwc_claude':   'Claude 完成時間（分）',
      'log.ttwc_manual':   '手寫估計時間（分）',
      'log.notes.label':   '備註',
      'log.notes.ph':      '（選填）這次 session 的觀察…',
      'log.pge':           'PGE 流程指標（選填）',
      'log.pge.toggle':    '記錄 PGE',
      'log.plan_total':    'Planner 步驟總數',
      'log.plan_adopted':  'Generator 採用步驟數',
      'log.eval_caught':   'Evaluator 抓到的問題',
      'log.eval_total':    '最終總問題數',
      'log.hl':            'Handoff Loss 次數',
      'log.pge_notes':     'PGE 備註',
      'log.pge_notes.ph':  '（選填）',
      'log.save':          '儲存 Session',
      'log.cancel':        '取消',
      'log.p.tcr':         'TCR（目標 >70%）',
      'log.p.ic':          'IC 狀態（目標 <3）',
      'log.p.car':         'CAR（目標 >60%）',
      'log.p.ttwc':        'TTWC（目標 <50%）',
      'log.p.pa':          'PA — Plan Accuracy',
      'log.p.ecr':         'ECR — Catch Rate',

      // Weekly
      'weekly.title':      '週報',
      'weekly.summary':    '本週自動彙整',
      'weekly.loading':    '計算中…',
      'weekly.no_data':    '本週尚無 session 資料',
      'weekly.record':     '記錄品質指標',
      'weekly.bir':        'BIR — bugs / 1000 行',
      'weekly.bir.ph':     '例：2.5',
      'weekly.rr':         'RR — 重構比例',
      'weekly.rr.ph':      '0.0 ~ 1.0',
      'weekly.ce':         'CE — Context Efficiency',
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
      'mini.tcr.note':     '目標 >70%',
      'mini.ic.note':      '目標 <3',
      'mini.car.note':     '目標 >60%',
      'mini.ttwc.note':    '目標 <50%',
      'mini.pa.note':      'Plan Accuracy',
      'mini.ecr.note':     'Catch Rate',
      'mini.hl':           'HL / session',
    },

    en: {
      // Nav
      'nav.dashboard':  'Dashboard',
      'nav.log':        'Log',
      'nav.weekly':     'Weekly',
      'nav.import':     'Import',
      'nav.export':     'Export',
      'nav.lang':       '中',

      // Status
      'status.pass':    'On Track',
      'status.warn':    'Warning',
      'status.fail':    'Off Track',

      // Metrics
      'metric.tcr.label':  'TCR — Task Completion Rate',
      'metric.tcr.target': 'Target > 70%',
      'metric.ic.label':   'IC — Iteration Count',
      'metric.ic.target':  'Target < 3',
      'metric.car.label':  'CAR — Code Acceptance Rate',
      'metric.car.target': 'Target > 60%',
      'metric.ttwc.label': 'TTWC — Time-to-Working-Code',
      'metric.ttwc.target':'Target < 50%',

      // Dashboard
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

      // Log
      'log.title':         'Log Session',
      'log.basic':         'Basic Info',
      'log.project.label': 'Project Name',
      'log.project.ph':    'e.g. TOKEN-KPI',
      'log.date':          'Date',
      'log.core':          'Core Metrics',
      'log.total':         'Total Tasks',
      'log.passed':        'Passed First Try',
      'log.ic':            'Avg Iterations (IC)',
      'log.lines_gen':     'Lines Generated',
      'log.lines_kept':    'Lines Kept',
      'log.ttwc_claude':   'Claude Time (min)',
      'log.ttwc_manual':   'Manual Estimate (min)',
      'log.notes.label':   'Notes',
      'log.notes.ph':      '(Optional) Observations from this session…',
      'log.pge':           'PGE Flow Metrics (Optional)',
      'log.pge.toggle':    'Track PGE',
      'log.plan_total':    'Total Planner Steps',
      'log.plan_adopted':  'Steps Adopted by Generator',
      'log.eval_caught':   'Issues Caught by Evaluator',
      'log.eval_total':    'Total Final Issues',
      'log.hl':            'Handoff Loss Count',
      'log.pge_notes':     'PGE Notes',
      'log.pge_notes.ph':  '(Optional)',
      'log.save':          'Save Session',
      'log.cancel':        'Cancel',
      'log.p.tcr':         'TCR (Target >70%)',
      'log.p.ic':          'IC Status (Target <3)',
      'log.p.car':         'CAR (Target >60%)',
      'log.p.ttwc':        'TTWC (Target <50%)',
      'log.p.pa':          'PA — Plan Accuracy',
      'log.p.ecr':         'ECR — Catch Rate',

      // Weekly
      'weekly.title':      'Weekly Review',
      'weekly.summary':    'This Week Auto-Summary',
      'weekly.loading':    'Calculating…',
      'weekly.no_data':    'No session data this week',
      'weekly.record':     'Record Quality Metrics',
      'weekly.bir':        'BIR — bugs per 1000 lines',
      'weekly.bir.ph':     'e.g. 2.5',
      'weekly.rr':         'RR — Rework Rate',
      'weekly.rr.ph':      '0.0 ~ 1.0',
      'weekly.ce':         'CE — Context Efficiency',
      'weekly.ce.ph':      '0.0 ~ 1.0',
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
      'mini.tcr.note':     'Target >70%',
      'mini.ic.note':      'Target <3',
      'mini.car.note':     'Target >60%',
      'mini.ttwc.note':    'Target <50%',
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
      const key = el.dataset.i18n;
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
    // Re-render dynamic content if a page-level callback exists
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
      const sys = (navigator.language || navigator.userLanguage || 'zh');
      this.lang = sys.startsWith('zh') ? 'zh' : 'en';
    }
    this.applyAll();
  },
};
