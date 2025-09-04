# Telegram-бот анекдотник с коллекцией анекдотов

Telegram-бот для просмотра и сохранения анекдотов из различных категорий. Все сайты находятся в файле app/config.py, где можно так же добавлять новые

---

## Используемые технологии

- Python 3.13.5
- [`Aiogram 3.х`](https://docs.aiogram.dev/en/latest/) — фреймворк для написания Telegram-бота
- [`Async SQLAlchemy 2.x`](https://docs.sqlalchemy.org/en/20/#) — ORM для работы с PostgresSQL
- `PostgresSQL` — используемая база данных
- `aiohttp + BeautifulSoup4 + lxml` — скрапинг анекдотов с сайтов

---

## Основной функционал

- `/start` — регистрация пользователя в базе данных
- `/joke` — отображает анекдоты
- `/favorites` — показывает избранные

---

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/newyearoldme/telegram-jokes-bot
cd telegram-jokes-bot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл .env и добавьте туда ваш Telegram-токен и данные для PostgresSQL:
```env
token=ВАШ_ТОКЕН_БОТА
db_url=postgresql+psycopg2://user:password@localhost/dbname
```

4. Запустите файл init_db.py для создания таблиц в базе данных
```bash
python init_db.py
```

5. Запустите бота:
```bash
poetry run python -m app.main
python -m app.main
```

---

## Лицензия
Проект опубликован под лицензией MIT. Используйте свободно, ссылайтесь на автора при необходимости.
