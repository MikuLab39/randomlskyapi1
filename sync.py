import requests
import json
import os

# --- 唯一需要手动维护的地方：在列表里增加相册 ID ---
ALBUM_IDS = [3, 4, 5, 6, 7, 8] 

LSKY_TOKEN = os.getenv("LSKY_TOKEN")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_KV_ID = os.getenv("CF_KV_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")

def sync():
    headers = {"Authorization": LSKY_TOKEN, "Accept": "application/json"}
    
    for album_id in ALBUM_IDS:
        print(f"正在同步相册 {album_id}...")
        api_url = f"https://image.mikulab.com/api/v1/images?album_id={album_id}"
        
        try:
            res = requests.get(api_url, headers=headers).json()
            if res.get('status'):
                # 提取图片 URL
                urls = [img['links']['url'] for img in res['data']['data']]
                
                # 使用相册 ID 作为 KV 的 Key
                kv_endpoint = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/storage/kv/namespaces/{CF_KV_ID}/values/{album_id}"
                
                kv_headers = {
                    "Authorization": f"Bearer {CF_API_TOKEN}",
                    "Content-Type": "text/plain"
                }
                
                requests.put(kv_endpoint, headers=kv_headers, data=json.dumps(urls))
                print(f"相册 {album_id} 同步成功，共 {len(urls)} 张图片。")
        except Exception as e:
            print(f"相册 {album_id} 同步失败: {e}")

if __name__ == "__main__":
    sync()

