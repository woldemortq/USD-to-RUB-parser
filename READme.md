# Django Currency Parser

Этот проект — простой Django-приложение для получения текущего курса доллара (USD) к рублю (RUB) с сайта Центрального банка РФ.  
Периодически сохраняет историю последних 10 запросов и отображает её на веб-странице.

##  Функционал

- Получение курса USD к RUB с сайта [ЦБ РФ](https://www.cbr.ru/currency_base/daily/)
- Интервал между запросами: минимум 10 секунд
- Хранение последних 10 значений в JSON (`history.json`)
- Отображение текущего курса и истории на `/get-current-usd/`
- Адаптивный HTML-шаблон

##  Установка

1. Клонируй репозиторий:
```bash
git clone https://github.com/yourusername/currency-parser.git
cd currency-parser
docker build -t django-currency-uv .
docker run -p 8000:8000 django-currency-uv
```

## Если не работает докерфайл:
 - Можно просто установить зависимости вручную:
 - Django, BeautifulSoup, requests

"beautifulsoup4>=4.13.4",
    "django>=5.2.1",
    "requests>=2.32.3",
