from playwright.sync_api import sync_playwright
import json
import os

def fetch_data():
    os.makedirs("data", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        target_url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        print(f"正在前往: {target_url}")
        page.goto(target_url, wait_until="networkidle", timeout=60000)
        
        # 給予充足時間讓 SPA 完全渲染
        page.wait_for_timeout(10000)
        
        # 直接拿取整個頁面的文字內容
        page_text = page.inner_text("body")
        
        # 儲存內容
        output_content = {
            "status": "text_extracted",
            "content_preview": page_text[:500], # 先看前 500 個字
            "full_length": len(page_text)
        }
        
        with open("data/today_ST.json", "w", encoding="utf-8") as f:
            json.dump(output_content, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print("完成！")

if __name__ == "__main__":
    fetch_data()
