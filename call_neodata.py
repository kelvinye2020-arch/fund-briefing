import subprocess
import json
import sys

# 设置工作目录
script_path = r"C:\Users\kelvinyye\.workbuddy\plugins\marketplaces\cb_teams_marketplace\plugins\finance-data\skills\neodata-financial-search\scripts"

# 构建命令
cmd = [sys.executable, "query.py", "--query", "2026年5月8日公募基金行业最新新闻"]

# 执行命令
try:
    result = subprocess.run(
        cmd,
        cwd=script_path,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    if result.stdout:
        print("标准输出:", result.stdout[:1000])
    if result.stderr:
        print("错误输出:", result.stderr)
        
    # 尝试解析JSON
    if result.stdout.strip():
        try:
            data = json.loads(result.stdout)
            print("\n解析成功!")
            print("code:", data.get("code"))
            print("suc:", data.get("suc"))
            print("msg:", data.get("msg"))
            
            # 如果有数据，显示部分内容
            if data.get("data"):
                print("\n部分数据:")
                api_data = data["data"].get("apiData", {})
                doc_data = data["data"].get("docData", {})
                
                if api_data:
                    print("API数据条目数:", len(api_data.get("apiRecall", [])))
                if doc_data:
                    print("文档数据组数:", len(doc_data.get("docRecall", [])))
                    
        except json.JSONDecodeError as e:
            print("JSON解析错误:", e)
            print("输出内容:", result.stdout[:500])
            
except Exception as e:
    print("执行错误:", str(e))