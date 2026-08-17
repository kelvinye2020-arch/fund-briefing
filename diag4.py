import sqlite3, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

db_path = r'c:\Users\kelvinyye\AppData\Roaming\WorkBuddy\automations\automations.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get runs_json for the failed git runs on 5/28 and 5/29
cur.execute("""
    SELECT thread_id, thread_title, runs_json, result_success, created_at
    FROM automation_runs 
    WHERE automation_id = 'git'
    ORDER BY created_at DESC
    LIMIT 3
""")

for row in cur.fetchall():
    print(f"\n{'='*60}")
    print(f"Thread: {row[0]}")
    print(f"Title: {row[1]}")
    print(f"Success: {row[3]}")
    print(f"Created: {row[4]}")
    print(f"\nRuns JSON:")
    runs = row[2]
    if runs:
        try:
            data = json.loads(runs)
            print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
        except:
            print(runs[:3000])
    else:
        print("  (empty)")

conn.close()
