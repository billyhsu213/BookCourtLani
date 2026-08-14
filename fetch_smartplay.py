from playwright.sync_api import sync_playwright
import json
import os

def fetch_data():
    os.makedirs("data", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        captured_data = []
        
        # 設置攔截網絡請求
        def handle_response(response):
            # 只要網頁背景有呼叫任何設施相關的 API，我們就把它整段抓下來
            if "facility-catalog/api" in response.url or "facilities" in response.url:
                try:
                    data = response.json()
                    if data: # 確保不是空資料
                        captured_data.append(data)
                except:
                    pass

        page.on("response", handle_response)
        
        # 直接去已選好沙田區的預設搜尋結果頁面（繞過首頁）
        # 讓瀏覽器直接去載入這個帶有數據的頁面
        target_url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        print(f"正在前往: {target_url}")
        
        # 載入頁面並等待網絡靜止
        page.goto(target_url, wait_until="networkidle", timeout=60000)
        
        # 給予額外時間讓頁面完全渲染
        page.wait_for_timeout(10000)
        
        # 強制寫入檔案（就算captured_data係空，也會寫入{"status": "empty"}以便git知道有更新）
        output_content = captured_data if captured_data else {"status": "no_data_captured"}
        
        file_path = "data/today_ST.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output_content, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print("完成！")

if __name__ == "__main__":
    fetch_data()
