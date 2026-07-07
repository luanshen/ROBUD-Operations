# ROBUD Operations

> 跨境电商运营工具平台 · v0.1.0

ROBUD 品牌的亚马逊运营助手集合,目前以**选品**为核心,逐步拓展到利润计算、ASIN 评估、多店中控等场景。

---

## 平台特点

- **单文件 HTML + 内联依赖** · 打开即用,无构建步骤
- **深色头部 + 白色画布 + 浅灰网格** · 统一视觉规范
- **可公开访问** · CloudStudio 静态部署,获得 https 分享链接
- **共享设计资源** · `portal/assets/` 下的 CSS / JS / 导航配置,所有工具复用
- **可扩展** · 新工具 30 分钟内上线

---

## 目录结构

```
ROBUD-Operations/
├── portal/                      平台门户
│   ├── index.html               工具中心首页
│   └── assets/
│       ├── shared.css           共享样式(主题/组件/响应式)
│       ├── shared.js            共享逻辑(Toast/Drawer/Modal/CSV)
│       └── nav-config.js        工具清单 + 进度数据
│
├── tools/                       运营工具集
│   └── product-helper/          选品助手(LIVE)
│       ├── index.html           前台(只读版)
│       └── data/
│           └── products.sample.json  示例数据
│
├── shared/                      跨工具复用
│   └── api/                     卖家精灵 / 浏览器抓取封装(Phase B)
│
├── docs/
│   └── TODO.md                  ⭐ 待执行清单(34 项)
│
└── README.md
```

---

## 当前已上线工具

| 工具 | 状态 | 入口 |
|------|------|------|
| 🎯 **选品助手** | LIVE | `tools/product-helper/index.html` |
| 📊 ASIN 评估 | planned | - |
| 💰 FBA 利润计算器 | planned | - |
| 📑 VC 结算分析 | planned | - |
| 🏪 多店运营仪表 | planned | - |
| 💬 竞品评论挖掘 | planned | - |

---

## 快速开始

### 本地预览
```bash
# 直接双击打开 portal/index.html
# 或在浏览器中拖入
```

### 公开部署

#### 方案 1:Netlify Drop(最快,1 分钟)
```
1. 访问 https://app.netlify.com/drop
2. 把整个 ROBUD-Operations/portal/ 文件夹拖进去
3. 获得 https://xxx.netlify.app 链接(立即生效)
4. 选品助手入口:https://xxx.netlify.app/tools/product-helper/
```

#### 方案 2:GitHub Pages
```
1. 把 ROBUD-Operations 推到 GitHub 仓库
2. Settings > Pages > Source 选 gh-pages 分支(或 main + /portal)
3. 获得 https://<用户名>.github.io/ROBUD-Operations/portal/
```

#### 方案 3:EdgeOne Pages(腾讯云)
```
1. 登录 https://edgeone.ai/pages
2. 新建项目 > 上传 portal/ 整个目录
3. 获得 https://xxx.edgeonepages.com
```

#### 方案 4:CloudStudio(原计划)
```bash
# 如已恢复服务,可用工具部署
workbuddy_cloudstudio_deploy --directory C:\Users\RT\WorkBuddy\ROBUD-Operations\portal
workbuddy_cloudstudio_deploy --directory C:\Users\RT\WorkBuddy\ROBUD-Operations\tools\product-helper
```

#### 方案 5:Python 本地服务(仅本机访问)
```bash
cd C:\Users\RT\WorkBuddy\ROBUD-Operations
python -m http.server 8080
# 浏览器打开 http://localhost:8080/portal/
# 选品助手:http://localhost:8080/tools/product-helper/
```

#### 备选部署说明

| 方案 | 速度 | 公开访问 | 适合场景 |
|------|------|---------|---------|
| Netlify Drop | ⚡ 1 分钟 | ✅ https | 临时分享、demo |
| GitHub Pages | 🕐 5 分钟 | ✅ https | 长期托管、版本管理 |
| EdgeOne Pages | 🕐 5 分钟 | ✅ https | 腾讯系生态 |
| CloudStudio | ⏸ 暂不可用 | - | 工具恢复后 |
| Python http | ⚡ 立即 | ❌ 仅本机 | 调试、离线使用 |

> 💡 **单次部署同时拿到两个 URL**:
> Netlify Drop 拖 `portal/` 整个文件夹(含 `../tools/` 相对路径),门户首页的"选品助手"卡片跳转即指向同源 `tools/product-helper/`,无需重复部署。

部署后获得 2 个 https 分享链接,可发给团队成员浏览。

### 真实数据接入
见 `docs/TODO.md` Phase B:
1. 确认 `mcp__sellersprite__*` MCP 工具可调用
2. 安装 playwright-scraper-skill
3. 写 Python 后端 `tools/product-helper/data/fetch.py`
4. 抓取后落 JSON,重新内嵌到 HTML,重新部署

---

## 设计规范

### 颜色
| 用途 | 颜色 |
|------|------|
| 头部背景 | `linear-gradient(135deg,#0f172a,#1e293b)` |
| 画布 | `#ffffff` / `#fafbfc` |
| 网格线 | `#f1f5f9` / `#e2e8f0` |
| 主色 | `#2563eb` (蓝) |
| 辅色 | `#7c3aed` (紫) |
| 状态 | good `#16a34a` / warn `#d97706` / bad `#dc2626` |

### 组件类(在 `shared.css` 中定义)
- `.app-header` · 顶部头部
- `.read-only-banner` · 只读模式横幅
- `.card` / `.stat-card` · 卡片
- `.badge.live|beta|planned` · 状态徽标
- `.btn` / `.btn-primary` / `.btn-ghost` · 按钮
- `.tab-bar` · Tab 导航
- `.data-table` · 数据表格
- `.card-grid` / `.product-card` · 卡片网格
- `.drawer` / `.drawer-mask` · 抽屉
- `.toast` · Toast 提示
- `.tool-grid` / `.tool-card` · 工具网格(门户用)
- `.progress` / `.progress-card` · 进度条

### 共享 JS 命名空间 `WorkBuddy.*`
```js
WorkBuddy.toast(msg, type)            // 轻量反馈
WorkBuddy.openDrawer({title,body,actions})  // 抽屉
WorkBuddy.modal({title,content,onConfirm})  // 模态框
WorkBuddy.exportCSV(headers, rows, filename) // CSV 导出
WorkBuddy.fetchJSON(url)              // JSON 加载
WorkBuddy.injectHeaderNav(activeId)   // 注入顶部菜单
WorkBuddy.renderToolGrid(sel)         // 渲染工具网格
WorkBuddy.fmtUSD(n) / fmtNum(n) / fmtDate(s) / relTime(s)
```

---

## 新增工具的标准流程

1. 在 `tools/<新工具名>/` 创建文件夹
2. 复制 `product-helper/index.html` 作为脚手架,删去业务代码
3. 引入 shared 资源:
   ```html
   <link rel="stylesheet" href="../../portal/assets/shared.css">
   <script src="../../portal/assets/nav-config.js"></script>
   <script src="../../portal/assets/shared.js"></script>
   ```
4. 在 `portal/assets/nav-config.js` 中追加新条目
5. 若需要数据,写 `<工具名>.py` + `data/` 目录
6. 部署到 CloudStudio

**新工具上线成本**: ≤ 30 分钟

---

## 路线图

- ✅ **v0.1.0** (2026-07-03) · 平台门户 + 选品助手只读前台
- 🔄 **v0.2.0** (2026-07-20) · 选品助手真实数据接入(卖家精灵 MCP)
- 🔄 **v0.3.0** (2026-07-31) · 自动化 + 监控(每天 09:00 拉取)
- 📋 **v0.4.0** (2026-08 起) · ASIN 评估 / 利润计算 / 评论挖掘
- 📋 **v1.0.0** · 多店运营仪表 + VC 结算分析

详见 `docs/TODO.md`。
