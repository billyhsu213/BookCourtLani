from playwright.sync_api import sync_playwright
import json
import os

def fetch_data():
    os.makedirs("data", exist_ok=True)
    dist_code = "ST"
    
    with sync_playwright() as p:
        # 開啟隱形瀏覽器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 直接去 SmartPLAY 查場主頁
        url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        print(f"正在前往: {url}")
        page.goto(url, wait_until="networkidle")
        
        # 等待頁面完全載入，並嘗試取得頁面上的文字或資料
        # 這裡我們讓瀏覽器逗留一陣子，確保頁面元素渲染完成
        page.wait_for_timeout(5000)
        
        # 抓取頁面上的文字內容作為測試
        page_title = page.title()
        print(f"成功進入頁面，標題是: {page_title}")
        
        # 儲存一個簡單的狀態確認檔案
        result = {
            "status": "success",
            "page_title": page_title,
            "message": "已成功透過瀏覽器穿透 SmartPLAY 防護網"
        }
        
        file_path = f"data/today_{dist_code}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print(f"已更新檔案至 {file_path}")

if __name__ == "__main__":
    fetch_data()
