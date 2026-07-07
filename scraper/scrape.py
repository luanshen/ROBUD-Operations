#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROBUD Operations · 竞品新品每日抓取

读取 ../tools/product-helper/data/watchlist.json 中的品牌官网列表，
按策略 (shopify / html / playwright) 抓取新品，输出合并后的 products.json。

用法:
  python scrape.py                 # 抓取所有 enabled 品牌
  python scrape.py --site B04      # 只抓单个站点 (调试用)
  python scrape.py --dry-run       # 不写文件，只打印统计

兼容:
  - 本地: python scraper/scrape.py
  - CI:  GitHub Actions 每天 09:00 (UTC 01:00) 自动运行
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------
# 路径 & 常量
# ----------------------------------------------------------------------------
BASE = Path(__file__).parent.parent
WATCHLIST = BASE / "tools/product-helper/data/watchlist.json"
OUTPUT = BASE / "tools/product-helper/data/products.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

DELAY = 2.0  # 站点间礼貌延迟(秒)
MAX_PER_SITE = 150  # 每站最多保留商品数(防止单站全量目录撑爆文件)
SHOPIFY_WINDOW_DAYS = 90  # Shopify 站点只保留近 N 天新品(其 API 含精确上架时间)


# ----------------------------------------------------------------------------
# 工具函数
# ----------------------------------------------------------------------------
def make_id(brand: str, idx: int) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]", "", brand)[:4].upper() or "BRND"
    return f"{slug}{idx:04d}"


def parse_price(text: str):
    """从文本提取价格与货币。返回 (float|None, str)。"""
    if not text:
        return None, "USD"
    m = re.search(r"([$€£¥])\s?(\d[\d,]*\.?\d*)", text)
    if not m:
        return None, "USD"
    symbol = m.group(1)
    amount = float(m.group(2).replace(",", ""))
    currency = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "CNY"}[symbol]
    return round(amount, 2), currency


def to_absolute(url: str, base: str) -> str:
    if not url:
        return ""
    if url.startswith("http"):
        return url
    if url.startswith("//"):
        return urlparse(base).scheme + ":" + url
    if url.startswith("/"):
        netloc = urlparse(base).scheme + "://" + urlparse(base).netloc
        return netloc + url
    return urlparse(base).scheme + "://" + urlparse(base).netloc + "/" + url.lstrip("/")


def normalize(prod: dict) -> dict:
    """统一字段，防止缺字段导致前端渲染报错。"""
    return {
        "id": prod.get("id") or make_id(prod.get("brand", "X"), 0),
        "source": prod.get("source", "brand"),
        "title": (prod.get("title") or prod.get("name") or "未命名")[:200],
        "brand": prod.get("brand", ""),
        "price": float(prod.get("price") or 0),
        "oldPrice": prod.get("oldPrice"),
        "currency": prod.get("currency", "USD"),
        "image": prod.get("image", ""),
        "url": prod.get("url", ""),
        "tags": prod.get("tags", []),
        "launchDate": prod.get("launchDate")
        or prod.get("created")
        or datetime.now().strftime("%Y-%m-%d"),
        "rating": prod.get("rating"),
        "reviews": prod.get("reviews"),
        "bsr": prod.get("bsr"),
        "category": prod.get("category", ""),
        "bullets": prod.get("bullets", []),
    }


# ----------------------------------------------------------------------------
# 策略 1: Shopify /products.json
# ----------------------------------------------------------------------------
def scrape_shopify(url: str, brand: str):
    """Shopify 站点: 直接调 /products.json API，无需解析 HTML。
    只保留近 SHOPIFY_WINDOW_DAYS 天的新品，并按上架时间倒序限 MAX_PER_SITE 条。"""
    netloc = urlparse(url).scheme + "://" + urlparse(url).netloc
    collected = []
    page = 1
    while True:
        api = f"{netloc}/products.json?limit=250&page={page}"
        data = None
        for attempt in range(3):
            try:
                r = requests.get(api, headers=HEADERS, timeout=30)
                if r.status_code == 200:
                    data = r.json().get("products", [])
                    break
                elif r.status_code in (429, 403):
                    time.sleep(3 * (attempt + 1))  # 限流/拦截，退避重试
                    continue
                else:
                    break
            except Exception as e:
                if attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                print(f"    [shopify] request error: {e}")
                break
        if data is None:
            break
        if not data:
            break
        for p in data:
            # 缩略图
            img = ""
            if p.get("images"):
                img = p["images"][0].get("src", "")
            # 价格(取第一个变体)
            price = None
            for v in p.get("variants", []):
                if v.get("price"):
                    price, _ = parse_price("$" + str(v["price"]))
                    break
            # 创建时间 -> 用作上架日期
            created = p.get("created_at", "")
            launch = created[:10] if created else datetime.now().strftime("%Y-%m-%d")
            # 标签: 从 product_type + tags 提取
            tags = [t.strip().lower() for t in p.get("tags", []) if t.strip()]
            if "wood" in (p.get("product_type", "") + p.get("title", "")).lower():
                tags = list(set(tags + ["wooden"]))

            collected.append(
                normalize(
                    {
                        "id": make_id(brand, len(collected)),
                        "source": "brand",
                        "title": p.get("title", ""),
                        "brand": brand,
                        "price": price,
                        "currency": "USD",
                        "image": to_absolute(img, netloc),
                        "url": f"{netloc}/products/{p.get('handle', '')}",
                        "tags": tags,
                        "launchDate": launch,
                        "category": p.get("product_type", "Toys"),
                    }
                )
            )
        if len(data) < 250:
            break
        page += 1
        time.sleep(0.5)

    # 过滤近 N 天新品
    cutoff = (datetime.now() - timedelta(days=SHOPIFY_WINDOW_DAYS)).strftime("%Y-%m-%d")
    recent = [p for p in collected if p["launchDate"] >= cutoff]
    # 按上架时间倒序
    recent.sort(key=lambda x: x["launchDate"], reverse=True)
    return recent[:MAX_PER_SITE]


# ----------------------------------------------------------------------------
# 策略 2: HTTP + BeautifulSoup 通用解析
# ----------------------------------------------------------------------------
def scrape_html_generic(url: str, brand: str):
    """
    通用 HTML 解析: 在页面里找「带图片的链接」并提取标题/价格。
    适用于大多数服务端渲染的电商/品牌站。复杂站点可在此扩展专属解析器。
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"    [html] request failed: {e}")
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    products = []
    seen = set()

    # 候选链接: 看起来像商品页的 a 标签
    anchors = soup.select(
        'a[href*="product"], a[href*="produit"], a[href*="prod"], '
        'a[href*="toy"], a[href*="article"], a[href*="p/"], a[href*="item"]'
    )
    for a in anchors:
        href = a.get("href", "")
        if not href or href in seen or href.startswith(("#", "javascript", "mailto")):
            continue
        img = a.find("img")
        if not img:
            continue
        img_url = img.get("src") or img.get("data-src") or img.get("data-srcset") or ""
        if isinstance(img_url, list):
            img_url = img_url[0] if img_url else ""
        if not img_url:
            src = a.find("source")
            if src:
                img_url = src.get("srcset") or src.get("src") or ""
        if not img_url:
            continue

        title = (
            img.get("alt") or a.get("title") or a.get("aria-label") or a.get_text(strip=True) or ""
        ).strip()
        if len(title) < 3:
            continue

        # 价格探测: 在 a 标签及其祖先节点里找货币符号
        price_text = ""
        el = a
        for _ in range(3):
            pt = el.find(string=re.compile(r"[$€£¥]\s?\d[\d,]*\.?\d*"))
            if pt:
                price_text = pt
                break
            el = el.parent
            if not el:
                break
        price, currency = parse_price(price_text)

        products.append(
            normalize(
                {
                    "id": make_id(brand, len(products)),
                    "source": "brand",
                    "title": title,
                    "brand": brand,
                    "price": price,
                    "currency": currency,
                    "image": to_absolute(img_url, url),
                    "url": to_absolute(href, url),
                    "tags": ["wooden"] if "wood" in (title + brand).lower() else [],
                    "launchDate": datetime.now().strftime("%Y-%m-%d"),
                    "category": "Toys",
                }
            )
        )
        seen.add(href)
        if len(products) >= MAX_PER_SITE:
            break

    return products


# ----------------------------------------------------------------------------
# 策略 3: Playwright 无头浏览器 (JS 渲染 / 反爬站点)
# ----------------------------------------------------------------------------
def scrape_playwright(url: str, brand: str):
    """困难站点: 用真实浏览器加载 JS 后再提取。懒加载 playwright。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("    [playwright] 未安装 playwright，跳过 (pip install playwright && playwright install chromium)")
        return []

    products = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(user_agent=HEADERS["User-Agent"])
            page = ctx.new_page()
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            # 常见商品卡片选择器
            cards = page.query_selector_all(
                ".product, .product-item, .product-card, [class*='product-card'], "
                "a[href*='product'], article"
            )
            seen = set()
            for card in cards:
                href = card.get_attribute("href") or ""
                img = card.query_selector("img")
                if not img:
                    continue
                img_url = img.get_attribute("src") or img.get_attribute("data-src") or ""
                if not img_url:
                    continue
                title = (
                    img.get_attribute("alt")
                    or card.get_attribute("aria-label")
                    or (card.inner_text()[:120] if card.inner_text() else "")
                ).strip()
                if len(title) < 3:
                    continue
                if href in seen:
                    continue
                seen.add(href)

                # 价格探测: 卡片文本里找货币
                txt = card.inner_text() or ""
                price, currency = parse_price(txt)

                products.append(
                    normalize(
                        {
                            "id": make_id(brand, len(products)),
                            "source": "brand",
                            "title": title,
                            "brand": brand,
                            "price": price,
                            "currency": currency,
                            "image": to_absolute(img_url, url),
                            "url": to_absolute(href, url),
                            "tags": ["wooden"] if "wood" in (title + brand).lower() else [],
                            "launchDate": datetime.now().strftime("%Y-%m-%d"),
                            "category": "Toys",
                        }
                    )
                )
                if len(products) >= 60:
                    break
            browser.close()
    except Exception as e:
        print(f"    [playwright] error: {e}")
    return products


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def run(only_site: str = None, dry_run: bool = False):
    if not WATCHLIST.exists():
        print(f"[ERROR] 找不到 {WATCHLIST}")
        sys.exit(1)
    wl = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    sites = [s for s in wl.get("brandSites", []) if s.get("enabled")]
    if only_site:
        sites = [s for s in sites if s.get("id") == only_site]
        if not sites:
            print(f"[ERROR] 未找到站点 {only_site}")
            sys.exit(1)

    all_products = []
    ok, fail = 0, 0

    for site in sites:
        name = site.get("name", site.get("id"))
        strategy = site.get("strategy", "html")
        print(f"[*] {name} ({strategy}) ...", end=" ", flush=True)
        try:
            if strategy == "shopify":
                prods = scrape_shopify(site["url"], name)
            elif strategy == "playwright":
                prods = scrape_playwright(site["url"], name)
            else:  # html
                prods = scrape_html_generic(site["url"], name)
            all_products.extend(prods)
            ok += 1
            print(f"OK ({len(prods)})")
        except Exception as e:
            fail += 1
            print(f"FAIL ({e})")
        time.sleep(DELAY)

    out = {
        "updatedAt": datetime.now().isoformat(timespec="seconds"),
        "total": len(all_products),
        "source": "github-actions" if not only_site else "manual",
        "products": all_products,
    }

    print(f"\n==== 统计: {ok} 成功 / {fail} 失败 / 共 {len(all_products)} 商品 ====")
    if dry_run:
        print("[dry-run] 不写入文件")
        return out

    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] 已写入 {OUTPUT} ({OUTPUT.stat().st_size/1024:.1f} KB)")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", help="只抓单个站点 ID (如 B04)")
    ap.add_argument("--dry-run", action="store_true", help="不写文件")
    args = ap.parse_args()
    run(only_site=args.site, dry_run=args.dry_run)
