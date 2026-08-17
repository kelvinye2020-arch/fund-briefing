import requests
import json
import sys

# 凭证
token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJEckVYRDNfbWd6S24wNHZoNXIyaE5KS1VNaVhsQWRFSVc1dXoyWVlXckg4In0.eyJleHAiOjE4MDgyMTcxNTQsImlhdCI6MTc3ODIwNTQ5MCwiYXV0aF90aW1lIjoxNzc2NjgxMTU1LCJqdGkiOiIzMTI3MWY2Ny05YmI4LTQ3NjctYTViNS1iNTdkYjhmZDA4MGQiLCJpc3MiOiJodHRwczovL3RlbmNlbnQuc3NvLmNvZGVidWRkeS5jbi9hdXRoL3JlYWxtcy9zc28tZXRhaHpzcWVqMG40IiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImYyODA3MDEwLTFhZmItNDVlYi1iZjBjLWYxNDY0MjY2ZDRlNyIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNvbnNvbGUiLCJzaWQiOiJkZDQ2Yjg2My01ZDkwLTQ2Y2EtOGZkMC1mZDIyNTAxOGI3YjEiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImRlZmF1bHQtcm9sZXMiLCJvZmZsaW5lX2FjY2VzcyIsImVudC1tZW1iZXI6ZXRhaHpzcWVqMG40IiwiZW50LXBsdWdpbi1lbmFibGVkOmV0YWh6c3FlajBuNCIsImdyb3VwLWFkbWluOjZlNzA5MWI4LTg5YTktNDZjNi05YzlkLTM3NGI1MzkwZjIwOCIsInVtYV9hdXRob3JpemF0aW9uIiwiZW50LWdyb3VwOmV0YWh6c3FlajBuNCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIHByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5pY2tuYW1lIjoia2VsdmlueXllIiwicHJlZmVycmVkX3VzZXJuYW1lIjoia2VsdmlueXllIiwiZW1haWwiOiJrZWx2aW55eWVAdGVuY2VudC5jb20ifQ.lzK3aDG57MtcRHjXqiHmIagtmPzE6CYJ8wOkax93k4WKxBXXvTtAWJWbOuMevYpN57jsv3QFnYDDrCwAvwFcA28GdVl2BVZ9EL4ZoR6-Bs2E4NkaNmvb4OysQezECKXONTnkj-L_7ofwCXLN7kPQgJ9jfjQlHbqtR8MlhYGTxJtrt5J6f86uoB2EjJg8TBoOwS2HovdblcsNRzJFu-8nDGvrdaeJYXlP3D6U52e-Bdd-KncQbwTsq9dh-Z68gjL7kk8xwH88B6Y5fF7hc4pDnf4wyxAguMJJ6IR7uLNdnL4gChNe_KEOtXrwRPRQYQEQr3-4jEJUVxDv0ar1BgloPw"

# 准备请求
url = "https://copilot.tencent.com/agenttool/v1/neodata"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "query": "2026年5月8日公募基金行业最新新闻",
    "channel": "neodata",
    "sub_channel": "workbuddy",
    "data_type": "all"
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"code: {data.get('code')}")
        print(f"msg: {data.get('msg')}")
        print(f"suc: {data.get('suc')}")
        
        # 保存到文件
        with open("neodata_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("响应已保存到 neodata_response.json")
        
        # 提取关键信息
        if data.get("suc") and data.get("data"):
            api_data = data["data"].get("apiData", {})
            doc_data = data["data"].get("docData", {})
            
            print("\n=== API数据 ===")
            if api_data.get("apiRecall"):
                for i, item in enumerate(api_data["apiRecall"][:3], 1):
                    print(f"{i}. type: {item.get('type')}")
                    print(f"   desc: {item.get('desc', '')[:100]}...")
                    
            print("\n=== 文档数据 ===")
            if doc_data.get("docRecall"):
                for i, group in enumerate(doc_data["docRecall"][:2], 1):
                    print(f"组 {i}: {group.get('extQuery', '')}")
                    if group.get("docList"):
                        for j, doc in enumerate(group["docList"][:2], 1):
                            print(f"  {j}. {doc.get('title', '')[:80]}...")
                            print(f"     来源: {doc.get('source', '')}, 时间: {doc.get('time', '')}")
    else:
        print(f"错误响应: {response.text}")
        
except Exception as e:
    print(f"请求异常: {str(e)}")
    import traceback
    traceback.print_exc()