/**
 * TOKEN KPI — 核心資料層（localStorage）
 * 所有計算邏輯、儲存、匯出入
 */
const KPI = {
  THRESHOLDS: {
    tcr:  { target: 0.70, warn: 0.60, invert: false },
    ic:   { target: 3.0,  warn: 4.0,  invert: true  },
    car:  { target: 0.60, warn: 0.40, invert: false },
    ttwc: { target: 0.50, warn: 0.70, invert: true  },
  },

  // ── Utils ──────────────────────────────────────────────

  sf(v, def = 0) {
    const n = parseFloat(v);
    return isNaN(n) ? def : n;
  },

  round(v, d = 3) {
    const f = Math.pow(10, d);
    return Math.round(v * f) / f;
  },

  avg(arr) {
    return arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  },

  uuid() {
    return Math.random().toString(36).slice(2, 10);
  },

  today() {
    return new Date().toISOString().slice(0, 10);
  },

  // ── Sessions ──────────────────────────────────────────

  getSessions() {
    return JSON.parse(localStorage.getItem('kpi_sessions') || '[]')
      .sort((a, b) => (a.date || '').localeCompare(b.date || ''));
  },

  addSession(raw) {
    const row = this.calcSession(raw);
    const all = this.getSessions();
    all.push(row);
    localStorage.setItem('kpi_sessions', JSON.stringify(all));
    return row;
  },

  deleteSession(sessionId) {
    const all = this.getSessions().filter(r => r.session_id !== sessionId);
    localStorage.setItem('kpi_sessions', JSON.stringify(all));
    // Also remove associated PGE
    const pge = this.getPGE().filter(r => r.session_id !== sessionId);
    localStorage.setItem('kpi_pge', JSON.stringify(pge));
  },

  calcSession(data) {
    const total  = parseInt(data.total_tasks) || 1;
    const passed = parseInt(data.passed_first_try) || 0;
    const gen    = parseInt(data.lines_generated) || 0;
    const kept   = parseInt(data.lines_kept) || 0;
    const claude = this.sf(data.ttwc_claude_min);
    const manual = this.sf(data.ttwc_manual_estimate_min) || 1;
    const ic     = this.sf(data.avg_iterations, 2);

    return {
      date:                      data.date || this.today(),
      session_id:                data.session_id || this.uuid(),
      project:                   data.project || '',
      total_tasks:               total,
      passed_first_try:          passed,
      tcr:                       this.round(passed / total),
      avg_iterations:            ic,
      ic,
      lines_generated:           gen,
      lines_kept:                kept,
      car:                       gen ? this.round(kept / gen) : 0,
      ttwc_claude_min:           claude,
      ttwc_manual_estimate_min:  manual,
      ttwc_ratio:                this.round(claude / manual),
      notes:                     data.notes || '',
    };
  },

  // ── Weekly ────────────────────────────────────────────

  getWeekly() {
    return JSON.parse(localStorage.getItem('kpi_weekly') || '[]');
  },

  addWeekly(row) {
    const all = this.getWeekly();
    all.push(row);
    localStorage.setItem('kpi_weekly', JSON.stringify(all));
  },

  // ── PGE ──────────────────────────────────────────────

  getPGE() {
    return JSON.parse(localStorage.getItem('kpi_pge') || '[]');
  },

  addPGE(data) {
    const pt = parseInt(data.plan_steps_total) || 0;
    const pa = parseInt(data.plan_steps_adopted) || 0;
    const ec = parseInt(data.issues_caught_by_evaluator) || 0;
    const et = parseInt(data.total_final_issues) || 0;
    const hl = parseInt(data.handoff_loss_count) || 0;

    const row = {
      date:                         data.date || this.today(),
      session_id:                   data.session_id || '',
      plan_steps_total:             pt,
      plan_steps_adopted:           pa,
      pa:                           pt ? this.round(pa / pt) : 0,
      issues_caught_by_evaluator:   ec,
      total_final_issues:           et,
      ecr:                          et ? this.round(ec / et) : 1,
      handoff_loss_count:           hl,
      hl,
      notes:                        data.pge_notes || '',
    };
    const all = this.getPGE();
    all.push(row);
    localStorage.setItem('kpi_pge', JSON.stringify(all));
    return row;
  },

  getPGEBySession(id) {
    return this.getPGE().find(r => r.session_id === id) || null;
  },

  // ── Health ────────────────────────────────────────────

  getStatus(val, key) {
    const t = this.THRESHOLDS[key];
    if (!t) return 'pass';
    if (!t.invert) {
      if (val >= t.target) return 'pass';
      if (val >= t.warn)   return 'warn';
      return 'fail';
    } else {
      if (val <= t.target) return 'pass';
      if (val <= t.warn)   return 'warn';
      return 'fail';
    }
  },

  getTrend(vals) {
    if (vals.length < 2) return 'stable';
    const delta = vals[vals.length - 1] - vals[vals.length - 2];
    if (Math.abs(delta) < 0.02) return 'stable';
    return delta > 0 ? 'up' : 'down';
  },

  getHealth(n = 10) {
    const sessions = this.getSessions().slice(-n);
    if (!sessions.length) return { sessions_count: 0, metrics: {} };

    const tcrV  = sessions.map(r => this.sf(r.tcr));
    const icV   = sessions.map(r => this.sf(r.ic));
    const carV  = sessions.map(r => this.sf(r.car));
    const ttwcV = sessions.map(r => this.sf(r.ttwc_ratio));

    const mk = (vals, key, target) => ({
      value:  this.round(this.avg(vals), key === 'ic' ? 2 : 3),
      target,
      status: this.getStatus(this.avg(vals), key),
      trend:  this.getTrend(vals),
    });

    return {
      sessions_count: sessions.length,
      metrics: {
        tcr:  mk(tcrV,  'tcr',  0.70),
        ic:   mk(icV,   'ic',   3.0 ),
        car:  mk(carV,  'car',  0.60),
        ttwc: mk(ttwcV, 'ttwc', 0.50),
      },
    };
  },

  getTrends(n = 20) {
    const sessions = this.getSessions().slice(-n);
    return {
      labels:   sessions.map(r => r.date),
      datasets: {
        tcr:        sessions.map(r => this.sf(r.tcr)),
        ic:         sessions.map(r => this.sf(r.ic)),
        car:        sessions.map(r => this.sf(r.car)),
        ttwc_ratio: sessions.map(r => this.sf(r.ttwc_ratio)),
      },
      projects: sessions.map(r => r.project || ''),
    };
  },

  getWeekRange(offsetWeeks = 0) {
    const today = new Date();
    const dow = today.getDay();
    const mon = new Date(today);
    mon.setDate(today.getDate() - (dow === 0 ? 6 : dow - 1) - offsetWeeks * 7);
    const sun = new Date(mon);
    sun.setDate(mon.getDate() + 6);
    const fmt = d => d.toISOString().slice(0, 10);
    return { start: fmt(mon), end: fmt(sun) };
  },

  getWeekSummary(offsetWeeks = 0) {
    const { start, end } = this.getWeekRange(offsetWeeks);
    const sessions = this.getSessions().filter(r => r.date >= start && r.date <= end);
    const pge      = this.getPGE().filter(r => r.date >= start && r.date <= end);

    const s = {
      week_start: start, week_end: end,
      total_sessions: sessions.length,
      avg_tcr: null, avg_ic: null, avg_car: null, avg_ttwc: null,
      has_pge: false, avg_pa: null, avg_ecr: null, avg_hl: null,
    };

    if (sessions.length) {
      s.avg_tcr  = this.round(this.avg(sessions.map(r => this.sf(r.tcr))));
      s.avg_ic   = this.round(this.avg(sessions.map(r => this.sf(r.ic))), 2);
      s.avg_car  = this.round(this.avg(sessions.map(r => this.sf(r.car))));
      s.avg_ttwc = this.round(this.avg(sessions.map(r => this.sf(r.ttwc_ratio))));
    }

    if (pge.length) {
      s.has_pge = true;
      s.avg_pa  = this.round(this.avg(pge.map(r => this.sf(r.pa))));
      s.avg_ecr = this.round(this.avg(pge.map(r => this.sf(r.ecr))));
      s.avg_hl  = this.round(this.avg(pge.map(r => this.sf(r.hl))), 2);
    }

    return s;
  },

  // ── CSV Export ────────────────────────────────────────

  exportCSV(type = 'sessions') {
    const configs = {
      sessions: {
        data: this.getSessions(),
        fields: ['date','session_id','project','total_tasks','passed_first_try','tcr','avg_iterations','ic','lines_generated','lines_kept','car','ttwc_claude_min','ttwc_manual_estimate_min','ttwc_ratio','notes'],
        name: 'sessions',
      },
      weekly: {
        data: this.getWeekly(),
        fields: ['week_start','week_end','total_sessions','bir','rr','ce','notes'],
        name: 'weekly',
      },
      pge: {
        data: this.getPGE(),
        fields: ['date','session_id','plan_steps_total','plan_steps_adopted','pa','issues_caught_by_evaluator','total_final_issues','ecr','handoff_loss_count','hl','notes'],
        name: 'pge',
      },
    };

    const cfg = configs[type];
    if (!cfg.data.length) { alert('尚無資料可匯出'); return; }

    const escape = v => {
      const s = String(v ?? '');
      return s.includes(',') || s.includes('"') || s.includes('\n') ? `"${s.replace(/"/g,'""')}"` : s;
    };

    const csv = [
      cfg.fields.join(','),
      ...cfg.data.map(r => cfg.fields.map(f => escape(r[f])).join(',')),
    ].join('\n');

    const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `token-kpi-${cfg.name}-${this.today()}.csv`;
    a.click();
  },

  // ── CSV Import ────────────────────────────────────────

  parseCSV(text) {
    const lines = text.replace(/^\uFEFF/, '').trim().split(/\r?\n/);
    if (lines.length < 2) return [];

    const parseRow = line => {
      const result = [];
      let i = 0;
      while (i <= line.length) {
        if (line[i] === '"') {
          let val = ''; i++;
          while (i < line.length) {
            if (line[i] === '"' && line[i+1] === '"') { val += '"'; i += 2; }
            else if (line[i] === '"') { i++; break; }
            else val += line[i++];
          }
          if (line[i] === ',') i++;
          result.push(val);
        } else {
          let val = '';
          while (i < line.length && line[i] !== ',') val += line[i++];
          if (line[i] === ',') i++;
          result.push(val);
        }
      }
      return result;
    };

    const headers = parseRow(lines[0]);
    return lines.slice(1).filter(l => l.trim()).map(line => {
      const vals = parseRow(line);
      const obj = {};
      headers.forEach((h, i) => { obj[h.trim()] = (vals[i] || '').trim(); });
      return obj;
    });
  },

  importCSV(file, type = 'sessions') {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = e => {
        try {
          const rows = this.parseCSV(e.target.result);
          const key = type === 'sessions' ? 'kpi_sessions' : type === 'weekly' ? 'kpi_weekly' : 'kpi_pge';
          // Merge: append without duplicating session_id / week_start
          const existing = JSON.parse(localStorage.getItem(key) || '[]');
          const idField = type === 'weekly' ? 'week_start' : 'session_id';
          const existingIds = new Set(existing.map(r => r[idField]));
          const newRows = rows.filter(r => !existingIds.has(r[idField]));
          localStorage.setItem(key, JSON.stringify([...existing, ...newRows]));
          resolve({ total: rows.length, added: newRows.length });
        } catch (err) { reject(err); }
      };
      reader.readAsText(file, 'utf-8');
    });
  },

  clearAll() {
    localStorage.removeItem('kpi_sessions');
    localStorage.removeItem('kpi_weekly');
    localStorage.removeItem('kpi_pge');
  },

  // ── Remote Sync (GitHub raw) ──────────────────────────

  async syncFromRemote(baseUrl = 'https://raw.githubusercontent.com/kita731/TOKEN-KPI/main/data') {
    const targets = [
      { file: 'sessions.csv', key: 'kpi_sessions', idField: 'session_id' },
      { file: 'weekly.csv',   key: 'kpi_weekly',   idField: 'week_start' },
      { file: 'pge.csv',      key: 'kpi_pge',      idField: 'session_id' },
    ];
    let totalAdded = 0;
    for (const { file, key, idField } of targets) {
      try {
        const res = await fetch(`${baseUrl}/${file}?_=${Date.now()}`);
        if (!res.ok) continue;
        const text = await res.text();
        const rows = this.parseCSV(text);
        const existing = JSON.parse(localStorage.getItem(key) || '[]');
        const existingIds = new Set(existing.map(r => r[idField]));
        const newRows = rows.filter(r => r[idField] && !existingIds.has(r[idField]));
        if (newRows.length) {
          localStorage.setItem(key, JSON.stringify([...existing, ...newRows]));
          totalAdded += newRows.length;
        }
      } catch (_) {}
    }
    return totalAdded;
  },

};
