import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
DB = r'C:/Users/kelvinyye/AppData/Roaming/WorkBuddy/automations/automations.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

# automation-8 任务详情
c.execute("SELECT id, name, status, next_run_at, last_run_at, rrule FROM automations WHERE id='automation-8'")
print('--- automation-8 task ---')
for r in c.fetchall():
    print(r)

# automation-8 的runs
c.execute("SELECT thread_id, status, result_success, created_at, updated_at, runs_json FROM automation_runs WHERE automation_id='automation-8' ORDER BY rowid DESC LIMIT 5")
print('\n--- automation-8 runs ---')
import datetime
for r in c.fetchall():
    tid, status, succ, c_at, u_at, rj = r
    dt_c = datetime.datetime.fromtimestamp(c_at/1000).strftime('%Y-%m-%d %H:%M:%S')
    dt_u = datetime.datetime.fromtimestamp(u_at/1000).strftime('%Y-%m-%d %H:%M:%S')
    print(f'\n  thread_id: {tid}')
    print(f'  status: {status}, success: {succ}')
    print(f'  created: {dt_c}, updated: {dt_u}')
    print(f'  runs_json: {(rj or "")[:300]}')

# 当前所有 IN_PROGRESS 的runs
print('\n--- ALL IN_PROGRESS runs ---')
c.execute("SELECT thread_id, automation_id, status, created_at, runs_json FROM automation_runs WHERE status NOT IN ('PENDING_REVIEW','COMPLETED','FAILED') ORDER BY rowid DESC")
for r in c.fetchall():
    tid, aid, status, c_at, rj = r
    dt_c = datetime.datetime.fromtimestamp(c_at/1000).strftime('%Y-%m-%d %H:%M:%S')
    print(f'  [{status}] {aid} | {tid} | created={dt_c}')

# 看 status 都有哪些值
c.execute("SELECT DISTINCT status FROM automation_runs")
print('\n--- distinct statuses ---', c.fetchall())

conn.close()
