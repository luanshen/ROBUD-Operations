/* ROBUD Operations · 工具清单
   状态: live / beta / planned
   path: 相对于当前页面的目标路径
*/
window.NAV_ITEMS = [
  {
    id: 'product-helper',
    title: '选品助手',
    icon: '🎯',
    path: '../tools/product-helper/',
    status: 'live',
    desc: '品牌官网 + 亚马逊店铺 + 卖家精灵 三源新品聚合,只读前台',
    version: '0.1.0'
  },
  {
    id: 'asin-report',
    title: 'ASIN 评估',
    icon: '📊',
    path: '#',
    status: 'planned',
    desc: '输入 ASIN 列表输出市场/竞争/利润/合规 四维评分',
    version: '-'
  },
  {
    id: 'fba-profit',
    title: 'FBA 利润计算器',
    icon: '💰',
    path: '#',
    status: 'planned',
    desc: '采购 + FBA + 广告 + 退货 + 汇率,自动算毛利率/净利率/盈亏平衡',
    version: '-'
  },
  {
    id: 'vc-payments',
    title: 'VC 结算分析',
    icon: '📑',
    path: '#',
    status: 'planned',
    desc: 'Amazon VC Payments 费用分类、月度对比、关键发现(已有 skill 可迁移)',
    version: '-'
  },
  {
    id: 'store-dashboard',
    title: '多店运营仪表',
    icon: '🏪',
    path: '#',
    status: 'planned',
    desc: 'US/UK/DE/CA/JP 多店铺中控,广告花费/ACOS/库存/利润一屏看',
    version: '-'
  },
  {
    id: 'review-miner',
    title: '竞品评论挖掘',
    icon: '💬',
    path: '#',
    status: 'planned',
    desc: '从评论中提取差评痛点 → 转化为产品升级建议',
    version: '-'
  }
];

// 总进度数据(由 docs/TODO.md 同步)
window.PLATFORM_PROGRESS = {
  total: 37,
  done: 11,
  phases: {
    'A · 基础架子': { total: 16, done: 11 },
    'B · 接入卖家精灵': { total: 9, done: 0 },
    'C · 自动化 + 监控': { total: 6, done: 0 },
    'D · 拓展工具': { total: 6, done: 0 }
  }
};

// 硬编码备份(file:// 协议下 fetch 受 CORS 限制会失败,必须保留兜底)
window.PLATFORM_PROGRESS_FALLBACK = window.PLATFORM_PROGRESS;

// 异步加载并解析 docs/TODO.md,自动覆盖 PLATFORM_PROGRESS
// 解析规则: 匹配 `| **<阶段>** | <窗口> | <total> | <done> | <%> |` 这种行
window.loadProgressFromTodoMD = async function(){
  try{
    const url = (location.protocol === 'file:') ? null : '../docs/TODO.md';
    if(!url) return window.PLATFORM_PROGRESS_FALLBACK;
    const r = await fetch(url, { cache: 'no-store' });
    if(!r.ok) throw new Error('HTTP ' + r.status);
    const md = await r.text();
    const parsed = window.parseProgressFromMD(md);
    if(parsed){
      window.PLATFORM_PROGRESS = parsed;
      return parsed;
    }
    return window.PLATFORM_PROGRESS_FALLBACK;
  }catch(e){
    console.warn('[nav-config] 动态加载 TODO.md 失败,使用 FALLBACK:', e.message);
    return window.PLATFORM_PROGRESS_FALLBACK;
  }
};

window.parseProgressFromMD = function(mdText){
  // 匹配 `| **<阶段名>** | <窗口> | <total> | <done> | <%> |`
  const re = /\|\s*\*\*([^*]+)\*\*\s*\|\s*[^|]+\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*[^|]+\|/g;
  const phases = {};
  let total = 0, done = 0;
  let m;
  while((m = re.exec(mdText)) !== null){
    const name = m[1].trim();
    const t = parseInt(m[2], 10);
    const d = parseInt(m[3], 10);
    if(name && !isNaN(t) && !isNaN(d)){
      phases[name] = { total: t, done: d };
      total += t;
      done  += d;
    }
  }
  if(!Object.keys(phases).length) return null;
  return { total, done, phases };
};
