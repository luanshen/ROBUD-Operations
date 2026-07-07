# ROBUD Operations · 待执行 TODO 清单

> **平台**: ROBUD Operations v0.1.0
> **生成时间**: 2026-07-03
> **总任务**: 37 项 · 4 阶段
> **完成度**: 11/37 (30%)

## 激活 Phase B 的入口

> Phase B (接入卖家精灵) 的启动条件 = **用户填好 [WATCHLIST.md](./WATCHLIST.md)**。
> 你只要在对话中告诉我 3-5 个品牌 + 3-5 个亚马逊店铺 + 1-3 个卖家精灵筛选条件,我会:
> 1. 写入 `data/watchlist.json`
> 2. 把门户首页的 Watchlist 进度卡从 `0%` 推到 `100%`
> 3. 立刻开始 Phase B 的真实接口接入

---

## 进度总览

| 阶段 | 时间窗口 | 任务数 | 完成 | 进度 |
|------|---------|-------|-----|------|
| **A · 基础架子** | 2026-07-03 ~ 07-10 | 16 | 11 | ▰▰▰▰▰▰▰▱▱▱▱▱▱▱ 69% |
| **B · 接入卖家精灵** | 2026-07-11 ~ 07-20 | 9 | 0 | ▱▱▱▱▱▱▱▱▱ 0% |
| **C · 自动化 + 监控** | 2026-07-21 ~ 07-31 | 6 | 0 | ▱▱▱▱▱▱ 0% |
| **D · 拓展工具** | 2026-08 起 | 6 | 0 | ▱▱▱▱▱▱ 0% |

---

## Phase A · 基础架子(本周内 2026-07-03 ~ 07-10)

目标:建立可公开访问的 ROBUD Operations 平台门户 + 选品助手只读前台。

| # | 任务 | 状态 | 预估 | 负责人 | 依赖 |
|---|------|------|------|-------|------|
| A1 | 建立 `C:\Users\RT\WorkBuddy\ROBUD-Operations\` 目录骨架 | ✅ 完成 | 0.5h | ROBUD | - |
| A2 | 写 `portal/assets/shared.css` (设计规范 + 组件库) | ✅ 完成 | 1h | ROBUD | A1 |
| A3 | 写 `portal/assets/shared.js` (WorkBuddy.* 命名空间) | ✅ 完成 | 1.5h | ROBUD | A1 |
| A4 | 写 `portal/assets/nav-config.js` (6 个工具配置) | ✅ 完成 | 0.5h | ROBUD | - |
| A5 | 写 `portal/index.html` 门户首页 | ✅ 完成 | 1h | ROBUD | A2 A3 A4 |
| A6 | 迁移 product-helper HTML 到新位置 | ✅ 完成 | 0.5h | ROBUD | A1 |
| A7 | 改造 product-helper 接入 shared 资源 | ✅ 完成 | 1.5h | ROBUD | A6 A2 A3 |
| A8 | 在 product-helper 加只读模式横幅 | ✅ 完成 | 0.5h | ROBUD | A7 |
| A9 | 部署 portal/index.html 到 CloudStudio(获得分享链接) | ⏸ 暂停 | 0.5h | ROBUD | A5 |
| A10 | 部署 product-helper 到 CloudStudio(只读分享链接) | ⏸ 暂停 | 0.5h | ROBUD | A8 |
| A11 | 写 `docs/TODO.md` (本文件) | ✅ 完成 | 1h | ROBUD | - |
| A12 | 写 `ROBUD-Operations/README.md` (平台使用说明) | ⏳ 待开始 | 0.5h | ROBUD | A1 |
| A13 | 把 TODO 嵌入门户首页的进度条(动态读 TODO.md) | ⏳ 待开始 | 0.5h | ROBUD | A11 A5 |
| A14 | 写 `docs/WATCHLIST.md` (用户意向清单 · 品牌/店铺/筛选条件) | ✅ 完成 | 1h | ROBUD | - |
| A15 | 创建 `data/watchlist.json` (机器可读版意向清单) | ✅ 完成 | 0.5h | ROBUD | A14 |
| A16 | 把 WATCHLIST 嵌入门户首页(进度卡 + 跳转按钮) | ✅ 完成 | 0.5h | ROBUD | A14 A15 |

**Phase A 小计**: 16 项 · 11 完成 / 5 待办

---

## Phase B · 接入卖家精灵(7 月中 2026-07-11 ~ 07-20)

> ⚠️ **Phase B 已延期**。启动条件 = 用户填好 [WATCHLIST.md](./WATCHLIST.md) 中的品牌/店铺/筛选条件后,手动通知我启动。当前平台以静态只读模式运行,所有数据为 mock 示例。
> 
> 部署备选方案见 [README.md](../README.md) - "公开部署" 章节(Netlify Drop / GitHub Pages / EdgeOne Pages / Python http.server 4 种)。

目标:把三个数据源从 mock 替换为真实接口,产出第一份真实产品 JSON。

| # | 任务 | 状态 | 预估 | 负责人 | 依赖 |
|---|------|------|------|-------|------|
| B1 | 确认 SellerSprite MCP 在 WorkBuddy 中可调用(测试 `mcp__sellersprite__*` 工具) | ⏳ 待开始 | 0.5h | ROBUD | - |
| B2 | 安装 `playwright-scraper-skill`(隐身抓取) | ⏳ 待开始 | 0.5h | ROBUD | - |
| B3 | 写 `shared/api/sellersprite.py`(38 个 MCP 工具的 Python 封装) | ⏳ 待开始 | 3h | ROBUD | B1 |
| B4 | 写 `shared/api/playwright_fetch.py`(通用浏览器抓取) | ⏳ 待开始 | 2h | ROBUD | B2 |
| B5 | 写 `tools/product-helper/data/fetch.py`(三路并发:品牌/店铺/卖家精灵) | ⏳ 待开始 | 3h | ROBUD | B3 B4 |
| B6 | 测试数据抓取:US 玩具类目 "wooden" 近 30 天新品 | ⏳ 待开始 | 2h | ROBUD | B5 |
| B7 | 合并抓取结果为 `products_YYYYMMDD.json` | ⏳ 待开始 | 0.5h | ROBUD | B6 |
| B8 | 把 JSON 嵌入 product-helper/index.html(覆盖 sample) | ⏳ 待开始 | 0.5h | ROBUD | A7 B7 |
| B9 | 重新部署到 CloudStudio(更新分享链接) | ⏳ 待开始 | 0.5h | ROBUD | B8 |

**Phase B 小计**: 9 项 · 0 完成

---

## Phase C · 自动化 + 监控(7 月下 2026-07-21 ~ 07-31)

目标:每天 9:00 自动拉取数据,保留历史快照,推送简报。

| # | 任务 | 状态 | 预估 | 负责人 | 依赖 |
|---|------|------|------|-------|------|
| C1 | 建 `automation_update` 任务(每天 09:00 跑 fetch.py) | ⏳ 待开始 | 1h | ROBUD | B5 |
| C2 | 实现数据快照(保留 7/30/90 天) | ⏳ 待开始 | 1h | ROBUD | C1 |
| C3 | 增量检测(对比新旧 JSON,标 NEW 徽章) | ⏳ 待开始 | 1h | ROBUD | C2 |
| C4 | 推送简报到企业微信 / IMA(可选) | ⏳ 待开始 | 1h | ROBUD | C1 |
| C5 | 在门户首页显示"今日新增 N 个" | ⏳ 待开始 | 1h | ROBUD | C3 A5 |
| C6 | 错误监控(fetch 失败时邮件/TODO 提醒) | ⏳ 待开始 | 1h | ROBUD | C1 |

**Phase C 小计**: 6 项 · 0 完成

---

## Phase D · 拓展工具(8 月起)

目标:把平台从"选品"扩展到完整的运营套件。

| # | 任务 | 状态 | 预估 | 负责人 | 依赖 |
|---|------|------|------|-------|------|
| D1 | **ASIN 评估工具**:输入 ASIN 列表,输出市场/竞争/利润/合规四维评分 | ⏳ 待开始 | 8h | ROBUD | A2 A3 |
| D2 | **FBA 利润计算器**:采购 + FBA + 广告 + 退货 + 汇率,自动算毛利率 | ⏳ 待开始 | 6h | ROBUD | A2 A3 |
| D3 | **竞品评论挖掘**:从评论中提取差评痛点 → 产品升级建议 | ⏳ 待开始 | 6h | ROBUD | A2 A3 |
| D4 | **多店运营仪表**:US/UK/DE/CA/JP 多店铺中控 | ⏳ 待开始 | 10h | ROBUD | A2 A3 |
| D5 | **VC 结算分析**:迁移已有 `amazon-vc-payments-analysis` skill | ⏳ 待开始 | 4h | ROBUD | A2 A3 |
| D6 | **通用筛选/导出组件**:跨工具复用 | ⏳ 待开始 | 3h | ROBUD | A3 |

**Phase D 小计**: 6 项 · 0 完成

---

## 状态图例

- ✅ 完成
- 🔄 进行中
- ⏳ 待开始
- ❌ 阻塞
- ⏸ 暂停 (改用备选方案)
- ⏸ 延期 (启动条件未满足)

## 优先级矩阵

| 紧急\重要 | 重要 | 不重要 |
|----------|------|--------|
| **紧急** | A9 A10 B1 | A12 A13 |
| **不紧急** | B5 B6 C1 | D1-D6 |

## 备注

- **本清单**作为门户首页的"进度条"数据源(A13 实现后自动同步)
- **新任务**按以下模板追加到对应阶段:
  ```
  | # | 任务 | 状态 | 预估 | 负责人 | 依赖 |
  ```
- **阶段结束**时把 ✅ 状态归档到 `docs/TODO-archive.md`,本文件瘦身到只显示活跃任务
