import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parent / 'history.json'
MAX_HISTORY = 10
MIN_INTERVAL_SECONDS = 10

_last_fetch_time = None
_last_rate = None


def get_usd_to_rub_cbr():
    global _last_fetch_time, _last_rate

    now = datetime.now()
    if _last_fetch_time and (now - _last_fetch_time).total_seconds() < MIN_INTERVAL_SECONDS:
        return _last_rate

    url = 'https://www.cbr.ru/currency_base/daily/'
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find('table', class_='data').find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if cols and cols[1].text.strip() == 'USD':
            value = float(cols[4].text.strip().replace(',', '.'))
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            rate_entry = {"timestamp": timestamp, "usd_to_rub": value}

            history = load_history()
            history.append(rate_entry)
            if len(history) > MAX_HISTORY:
                history = history[-MAX_HISTORY:]
            save_history(history)

            _last_fetch_time = now
            _last_rate = rate_entry
            return rate_entry

    raise ValueError("Курс USD не найден")


def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
