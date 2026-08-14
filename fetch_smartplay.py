from playwright.sync_api import sync_playwright
import requests
import json
import os

def fetch_data():
    os.makedirs("data", exist_ok=True)
    dist_code = "ST"  # 暫時先試沙田區
    play_date = "2026-08-15"  # 日期
    fa_code = "BADC"  # 羽毛球

    print("Step 1: 正在用瀏覽器獲取官方通行證 (Cookie)...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. 先去 SmartPLAY 首頁，讓伺服器發放合法的 Cookie
        page.goto("https://www.smartplay.lcsd.gov.hk/", wait_until="networkidle")
        
        # 2. 抽出瀏覽器拿到的所有 Cookies
        cookies = context.cookies()
        browser.close()

    # 將 Playwright 的 cookies 轉成 requests 格式
    cookie_dict = {c['name']: c['value'] for c in cookies}
    
    print("Step 2: 拿著通行證極速請求 API...")
    
    # 目標 API 網址
    url = f"https://www.smartplay.lcsd.gov.hk/rest/facility-catalog/api/v1/publ/facilities?distCode={dist_code}&faCode={fa_code}&playDate={play_date}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.smartplay.lcsd.gov.hk/"
    }
    
    # 用帶有 Cookie 的身份去打 API
    response = requests.get(url, headers=headers, cookies=cookie_dict, timeout=10)
    
    print(f"API 回應狀態碼: {response.status_code}")
    data = response.json()
    
    # 檢查結果
    if isinstance(data, dict) and data.get("code") == "error":
        print("❌ 失敗：還是被官方攔截了 (Error)")
    else:
        print("✅ 成功：順利繞過防護，拿到真實數據！")
        
    # 儲存檔案
    file_path = f"data/today_{dist_code}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"檔案已儲存至 {file_path}")

if __name__ == "__main__":
    fetch_data()
