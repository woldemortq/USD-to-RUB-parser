import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

from .models import CurrencyRate

MIN_INTERVAL_SECONDS = 10
_last_fetch_time = None

def fetch_usd_rate():
    global _last_fetch_time

    now = datetime.now()

    if _last_fetch_time and (now - _last_fetch_time).total_seconds() < MIN_INTERVAL_SECONDS:
        return CurrencyRate.objects.latest('timestamp')  # Возврат из базы, без запроса

    url = 'https://www.cbr.ru/currency_base/daily/'
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find('table', class_='data').find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if cols and cols[1].text.strip() == 'USD':
            rate = float(cols[4].text.replace(',', '.'))

            _last_fetch_time = now
            record = CurrencyRate.objects.create(rate=rate)
            return record

    raise ValueError("Не удалось найти курс USD")
