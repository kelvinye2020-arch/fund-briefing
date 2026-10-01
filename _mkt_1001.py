# -*- coding: utf-8 -*-
import json, urllib.request, io, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
out = io.StringIO()
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def kline(secid, n=4):
    url = ('https://push2his.eastmoney.com/api/qt/stock/kline/get?'
           f'secid={secid}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61'
           '&klt=101&fqt=1&end=20500101&lmt=%d' % n)
    try:
        req = urllib.request.Request(url, headers=UA)
        d = json.loads(urllib.request.urlopen(req, timeout=20).read().decode('utf-8'))
        if not d.get('data') or not d['data'].get('klines'):
            return secid, None, 'no data'
        name = d['data'].get('name', '?')
        return secid, name, d['data']['klines']
    except Exception as e:
        return secid, None, repr(e)

targets = [
    ('上证指数', '1.000001'), ('深证成指', '0.399001'), ('创业板指', '0.399006'),
    ('沪深300', '1.000300'), ('科创50', '1.000688'), ('科创综指', '1.000680'),
    ('北证50', '0.899050'), ('恒生指数', '100.HSI'), ('国企指数', '100.HSCEI'),
    ('恒生科技', '100.HSTECH'), ('道琼斯', '105.DJIA'), ('纳斯达克', '105.NDX'),
    ('标普500', '105.SPX'),
]
for label, sid in targets:
    sid_, name, kl = kline(sid)
    out.write(f'### {label} ({sid}) name={name}\n')
    if isinstance(kl, list):
        for line in kl[-3:]:
            out.write('   ' + line + '\n')
    else:
        out.write(f'   ERR: {kl}\n')
open('_mkt_1001.txt', 'w', encoding='utf-8').write(out.getvalue())
print('done')
