from fastapi import FastAPI
from datetime import datetime, timedelta
import pytz

app = FastAPI()

WEEKDAY_MAP = {
    "monday": 0, "tuesday": 1, "wednesday": 2,
    "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
    "週一": 0, "週二": 1, "週三": 2,
    "週四": 3, "週五": 4, "週六": 5, "週日": 6
}

@app.get("/calculate-date")
def calculate_target_date(today_date: str, target_weekday: str):
    """
    today_date: 格式 YYYY-MM-DD，例如 2026-05-11
    target_weekday: 星期幾，例如 friday 或 週五
    """
    target_key = target_weekday.lower().strip()
    target_num = WEEKDAY_MAP.get(target_key)

    if target_num is None:
        return {"error": f"無法識別的星期：{target_weekday}"}

    today = datetime.strptime(today_date, "%Y-%m-%d")
    today_num = today.weekday()  # 0=週一, 6=週日

    days_ahead = (target_num - today_num) % 7
    if days_ahead == 0:
        days_ahead = 7  # 如果今天就是目標星期，往下一週算

    target_date = today + timedelta(days=days_ahead)

    return {
        "target_date": target_date.strftime("%Y-%m-%d"),
        "input_today": today_date,
        "input_weekday": target_weekday
    }