import datetime
import os
import requests

# 康民署所有主要地區代碼
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
fa_code = "BADC"  # 羽毛球場

# 動態取得今日日期，並計算未來 7 日
today = datetime.date.today()
dates = [(today + datetime.timedelta(days=i)).isoformat() for i in range(7)]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}

# 確保儲存數據嘅資料夾存在
os.makedirs("data", exist_ok=True)

for date in dates:
  for dist in dist_codes:
    url = f"https://www.smartplay.lcsd.gov.hk/rest/facility-catalog/api/v1/publ/facilities?distCode={dist}&faCode={fa_code}&playDate={date}"
    try:
      response = requests.get(url, headers=headers, timeout=10)
      if response.status_code == 200:
        data = response.json()
        # 可以選擇性將每個區、每一日嘅 JSON 儲存低
        file_path = f"data/{date}_{dist}.json"
        with open(file_path, "w", encoding="utf-8") as f:
          import json

          json.dump(data, f, ensure_ascii=False)
        print(f"Successfully fetched & saved: Date {date}, District {dist}")
      else:
        print(
            f"Failed (Status {response.status_code}): Date {date}, District"
            f" {dist}"
        )
    except Exception as e:
      print(f"Error fetching Date {date}, District {dist}: {e}")
