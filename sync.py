import requests
import json
import os

# 配置信息（建议通过环境变量读取）
LSKY_API = "https://img.mikulab.com/api/v1/images?album_id=5"
LSKY_TOKEN = os.getenv("LSKY_TOKEN")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_KV_ID = os.getenv("CF_KV_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")

def sync():
    # 1. 从兰空图床获取图片
    headers = {"Authorization": LSKY_TOKEN, "Accept": "application/json"}
    res = requests.get(LSKY_API, headers=headers).json()
    
    if res['status']:
        urls = [img['links']['url'] for img in res['data']['data']]
        
        # 2. 推送到 Cloudflare KV
        # API 路径：/accounts/:account_id/storage/kv/namespaces/:namespace_id/values/:key_name
        kv_url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/storage/kv/namespaces/{CF_KV_ID}/values/images"
        
        kv_headers = {
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type": "text/plain"
        }
        
        put_res = requests.put(kv_url, headers=kv_headers, data=json.dumps(urls))
        if put_res.status_code == 200:
            print("Sync Success!")

if __name__ == "__main__":

    sync()
