import sqlite3, json
from datetime import datetime, timezone, timedelta

db_path = r'C:\Users\kelvinyye\AppData\Roaming\WorkBuddy\automations\automations.db'
db = sqlite3.connect(db_path)
db.row_factory = sqlite3.Row
cur = db.cursor()

CST = timezone(timedelta(hours=8))
def ts(v):
    if not v: return None
    try:
        # 看数值大小，判断ms还是s
        v = int(v)
        if v > 10**12: v = v / 1000
        return datetime.fromtimestamp(v, CST).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return v

print("=" * 80)
print("AUTOMATIONS")
print("=" * 80)
cur.execute("SELECT id, name, status, last_run_at, next_run_at, cwds, rrule, schedule_type, valid_from, valid_until FROM automations WHERE id IN ('git', 'automation', 'automation-8')")
for r in cur.fetchall():
    d = dict(r)
    print(f"\n[{d['id']}] {d['name']}  status={d['status']}")
    print(f"  last_run_at: {ts(d['last_run_at'])}")
    print(f"  next_run_at: {ts(d['next_run_at'])}")
    print(f"  cwds: {d['cwds']}")
    print(f"  rrule: {d['rrule']}")
    print(f"  schedule_type: {d['schedule_type']}")
    print(f"  valid: {d['valid_from']} ~ {d['valid_until']}")

print("\n" + "=" * 80)
print("RECENT RUNS (since 2026-06-01, by created_at)")
print("=" * 80)
# 6-1的UTC时间戳
cutoff = int(datetime(2026, 6, 1, tzinfo=CST).timestamp() * 1000)
cur.execute("SELECT thread_id, automation_id, status, source_cwd, runs_json, result_success, created_at, updated_at, thread_title FROM automation_runs WHERE created_at >= ? ORDER BY created_at DESC", (cutoff,))
for r in cur.fetchall():
    d = dict(r)
    print(f"\n[{d['automation_id']}] {ts(d['created_at'])} -> status={d['status']} success={d['result_success']}")
    print(f"  thread_id: {d['thread_id']}")
    print(f"  thread_title: {d['thread_title']}")
    print(f"  source_cwd: {d['source_cwd']}")
    if d['runs_json']:
        try:
            rj = json.loads(d['runs_json'])
            if isinstance(rj, list):
                for run in rj[:5]:
                    print(f"  run: {json.dumps(run, ensure_ascii=False)[:400]}")
            else:
                print(f"  runs_json: {json.dumps(rj, ensure_ascii=False)[:400]}")
        except:
            print(f"  runs_json(raw): {d['runs_json'][:400]}")

db.close()
