#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_check.py — 基金看板 daily-update 提交前三道闸
=====================================================
每次 daily-update / weekly-refresh 生成内容后、git commit 前必须运行：

    python3 gate_check.py

退出码 0 = 通过，可以提交；退出码 1 = 拒绝提交，输出里会列出所有违规项。

三道硬闸（违反即拒绝）：
  闸1 header 数据区间联动：上端点必须是今天或昨天；下端点必须 = 上端点 - 14 天（T-14）
  闸2 date-tag T-14 真实性：所有 <span class="date-tag">MM-DD</span> 不得早于 T-14 边界
  闸3 源链接黑名单：JFE 拦截域名 + UGC 域名 + 自媒体汇总页

一道软闸（只告警不拒绝）：
  闸4 source-tag 与 URL 域名一致性（防"tag 写证券时报、URL 是 21财经"式错标）

幻觉防御（csrc 事件教训 2026-08-24 / 2026-09-04）：
  凡引用 csrc.gov.cn / gov.cn / amac.org.cn 等官方站点的卡片，写卡前必须 WebFetch
  源页面提取"日期：YYYY-MM-DD"，与卡片 date-tag 比对，差 >2 天即幻觉缝合，禁止写入。
  本脚本对这类域名做"存在性提醒"，强制人工确认（见闸5输出）。
"""
import re
import sys
from datetime import date, timedelta

HTML = 'index.html'
TODAY = date.today()

# ---------------- 黑名单（2026-08-24 全量审计固化） ----------------
DOMAIN_BLACKLIST = {
    'm.21jingji.com':   'JFE 493 拦截（21财经移动版）',
    '21jingji.com':     'JFE 493 拦截（21财经）',
    'stcn.com':         'JFE 拦截风险（证券时报官网）',
    'www.cls.cn':       'JFE 拦截风险（财联社）',
    'cls.cn':           'JFE 拦截风险（财联社）',
    'guba.eastmoney.com': '股吧 UGC（营销软文重灾区，非新闻源）',
    'yicai.com':        'JFE 拦截风险（第一财经）',
}
# 自媒体汇总页特征（URL 路径或页面类型）
SELF_MEDIA_PATTERNS = ['投资日报', '基金日报', '财经早报', '日报']

# source-tag 媒体名 -> 允许的域名（防错标）
TAG_DOMAIN_MAP = {
    '证券时报':   ['stcn.com'],          # 但 stcn 本身在黑名单——出现即双重违规
    '中国证券报': ['cs.com.cn', 'gu.qq.com', 'so.html5.qq.com', 'finance.sina'],
    '上海证券报': ['cnstock.com', 'sac.net.cn', 'finance.sina'],
    '中国基金报': ['chnfund.com', 'so.html5.qq.com', 'finance.sina'],
    '每日经济新闻': ['nbd.com.cn', 'so.html5.qq.com'],
    '财联社':     ['cls.cn', 'so.html5.qq.com', '163.com'],
    '证监会':     ['csrc.gov.cn'],
    '中国基金业协会': ['amac.org.cn'],
    '证券业协会': ['sac.net.cn'],
}

# 官方站点——幻觉重灾区，强制人工确认（闸5）
OFFICIAL_DOMAINS = ['csrc.gov.cn', 'gov.cn', 'amac.org.cn', 'sac.net.cn', 'pbc.gov.cn']

def main():
    src = open(HTML, encoding='utf-8').read()
    errors, warns = [], []

    # ============ 闸1：header 数据区间 ============
    m = re.search(r'数据区间：(\d{4})\.(\d{2})\.(\d{2})\s*—\s*(\d{4})\.(\d{2})\.(\d{2})', src)
    if not m:
        errors.append('[闸1] header 数据区间角标缺失或格式错误')
    else:
        y1, mo1, d1, y2, mo2, d2 = map(int, m.groups())
        lo, hi = date(y1, mo1, d1), date(y2, mo2, d2)
        # 上端点：允许今天或昨天（早上跑时今日新闻未出全）
        if hi not in (TODAY, TODAY - timedelta(days=1)):
            errors.append(f'[闸1] header 上端点 {hi} 不是今天/昨天（{TODAY}）——区间没联动更新')
        expect_lo = hi - timedelta(days=14)
        if lo != expect_lo:
            errors.append(f'[闸1] header 下端点 {lo} != 上端点-14天（应为 {expect_lo}）——T-14 未生效')

    # ============ 闸2：date-tag T-14 ============
    t14 = TODAY - timedelta(days=14)
    for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src):
        mo, d = int(m.group(1)), int(m.group(2))
        try:
            dt = date(TODAY.year, mo, d)
        except ValueError:
            errors.append(f'[闸2] 非法日期标签 {mo:02d}-{d:02d}')
            continue
        if dt < t14:
            idx = m.start()
            before = src[max(0, idx - 3000):idx]
            titles = re.findall(r'<div class="card-title">([^<]+)</div>', before)
            t = titles[-1][:50] if titles else '?'
            # 带"调研延续"标注的是有意保留的历史卡，降级为告警
            after = src[m.end():m.end() + 200]
            if '调研延续' in after:
                warns.append(f'[闸2] {dt} 超T-14但带"调研延续"标注（{t}）——确认是有意保留')
            else:
                errors.append(f'[闸2] date-tag {dt} 超 T-14（边界 {t14}）：{t}')

    # ============ 闸3：源链接黑名单 ============
    urls = re.findall(r'href="(https?://[^"]+)"', src)
    for u in urls:
        dom = re.search(r'https?://([^/"]+)', u).group(1)
        for bad, reason in DOMAIN_BLACKLIST.items():
            if bad in dom:
                errors.append(f'[闸3] 黑名单域名 {dom}（{reason}）：{u[:70]}')
        for pat in SELF_MEDIA_PATTERNS:
            if pat in u:
                warns.append(f'[闸3] 疑似自媒体汇总页：{u[:70]}')

    # ============ 闸4（软）：source-tag 与域名一致性 ============
    for m in re.finditer(r'href="(https?://[^"]+)"[^>]*><span class="source-tag">([^<]+)</span>', src):
        u, tag = m.groups()
        dom = re.search(r'https?://([^/"]+)', u).group(1)
        tag_name = re.sub(r'[·\s].*$', '', tag)  # "中国基金报·08-23" -> "中国基金报"
        if tag_name in TAG_DOMAIN_MAP:
            allowed = TAG_DOMAIN_MAP[tag_name]
            if not any(a in dom for a in allowed):
                warns.append(f'[闸4] source-tag "{tag_name}" 与域名 {dom} 不匹配：{u[:60]}')

    # ============ 闸5（提醒）：官方站点幻觉防御 ============
    official_hits = [u for u in urls if any(od in u for od in OFFICIAL_DOMAINS)]
    if official_hits:
        warns.append('[闸5] 以下官方站链接必须已 WebFetch 验证过页面真实日期（防 csrc 幻觉缝合）：')
        for u in official_hits:
            warns.append(f'       - {u[:80]}')

    # ============ 输出 ============
    print(f'===== gate_check @ {TODAY} =====')
    for w in warns:
        print(f'⚠️  {w}')
    for e in errors:
        print(f'❌ {e}')
    if errors:
        print(f'\n拒绝提交：{len(errors)} 个硬违规。修复后重跑。')
        sys.exit(1)
    print(f'\n✅ 三道硬闸通过（{len(warns)} 条告警需人工确认）')
    sys.exit(0)

if __name__ == '__main__':
    main()
