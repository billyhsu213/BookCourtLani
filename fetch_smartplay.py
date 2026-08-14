from playwright.sync_api import sync_playwright
import json
import os
import time

def fetch_data():
    os.makedirs("data", exist_ok=True)
    
    # 這裡只示範沙田區 (ST) 作為測試
    # 之後你可以再加其他地區代碼落去個 list 度
    dist_code = "ST" 
    
    with sync_playwright() as p:
        # 開啟一個隱形瀏覽器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 直接進入 SmartPLAY 查場頁面
        url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        page.goto(url, wait_until="networkidle")
        
        # 這裡會模擬真人操作：等個網頁載入完，抓取網頁內容
        # 其實 SmartPLAY 的數據通常藏在網頁的 JSON 響應中
        # 這裡我們監聽網頁發出的請求並攔截數據
        
        with page.expect_response("**/api/v1/publ/facilities?*") as response_info:
            # 這裡可以觸發查詢，不過直接進入頁面通常會自動載入
            time.sleep(5) # 等候一下讓內容載入
            
        response = response_info.value
        data = response.json()
        
        # 儲存檔案
        file_path = f"data/today_{dist_code}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            
        browser.close()
        print(f"Data saved to {file_path}")

if __name__ == "__main__":
    fetch_data()
