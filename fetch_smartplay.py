from playwright.sync_api import sync_playwright
import json
import os
import time

def fetch_data():
    os.makedirs("data", exist_ok=True)
    dist_code = "ST" 
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 直接去 API 網址（用瀏覽器開，帶齊晒瀏覽器特徵同 Cookie）
        url = f"https://www.smartplay.lcsd.gov.hk/rest/facility-catalog/api/v1/publ/facilities?distCode={dist_code}&faCode=BADC&playDate=2026-08-15"
        
        print(f"Navigating to {url}")
        page.goto(url, wait_until="domcontentloaded")
        
        # 直接拎個網頁入面嘅文字（因為瀏覽器直接開 API 網址，入面全部都係 JSON 文字）
        content = page.inner_text("body")
        
        try:
            data = json.loads(content)
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Raw content: {content[:200]}")
            return
        
        # 儲存檔案
        file_path = f"data/today_{dist_code}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            
        browser.close()
        print(f"Data saved to {file_path}")

if __name__ == "__main__":
    fetch_data()
