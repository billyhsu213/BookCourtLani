import datetime
import json
import os
import time  # 1. 導入 time 模組
import requests

dist_codes = [
    "CW",
    "S",
    "E",
    "W",
    "KC",
    "KT",
    "SSP",
    "WTS",
    "YTM",
    "I",
    "KWT",
    "N",
    "SK",
    "ST",
    "TP",
    "TW",
    "TM",
    "YL",
]
fa_code = "BADC"

today = datetime.date.today()
dates = [(today + datetime.timedelta(days=i)).isoformat() for i in range(7)]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.smartplay.lcsd.gov.hk/",  # 2. 扮得貼近真實瀏覽器
}

os.makedirs("data", exist_ok=True)

for date in dates:
  for dist in dist_codes:
    url = f"https://www.smartplay.lcsd.gov.hk/rest/facility-catalog/api/v1/publ/facilities?distCode={dist}&faCode={fa_code}&playDate={date}"
    try:
      response = requests.get(url, headers=headers, timeout=10)
      if response.status_code == 200:
        data = response.json()

        # 檢查係咪真係拿到數據，定係回傳咗 error message
        if isinstance(data, dict) and data.get("code") == "error":
          print(f"Rate limited or error: Date {date}, District {dist}")
        else:
          file_path = f"data/{date}_{dist}.json"
          with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
          print(f"Successfully fetched & saved: Date {date}, District {dist}")

      else:
        print(f"Failed (Status {response.status_code}): {date}, {dist}")

      # 3. 每次請求後停 1 至 2 秒，避免過快被 block
      time.sleep(1.5)

    except Exception as e:
      print(f"Error fetching Date {date}, District {dist}: {e}")
      time.sleep(2)
