from playwright.sync_api import sync_playwright
import json
import os

def fetch_data():
    os.makedirs("data", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 記錄所有發出過的 API 網址，幫你「開箱驗貨」
        requested_urls = []
        
        def intercept_response(response):
            url = response.url
            # 把所有跟 api 相關或者 json 格式的回應網址都記低
            if "api" in url or ".json" in url:
                requested_urls.append(url)

        page.on("response", intercept_response)
        
        # 去主頁
        target_url = "https://www.smartplay.lcsd.gov.hk/facilities/search"
        print(f"正在前往: {target_url}")
        page.goto(target_url, wait_until="networkidle", timeout=60000)
        
        # 停留 8 秒，等頁面自己行晒所有初始化請求
        page.wait_for_timeout(8000)
        
        # 將所有捕捉到的網址寫入檔案
        output_content = {
            "status": "urls_captured",
            "urls": requested_urls if requested_urls else ["no_api_called"]
        }
        
        with open("data/today_ST.json", "w", encoding="utf-8") as f:
            json.dump(output_content, f, ensure_ascii=False, indent=2)
            
        browser.close()
        print("完成！")

if __name__ == "__main__":
    fetch_data()
