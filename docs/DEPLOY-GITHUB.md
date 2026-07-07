# 部署到 GitHub（自动抓取 + 公开访问）

> 目标：把 ROBUD Operations 推到 GitHub，每天 09:00 自动抓取 28 个竞品品牌官网，
> 前端通过 GitHub Pages 公开访问，全程无需 AI、无需手动操作。

---

## 一、准备（一次性，约 5 分钟）

### 1. 注册 GitHub 账号
访问 https://github.com/signup ，用邮箱注册（推荐用公司邮箱）。

### 2. 在本地安装 Git
- 下载：https://git-scm.com/downloads
- 安装时一路 Next 即可（默认选项含 Git Bash）
- 验证：打开 Git Bash 输入 `git --version`

### 3. 配置 Git 身份（只需一次）
```bash
git config --global user.name "你的名字"
git config --global user.email "你的GitHub邮箱"
```

---

## 二、创建仓库并推送

### 1. 在 GitHub 网页端新建仓库
- 点右上角 **+** → **New repository**
- Repository name: `ROBUD-Operations`
- 选 **Public**（免费，代码不含敏感信息）
- **不要**勾选 Add README / .gitignore（我们已有文件）
- 点 **Create repository**

### 2. 本地初始化并推送
在 Git Bash 里执行（替换 `<你的用户名>`）：

```bash
cd /c/Users/RT/WorkBuddy/ROBUD-Operations

git init
git add .
git commit -m "init: ROBUD Operations 选品助手 + 自动抓取"
git branch -M main
git remote add origin https://github.com/<你的用户名>/ROBUD-Operations.git
git push -u origin main
```

推送成功后，代码就在 GitHub 上了。

---

## 三、启用 GitHub Pages（公开访问）

1. 进入仓库 **Settings** → **Pages**（左侧菜单）
2. **Build and deployment** → Source 选 **Deploy from a branch**
3. Branch 选 **main**，目录选 **/portal** （门户在 portal/ 目录）
4. 点 **Save**
5. 等待 1-2 分钟，获得地址：
   `https://<你的用户名>.github.io/ROBUD-Operations/portal/`
6. 选品助手地址：
   `https://<你的用户名>.github.io/ROBUD-Operations/portal/tools/product-helper/`

> 注意：GitHub Pages 部署的是静态文件。**抓取脚本不在 Pages 上跑**——
> 它跑在 GitHub Actions（另一个服务）里，结果写入 `products.json`，
> Pages 只是把包含最新 `products.json` 的仓库内容展示出来。

---

## 四、启用自动抓取（GitHub Actions）

抓取已配置在 `.github/workflows/daily-scrape.yml`，**无需额外设置**，
推送代码后即生效。

### 手动触发测试（推荐先跑一次）
1. 仓库顶部 **Actions** 标签
2. 左侧选 **Daily Competitor Scrape**
3. 点 **Run workflow** → **Run workflow**（分支选 main）
4. 等待 3-10 分钟（取决于站点数量和网络）
5. 点进运行记录看日志，确认 `OK (xx)` 数量
6. 结束后 `products.json` 会被自动 commit 回仓库

### 每日自动运行
- 默认 **每天北京时间 09:00** 自动触发（cron: `0 1 * * *` UTC）
- 无需任何操作，第二天来看数据已更新

### 改抓取时间
编辑 `.github/workflows/daily-scrape.yml` 里的 `cron:` 行。
[cron 表达式生成器](https://crontab.guru/) 可辅助。例如：
- 每天 08:00 北京 = `0 0 * * *`
- 每天 12:00 北京 = `0 4 * * *`
- 每 6 小时 = `0 */6 * * *`

---

## 五、监控与维护

### 查看抓取结果
- **Actions** 页面：每次运行的日志、成功/失败站点数
- 仓库文件 `tools/product-helper/data/products.json`：最新数据
- 网站打开后，顶部「最后更新」显示日期

### 添加 / 移除品牌
编辑 `tools/product-helper/data/watchlist.json`：
- 新增：复制一行 `{"id":"B30", "name":"...", "url":"...", "strategy":"shopify|html|playwright", "enabled":true}`
- 暂停某个站：把 `"enabled":true` 改成 `false`
- commit 后下次自动抓取生效

### 抓取失败怎么办
- 单个站点失败不会中断整体（脚本有 try/except）
- 常见原因：站点改版（HTML 选择器失效）、临时封 IP、网络抖动
- 修复：检查 Actions 日志里 `[FAIL]` 的站点，调整 `scrape.py` 里对应解析逻辑

### 免费额度
- 公开仓库：GitHub Actions **完全免费**（2000 分钟/月，足够每天跑）
- 私有仓库：Actions 免费额度 2000 分钟/月（也够）；GitHub Pages 需 GitHub Pro ($4/月)
- 建议用 **Public** 仓库

---

## 六、本地运行（不依赖 GitHub）

```bash
cd /c/Users/RT/WorkBuddy/ROBUD-Operations
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r scraper/requirements.txt
python scraper/scrape.py --site B04   # 单站测试
python scraper/scrape.py              # 全量抓取
```

抓取结果写入 `tools/product-helper/data/products.json`，
本地用 `python -m http.server` 打开 `portal/` 即可看到。

---

## 七、目录结构（部署后）

```
ROBUD-Operations/
├── .github/workflows/daily-scrape.yml   # 自动抓取定时任务
├── scraper/
│   ├── scrape.py                         # 三路抓取脚本
│   └── requirements.txt
├── tools/product-helper/
│   ├── index.html                        # 前端（fetch products.json）
│   └── data/
│       ├── watchlist.json                # 28 个品牌配置
│       └── products.json                 # 自动生成的抓取结果
├── portal/                               # GitHub Pages 入口
└── docs/
```
