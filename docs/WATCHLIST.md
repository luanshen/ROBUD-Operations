# ROBUD Operations · 选品助手意向清单 (Watchlist)

> **用途**: 用户告诉系统「我要监控哪些品牌 / 亚马逊店铺 / 卖家精灵筛选条件」的输入清单。
> **状态**: 🆕 待用户填写(暂用占位,方便看到格式)
> **生成时间**: 2026-07-03
> **关联**: [TODO.md](./TODO.md) · [portal/index.html](../portal/index.html) · [product-helper](../tools/product-helper/)

---

## 一、品牌官网 (Brand Sites)

> 抓取策略:Playwright 隐身抓 Shopify / 自建站的新品列表页与商品详情页。
> 抓取频率:每日 1 次(每日 09:00,见 Phase C 任务 C1)。

| # | 品牌名 | 官网 URL | 入口页 | 抓取规则 | 上次抓取 | 状态 |
|---|--------|----------|--------|----------|----------|------|
| B01 | _(待填)_ | https:// | /collections/new | 近 7 天 | - | ⏳ 待配置 |
| B02 | _(待填)_ | https:// | /collections/all?sort=newest | 近 7 天 | - | ⏳ 待配置 |
| B03 | _(待填)_ | https:// | /products.json | 近 30 天 | - | ⏳ 待配置 |
| B04 | _(待填)_ | https:// | / | 近 14 天 | - | ⏳ 待配置 |
| B05 | _(待填)_ | https:// | / | 近 14 天 | - | ⏳ 待配置 |

**示例占位** (MELIANDRO / Skip Hop / Lovevery / Fisher-Price / Bright Starts 等玩具类目品牌):
- B01: Skip Hop → https://skiphop.com/collections/new
- B02: Lovevery → https://lovevery.com/products.json
- B03: Fisher-Price → https://fisher-price.com/en-us/brands/baby/products.html

---

## 二、亚马逊店铺 (Amazon Stores)

> 抓取策略:Playwright 抓 Seller 主页 (如 `amazon.com/seller/amzn1.seller.xxx`) + Best Sellers。
> 抓取频率:每日 1 次(每日 09:00,见 Phase C 任务 C1)。

| # | 店铺名 | 卖家 ID / ASIN | 类目 | 国家/地区 | 上次抓取 | 状态 |
|---|--------|---------------|------|----------|----------|------|
| S01 | _(待填)_ | amzn1.seller.xxxxx | 玩具 | US | - | ⏳ 待配置 |
| S02 | _(待填)_ | amzn1.seller.xxxxx | 婴儿用品 | US | - | ⏳ 待配置 |
| S03 | _(待填)_ | amzn1.seller.xxxxx | 户外 | DE | - | ⏳ 待配置 |
| S04 | _(待填)_ | amzn1.seller.xxxxx | 玩具 | US | - | ⏳ 待配置 |
| S05 | _(待填)_ | amzn1.seller.xxxxx | 玩具 | US | - | ⏳ 待配置 |

**常用抓取方式**:
- 店铺主页:`https://www.amazon.com/s?i=merchant-terms&me=卖家ID`
- 品牌聚合:`https://www.amazon.com/stores/品牌名/page/店铺ID`
- Best Sellers:`https://www.amazon.com/Best-Sellers-类目/zgbs/类目ID/`

---

## 三、卖家精灵筛选 (SellerSprite Filters)

> 调用方式:WorkBuddy MCP 工具 `mcp__sellersprite__*`
> 抓取频率:每日 1 次 + 用户手动触发(见 Phase C 任务 C1, C2)。

### 筛选组 A · 行业新爆款

| 字段 | 值 | 说明 |
|------|----|------|
| 类目 | Toys & Games > Baby Toys (类目 ID: 165797011) | 主目标类目 |
| 上架时间 | 近 30 天 | `launch_date >= 30_days_ago` |
| 月销量 | 100 ~ 5000 | 中等热度 |
| 评分 | 4.0 ~ 5.0 | 质量门槛 |
| 评论数 | 5 ~ 500 | 新品雏形 |
| 价格 | $15 ~ $80 | 中端价位 |
| BSR 趋势 | 上升 | 趋势筛选 |
| 排除品牌 | 头部 5 品牌 | 避免红海 |

### 筛选组 B · 利润蓝海款

| 字段 | 值 | 说明 |
|------|----|------|
| 类目 | Baby Products (类目 ID: 165796011) | 主营类目 |
| 上架时间 | 近 60 天 | 稍宽窗口 |
| 月销量 | 50 ~ 2000 | 低竞争区间 |
| 评论数 | 0 ~ 100 | 蓝海机会 |
| 价格 | $20 ~ $100 | 利润空间 |
| 配送方式 | FBA | 物流标准 |
| 卖家类型 | 不限 | 含自营与第三方 |

### 筛选组 C · 季节性爆发

| 字段 | 值 | 说明 |
|------|----|------|
| 类目 | Outdoor & Sports (类目 ID: 3375251) | 季节品 |
| 上架时间 | 近 90 天 | 含提前布局 |
| 月销量 | 200 ~ 10000 | 季节高需求 |
| 价格 | $25 ~ $150 | 客单价中等 |
| BSR 趋势 | 季节上升 | Q3/Q4 旺季 |
| 关键词 | 关键词 x 5 | 补足(待填) |

---

## 四、待填字段速查

下面是你**最容易**忘的字段,系统会在你提交意向时主动提示:

- [ ] **品牌官网**(≥ 3 个)
  - 品牌名 / 官网 URL / 入口页规则
- [ ] **亚马逊店铺**(≥ 3 个)
  - 店铺名 / 卖家 ID / 类目 / 地区
- [ ] **卖家精灵筛选组**(≥ 1 个)
  - 类目 / 价格区间 / 评分 / 评论数 / 销量范围
- [ ] **通用偏好**
  - 抓取国家(US/UK/DE/JP/...)
  - 抓取时间窗(近 7/30/60/90 天)
  - 是否排除头部品牌(是/否)
  - 是否要历史快照(是/否)
  - 推送渠道(IMA / 飞书 / 邮件 / 静默)

---

## 五、提交流程

1. 你把上表填好后,直接发给我或贴到对话中
2. 我会帮你:
   - 验证 URL / 卖家 ID 可达性
   - 把意向写入 `data/watchlist.json`(机器可读)
   - 在门户首页展示你的监控列表
3. 之后 Phase C 任务 C1 (每日 09:00 自动化) 会读取这份清单,真正开始抓取

---

## 六、当前状态

| 维度 | 进度 |
|------|------|
| 品牌意向 | 0/5 |
| 店铺意向 | 0/5 |
| 卖家精灵筛选组 | 0/3 |
| 通用偏好 | 0/5 |

**整体完成度**: 0% (框架已就位,等待你填入)

> 💡 提示:你可以现在就在对话里告诉我 3-5 个品牌 + 3-5 个店铺 + 1-2 个筛选组,我立刻把数据写入并启动 Phase B 接入。
