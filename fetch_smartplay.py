from playwright.sync_api import sync_playwright
import json
import os

def fetch_data():
    os.makedirs("data", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 準備捕捉數據
        data_captured = []
        def intercept_response(response):
            if "/api/v1/publ/facilities" in response.url:
                data_captured.append(response.json())

        page.on("response", intercept_response)
        
        # 進入查場頁面，讓它自動觸發查詢
        page.goto("https://www.smartplay.lcsd.gov.hk/facilities/search", wait_until="networkidle")
        page.wait_for_timeout(8000) # 等待 8 秒讓數據載入
        
        # 儲存結果
        with open("data/today_ST.json", "w", encoding="utf-8") as f:
            json.dump(data_captured, f, ensure_ascii=False)
            
        browser.close()

if __name__ == "__main__":
    fetch_data()
