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
            # 只要見到包含 facilities 嘅 API 就截取落嚟
            if "/api/v1/publ/facilities" in response.url:
                try:
                    data_captured.append(response.json())
                except:
                    pass

        page.on("response", intercept_response)
        
        # 直接去帶有沙田區 (ST) 參數嘅查場頁面
        target_url = "https://www.smartplay.lcsd.gov.hk/facilities/search?distCode=ST&faCode=BADC"
        print(f"正在前往: {target_url}")
        page.goto(target_url, wait_until="networkidle")
        
        # 給予充足時間讓頁面載入並觸發 API
        page.wait_for_timeout(8000)
        
        # 儲存結果
        with open("data/today_ST.json", "w", encoding="utf-8") as f:
            json.dump(data_captured, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print("完成擷取！")

if __name__ == "__main__":
    fetch_data()
