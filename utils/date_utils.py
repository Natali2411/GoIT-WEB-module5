from datetime import datetime, timedelta


def get_date_in_past(days_back: int) -> str:
    today_date = datetime.now().date()
    past_date = today_date - timedelta(days=days_back)
    return past_date.strftime("%d.%m.%Y")
