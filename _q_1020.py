# -*- coding: utf-8 -*-
import json, urllib.request, io, sys
out = []
UA = {'User-Agent': 'Mozilla/5.0'}
SECS = {
    '上证指数': '1.000001', '深证成指': '0.399001', '创业板指': '0.399006',
    '科创50': '1.000688', '沪深300': '1.000300', '北证50': '0.899050',
    '恒生指数': '100.HSI', '国企指数': '100.HSCEI', '恒生科技': '124.HSTECH',
}
for name, sec in SECS.items():
    url = ('https://push2his.eastmoney.com/api/qt/stock/kline/get?'
           'secid=%s&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61'
           '&klt=101&fqt=0&end=20500101&lmt=4' % sec)
    try:
        req = urllib.request.Request(url, headers=UA)
        d = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
        ks = (d.get('data') or {}).get('klines') or []
        out.append('%s [%s] -> %s' % (name, sec, ks[-3:] if ks else 'NONE'))
    except Exception as e:
        out.append('%s [%s] -> ERR %s' % (name, sec, e))
open(r'c:/Users/kelvinyye/WorkBuddy/20260314103829/_q_1020.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
