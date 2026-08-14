from playwright.sync_api import sync_playwright
import json
import os

def fetch_data():
    os.makedirs("data", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        captured_data = []
        def intercept_response(response):
            if "facility-catalog/api" in response.url or "facilities" in response.url:
                try:
                    data = response.json()
                    if data:
                        captured_data.append(data)
                except:
                    pass

        page.on("response", intercept_response)
        
        # 1. 去查場主頁
        target_url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        print(f"正在前往: {target_url}")
        page.goto(target_url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)
        
        # 2. 嘗試透過網址直接帶參數重載，或者直接讓頁面跳轉去帶有參數的網址
        # 因為 SmartPLAY 支援 URL 參數，我們直接去帶參數的網址
        search_with_params = "https://www.smartplay.lcsd.gov.hk/facilities/search?distCode=ST&faCode=BADC"
        print(f"帶參數重新載入: {search_with_params}")
        page.goto(search_with_params, wait_until="networkidle", timeout=60000)
        
        # 3. 給予充足時間讓它自動加載 API
        page.wait_for_timeout(10000)
        
        # 4. 寫入檔案
        output_content = captured_data if captured_data else {"status": "still_no_data"}
        
        with open("data/today_ST.json", "w", encoding="utf-8") as f:
            json.dump(output_content, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print("完成！")

if __name__ == "__main__":
    fetch_data()
