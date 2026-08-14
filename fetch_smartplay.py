from playwright.sync_api import sync_playwright
import json
import os

def fetch_data():
    os.makedirs("data", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        data_captured = []
        def intercept_response(response):
            if "/api/v1/publ/facilities" in response.url:
                try:
                    data_captured.append(response.json())
                except:
                    pass

        page.on("response", intercept_response)
        
        target_url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        print(f"正在前往: {target_url}")
        page.goto(target_url, wait_until="networkidle")
        
        page.wait_for_timeout(5000)
        
        # 嘗試直接點擊畫面上的搜尋按鈕
        try:
            # 尋找有「搜尋」字眼的按鈕
            page.locator("button:has-text('搜尋')").click(timeout=5000)
            print("已點擊搜尋按鈕！")
        except:
            print("找不到指定按鈕，繼續等待...")
            
        page.wait_for_timeout(8000)
        
        with open("data/today_ST.json", "w", encoding="utf-8") as f:
            json.dump(data_captured, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print("完成！")

if __name__ == "__main__":
    fetch_data()
