import re
with open('index.html', encoding='utf-8') as f:
    lines = f.readlines()
keys = re.compile(r'(04[-./月]\d{1,2}|03[-./月]\d{1,2}|数据区间|daily-update|content-fingerprint|class="section-title|class="card-title|news-date|item-date|<h2|<h3)')
out = []
for i, l in enumerate(lines, 1):
    if keys.search(l):
        out.append(f"{i}: {l.rstrip()[:200]}")
with open('_scan.txt', 'w', encoding='utf-8') as g:
    g.write('\n'.join(out))
print(len(out), 'lines matched')
