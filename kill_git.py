import sqlite3, json
DB = r'C:/Users/kelvinyye/AppData/Roaming/WorkBuddy/automations/automations.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print('tables:', tables)

for t in tables:
    c.execute(f"PRAGMA table_info({t})")
    cols = [r[1] for r in c.fetchall()]
    print(f'  {t}:', cols)

# 查git任务记录
c.execute("SELECT * FROM automations WHERE id='git'")
row = c.fetchone()
if row:
    c.execute("PRAGMA table_info(automations)")
    cols = [r[1] for r in c.fetchall()]
    print('\n--- automations.git ---')
    for col, val in zip(cols, row):
        s = str(val)
        if len(s) > 200: s = s[:200] + '...'
        print(f'  {col}: {s}')

# 查最近run记录
if 'automation_runs' in tables:
    c.execute("SELECT * FROM automation_runs WHERE automation_id='git' ORDER BY rowid DESC LIMIT 3")
    runs = c.fetchall()
    c.execute("PRAGMA table_info(automation_runs)")
    cols = [r[1] for r in c.fetchall()]
    print('\n--- recent runs ---')
    for r in runs:
        print()
        for col, val in zip(cols, r):
            s = str(val)
            if len(s) > 150: s = s[:150] + '...'
            print(f'  {col}: {s}')
conn.close()
