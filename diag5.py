import sqlite3, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

db_path = r'c:\Users\kelvinyye\AppData\Roaming\WorkBuddy\automations\automations.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get full prompt for automation-8
cur.execute("SELECT prompt FROM automations WHERE id = 'automation-8'")
row = cur.fetchone()
if row:
    print("AUTOMATION-8 FULL PROMPT:")
    print("=" * 60)
    print(row[0])

# Also check git full prompt
print("\n\n")
cur.execute("SELECT prompt FROM automations WHERE id = 'git'")
row = cur.fetchone()
if row:
    print("GIT FULL PROMPT:")
    print("=" * 60)
    print(row[0][:2000])
    if len(row[0]) > 2000:
        print(f"\n... (truncated, total {len(row[0])} chars)")

# Check all automation IDs and models
print("\n\nALL AUTOMATIONS:")
print("=" * 60)
cur.execute("SELECT id, name, status, model_id FROM automations ORDER BY id")
for r in cur.fetchall():
    print(f"  {r[0]:20s} | {r[2]:8s} | {r[3] or 'N/A':30s} | {r[1]}")

conn.close()
