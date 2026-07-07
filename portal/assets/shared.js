/* ==========================================================================
   ROBUD Operations · 共享 JS
   命名空间: WorkBuddy.*
   ========================================================================== */
(function(global){
  'use strict';

  // ====== Toast ======
  function ensureToastHost(){
    let h = document.getElementById('wb-toast-host');
    if (!h) {
      h = document.createElement('div');
      h.id = 'wb-toast-host';
      h.className = 'toast-host';
      document.body.appendChild(h);
    }
    return h;
  }
  function toast(msg, type){
    const host = ensureToastHost();
    const el = document.createElement('div');
    el.className = 'toast' + (type ? ' ' + type : '');
    el.textContent = msg;
    host.appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; el.style.transition = '.2s'; }, 2400);
    setTimeout(() => el.remove(), 2700);
  }

  // ====== Drawer ======
  let drawerEls = null;
  function ensureDrawer(){
    if (drawerEls) return drawerEls;
    const mask = document.createElement('div');
    mask.className = 'drawer-mask';
    const drawer = document.createElement('div');
    drawer.className = 'drawer';
    drawer.innerHTML = `
      <div class="drawer-head">
        <h3 id="wb-drawer-title"></h3>
        <button class="close" aria-label="close">×</button>
      </div>
      <div class="drawer-body" id="wb-drawer-body"></div>
      <div class="drawer-foot" id="wb-drawer-foot"></div>
    `;
    document.body.appendChild(mask);
    document.body.appendChild(drawer);
    const close = () => {
      mask.classList.remove('open');
      drawer.classList.remove('open');
    };
    mask.addEventListener('click', close);
    drawer.querySelector('.close').addEventListener('click', close);
    drawerEls = { mask, drawer, close };
    return drawerEls;
  }
  function openDrawer(opts){
    const { mask, drawer } = ensureDrawer();
    const titleEl = drawer.querySelector('#wb-drawer-title');
    const bodyEl  = drawer.querySelector('#wb-drawer-body');
    const footEl  = drawer.querySelector('#wb-drawer-foot');
    titleEl.textContent = opts.title || '';
    if (typeof opts.body === 'string') bodyEl.innerHTML = opts.body;
    else if (opts.body instanceof HTMLElement) { bodyEl.innerHTML = ''; bodyEl.appendChild(opts.body); }
    else bodyEl.textContent = String(opts.body || '');
    footEl.innerHTML = '';
    (opts.actions || []).forEach(a => {
      const b = document.createElement('button');
      b.className = 'btn' + (a.primary ? ' btn-primary' : '');
      b.textContent = a.label;
      b.addEventListener('click', () => { try { a.onClick && a.onClick(); } finally { if (a.dismiss !== false) { mask.classList.remove('open'); drawer.classList.remove('open'); } } });
      footEl.appendChild(b);
    });
    mask.classList.add('open');
    drawer.classList.add('open');
  }
  function closeDrawer(){
    if (!drawerEls) return;
    drawerEls.mask.classList.remove('open');
    drawerEls.drawer.classList.remove('open');
  }

  // ====== Modal ======
  function modal(opts){
    const mask = document.createElement('div');
    mask.className = 'drawer-mask';
    mask.style.opacity = '0';
    const box = document.createElement('div');
    box.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:white;border-radius:12px;padding:24px;max-width:480px;width:90vw;z-index:1001;box-shadow:0 8px 32px rgba(0,0,0,.2);';
    box.innerHTML = `
      <h3 style="margin:0 0 12px;font-size:18px;"></h3>
      <div style="color:#64748b;font-size:14px;line-height:1.6;margin-bottom:20px;"></div>
      <div style="display:flex;gap:8px;justify-content:flex-end;"></div>
    `;
    box.querySelector('h3').textContent = opts.title || '';
    box.querySelector('div').textContent = opts.content || '';
    const btns = box.querySelector('div:last-child');
    const cancel = document.createElement('button');
    cancel.className = 'btn'; cancel.textContent = opts.cancelText || '取消';
    cancel.onclick = () => { mask.style.opacity = '0'; setTimeout(() => { mask.remove(); box.remove(); }, 200); };
    const ok = document.createElement('button');
    ok.className = 'btn btn-primary'; ok.textContent = opts.okText || '确定';
    ok.onclick = () => { mask.style.opacity = '0'; setTimeout(() => { mask.remove(); box.remove(); opts.onConfirm && opts.onConfirm(); }, 200); };
    btns.appendChild(cancel);
    btns.appendChild(ok);
    document.body.appendChild(mask);
    document.body.appendChild(box);
    requestAnimationFrame(() => { mask.style.opacity = '1'; mask.style.transition = '.2s'; });
  }

  // ====== CSV Export ======
  function exportCSV(headers, rows, filename){
    const esc = v => {
      if (v == null) return '';
      const s = String(v);
      if (/[",\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
      return s;
    };
    const lines = [headers.map(esc).join(',')];
    rows.forEach(r => lines.push(r.map(esc).join(',')));
    const csv = '\uFEFF' + lines.join('\r\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename || 'export.csv';
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 100);
  }

  // ====== fetchJSON ======
  async function fetchJSON(url){
    try {
      const r = await fetch(url);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch (e) {
      console.warn('[WorkBuddy.fetchJSON] failed', url, e);
      return null;
    }
  }

  // ====== format helpers ======
  function fmtUSD(n){
    if (n == null) return '-';
    return '$' + Number(n).toFixed(2);
  }
  function fmtNum(n){
    if (n == null) return '-';
    return Number(n).toLocaleString('en-US');
  }
  function fmtDate(s){
    if (!s) return '-';
    const d = new Date(s);
    if (isNaN(d)) return s;
    return d.toISOString().slice(0,10);
  }
  function relTime(s){
    if (!s) return '-';
    const d = new Date(s);
    if (isNaN(d)) return s;
    const days = Math.floor((Date.now() - d.getTime()) / 86400000);
    if (days === 0) return '今天';
    if (days === 1) return '昨天';
    if (days < 30) return days + ' 天前';
    if (days < 365) return Math.floor(days/30) + ' 月前';
    return Math.floor(days/365) + ' 年前';
  }

  // ====== Nav 注入(顶部菜单 + 工具网格) ======
  function injectHeaderNav(activeId){
    const navHost = document.querySelector('[data-wb-nav]');
    if (!navHost || !global.NAV_ITEMS) return;
    navHost.innerHTML = '';
    global.NAV_ITEMS.forEach(item => {
      const a = document.createElement('a');
      a.href = item.path;
      a.textContent = item.icon + ' ' + item.title;
      if (item.id === activeId) a.classList.add('active');
      navHost.appendChild(a);
    });
  }
  function renderToolGrid(hostSel, activeId){
    const host = document.querySelector(hostSel);
    if (!host || !global.NAV_ITEMS) return;
    host.innerHTML = '';
    global.NAV_ITEMS.forEach(item => {
      const a = document.createElement('a');
      a.className = 'tool-card' + (item.status === 'live' && item.path && item.path !== '#' ? '' : ' disabled');
      a.href = item.status === 'live' ? item.path : '#';
      if (item.status !== 'live') a.onclick = e => { e.preventDefault(); toast('该工具尚未上线,见 docs/TODO.md', 'warn'); };
      a.innerHTML = `
        <div class="head">
          <div class="icon-circle">${item.icon || '🛠'}</div>
          <span class="badge ${item.status}">${item.status === 'live' ? '<span class="pulse"></span>LIVE' : item.status.toUpperCase()}</span>
        </div>
        <h3>${item.title}</h3>
        <div class="desc">${item.desc || '规划中'}</div>
        <div class="footer">
          <span class="text-xs text-muted">v0.1 · ROBUD Operations</span>
          <span class="text-xs text-bold" style="color:var(--accent)">${item.status === 'live' ? '进入 →' : '敬请期待'}</span>
        </div>
      `;
      host.appendChild(a);
    });
  }

  // ====== 暴露 ======
  global.WorkBuddy = {
    toast, openDrawer, closeDrawer, modal,
    exportCSV, fetchJSON,
    fmtUSD, fmtNum, fmtDate, relTime,
    injectHeaderNav, renderToolGrid
  };
})(window);
