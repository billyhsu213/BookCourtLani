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
        
        # 1. 去查場主頁
        target_url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        print(f"正在前往: {target_url}")
        page.goto(target_url, wait_until="networkidle")
        
        # 2. 等待頁面完全載入，嘗試尋找並點擊搜尋按鈕（通常按鈕有特定文字或 class）
        print("等待頁面載入並嘗試尋找搜尋按鈕...")
        page.wait_for_timeout(5000)
        
        # 嘗試點擊頁面上的「搜尋」或類似按鈕（這裡用通用的文字尋找）
        try:
            # 尋找包含「搜尋」或「查詢」的按鈕並點擊
            page.get_by_role("button", name=re.compile("搜尋|查詢|Search")).click(timeout=5000)
            print("已成功點擊搜尋按鈕！")
        except Exception as e:
            print(f"未能自動點擊按鈕（可能需要手動定位）：{e}")
            
        # 3. 給予充足時間讓 API 回應
        page.wait_for_timeout(8000)
        
        # 儲存結果
        with open("data/today_ST.json", "w", encoding="utf-8") as f:
            json.dump(data_captured, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print("完成擷取！")

if __name__ == "__main__":
    fetch_data()
