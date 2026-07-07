# 部署到 GitHub（自动抓取 + 公开访问）

> 目标：把 ROBUD Operations 推到 GitHub，每天 09:00 自动抓取 28 个竞品品牌官网，
> 前端通过 GitHub Pages 公开访问，全程无需 AI、无需手动操作。

---

## 一、准备工作（一次性）

### 1. 注册 GitHub 账号
访问 https://github.com/signup ，用邮箱注册（推荐公司邮箱）。

### 2. Git 已装好
本机已验证 `git version 2.54.0`，无需重装。
打开 **Git Bash**（开始菜单搜 Git Bash）执行后续命令。

### 3. 配置 Git 身份（只需一次，全局）
```bash
git config --global user.name "你的名字"
git config --global user.email "你的GitHub邮箱"
```
> 本仓库当前的提交身份是占位符 `ROBUD Ops <robud@example.com>`。
> 想让贡献图归到你名下，push 前执行下面任意一条：
> ```bash
> # 改全局（影响以后所有仓库）
> git config --global user.email "你真实的GitHub邮箱"
> # 仅改最近一次提交作者
> git commit --amend --reset-author -m "feat: ROBUD Operations platform ..."
> ```
> GitHub 邮箱可在 Settings → Emails 里复制「@users.noreply.github.com」那个，避免暴露真实邮箱。

---

## 二、创建仓库（GitHub 网页端）

1. 登录后点右上角 **+** → **New repository**
2. **Repository name**: `ROBUD-Operations`
3. **Visibility**: 选 **Public**（免费，代码不含敏感信息）
4. **不要**勾选 *Add a README file* / *Add .gitignore* / *Choose a license*
   —— 我们本地已有完整文件，勾了反而会导致首次 push 冲突
5. 点 **Create repository**
6. 创建后会看到一个快速上手页面，**不要照它里面的命令做**，按本文第三步来

---

## 三、认证方式（push 必须，最容易卡在这里）

GitHub **已不支持用账号密码 push**，必须用下面任一种凭证。

### 方式 A：HTTPS + Personal Access Token（推荐，零安装）

1. GitHub 网页 → 右上角头像 → **Settings**
2. 左侧最底部 **Developer settings** → **Personal access tokens** → **Tokens (classic)**
   （或新版 **Fine-grained tokens**，权限更细，二选一）
3. 点 **Generate new token** → 勾选 **repo**（整项勾选，含所有子权限）
4. 设个过期时间（如 90 天），点 **Generate token**
5. **立刻复制那串 `ghp_xxx` 令牌**——页面关掉就再也看不到了

之后 push 时：
- `Username` 填你的 GitHub **用户名**
- `Password` 粘贴刚才复制的 **token**（不是你的登录密码）

> 嫌每次输入麻烦，可让 Git 记住凭证：
> ```bash
> git config --global credential.helper manager
> ```
> 首次输入后，Windows 凭据管理器会保存，之后不再问。

### 方式 B：SSH 密钥（一劳永逸，但要多一步）

```bash
# 生成密钥（一路回车，不设密码最省事）
ssh-keygen -t ed25519 -C "你的GitHub邮箱"
# 打印公钥，整段复制
cat ~/.ssh/id_ed25519.pub
```
1. GitHub 网页 → Settings → **SSH and GPG keys** → **New SSH key**
2. Title 随意，Key 粘贴上面复制的内容，点 **Add SSH key**
3. 本文第三步里把远程地址换成 SSH 形式：
   `git remote add origin git@github.com:<你的用户名>/ROBUD-Operations.git`

---

## 四、本地已初始化，只需添加远程并推送

本仓库已经在本地 `git init` + `commit` 完成（17 个文件，`.venv` 已排除）。
你在 Git Bash 里只需执行以下几条（替换 `<你的用户名>`）：

```bash
cd /c/Users/RT/WorkBuddy/ROBUD-Operations

# 1. 把分支名统一成 main（GitHub 默认分支，便于 Pages/Actions 识别）
git branch -M main

# 2. 关联远程仓库（HTTPS 方式，配合方式 A 的 token）
git remote add origin https://github.com/<你的用户名>/ROBUD-Operations.git
# 若用 SSH（方式 B），改成：
# git remote add origin git@github.com:<你的用户名>/ROBUD-Operations.git

# 3. 推送（首次会要求输入 用户名 + token）
git push -u origin main
```

推送成功即代表代码已上 GitHub。可在仓库页面刷新看到文件。

---

## 五、启用 GitHub Pages（公开访问）

1. 仓库 **Settings** → 左侧 **Pages**
2. **Build and deployment** → Source 选 **Deploy from a branch**
3. Branch 选 **main**，目录选 **/ (root)**  ← 注意：只能选根目录或 /docs，不能选 /portal
4. 点 **Save**
5. 等待 1–2 分钟，访问：
   - 首页（自动跳转门户）：`https://<你的用户名>.github.io/ROBUD-Operations/`
   - 门户：`https://<你的用户名>.github.io/ROBUD-Operations/portal/`
   - 选品助手：`https://<你的用户名>.github.io/ROBUD-Operations/tools/product-helper/`

> 为什么选根目录？因为仓库根有一个 `index.html` 会自动 302 跳转到 `./portal/`。
> 所有前端资源都用相对路径，子路径下不会出现 404。
> 抓取脚本不在 Pages 上跑——它跑在 GitHub Actions，结果写入 `products.json`，Pages 只是展示最新数据。

---

## 六、启用自动抓取（GitHub Actions）

抓取已配置在 `.github/workflows/daily-scrape.yml`，推送后**自动生效**。

### 手动触发测试（强烈建议先跑一次）
1. 仓库顶部 **Actions** 标签
2. 左侧选 **Daily Product Scrape**
3. 点 **Run workflow** → 分支选 **main** → **Run workflow**
4. 等 3–10 分钟，点运行记录看日志
5. 确认 `[OK]` 站点数量；Playwright 类站点（Target / John Lewis 等）在 CI 里才会真正抓取
6. 结束自动把新 `products.json` commit 回仓库

### 每日自动运行
- 默认 **每天北京时间 09:00**（cron: `0 1 * * *` UTC）
- 改时间：编辑 `.github/workflows/daily-scrape.yml` 的 `cron:` 行
  （生成器：https://crontab.guru/ ，注意是 UTC）

---

## 七、监控与维护

### 看结果
- **Actions** 页：每次运行日志、成功/失败站点数
- 仓库文件 `tools/product-helper/data/products.json`：最新数据
- 网站顶部「最后更新」显示日期

### 加 / 减品牌
编辑 `tools/product-helper/data/watchlist.json`：
- 新增一行 `{ "id":"B30", "name":"...", "url":"...", "strategy":"shopify|html|playwright", "enabled":true }`
- 暂停某站：`"enabled": true` → `false`
- commit 后下次抓取生效

### 抓取失败
- 单站失败不中断整体（脚本有 try/except）
- 常见：站点改版（选择器失效）、临时封 IP、网络抖动
- 修复：看 Actions 日志 `[FAIL]` 站点，调 `scraper/scrape.py` 对应解析

### 免费额度
- 公开仓库：Actions **完全免费**（2000 分钟/月，每天跑足够）
- 私有仓库：Actions 同样免费额度；但 GitHub Pages 需 GitHub Pro（$4/月）
- **建议 Public**

---

## 八、本地运行（不依赖 GitHub）

```bash
cd /c/Users/RT/WorkBuddy/ROBUD-Operations
python -m venv .venv
.venv/Scripts/activate          # 激活虚拟环境
pip install -r scraper/requirements.txt
python scraper/scrape.py --site B04   # 单站测试
python scraper/scrape.py              # 全量抓取
```
结果写入 `tools/product-helper/data/products.json`；
本地 `python -m http.server` 起服务后访问 `portal/` 即可预览。

---

## 九、目录结构（部署后）

```
ROBUD-Operations/
├── index.html                          # 根目录跳转页 → portal/
├── .github/workflows/daily-scrape.yml  # 自动抓取定时任务
├── scraper/
│   ├── scrape.py                        # 三路抓取脚本
│   └── requirements.txt
├── tools/product-helper/
│   ├── index.html                       # 前端（fetch products.json）
│   └── data/
│       ├── watchlist.json               # 28 个品牌配置
│       └── products.json                # 自动生成的抓取结果
├── portal/                              # 平台门户（GitHub Pages 入口）
└── docs/
```
