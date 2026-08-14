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
            if "facilities" in response.url or "api/v1" in response.url:
                try:
                    data = response.json()
                    if data:
                        captured_data.append(data)
                except:
                    pass

        page.on("response", intercept_response)
        
        # 1. 去主頁
        target_url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        print(f"正在前往: {target_url}")
        page.goto(target_url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)
        
        # 2. 嘗試點擊「地區」下拉選單（SmartPLAY 通常用 select 或 custom dropdown）
        try:
            # 嘗試尋找並點擊地區選擇框
            page.click("text=地區", timeout=3000)
            page.wait_for_timeout(1000)
            # 嘗試點擊沙田
            page.click("text=沙田", timeout=3000)
            print("已成功在畫面選取沙田區！")
        except Exception as e:
            print(f"畫面點擊選單失敗，嘗試用 JS 直接觸發事件: {e}")
            
        # 給予時間讓頁面反應
        page.wait_for_timeout(8000)
        
        # 3. 寫入檔案
        output_content = captured_data if captured_data else {"status": "click_failed_no_data"}
        
        with open("data/today_ST.json", "w", encoding="utf-8") as f:
            json.dump(output_content, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print("完成！")

if __name__ == "__main__":
    fetch_data()
