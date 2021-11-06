## Семестровая работа №1 "Виртуальная книжная полка"

Установка и запуск проекта

- `git clone` - клонировать репозиторий
- `python -m venv env` - создать виртуальное окружение
- `env\Scripts\activate.bat` - войти в виртуальное окружение
- `pip install -r requirements.txt` - установить зависимости
- установить PostgreSQL
- `app.config['SQLALCHEMY_DATABASE_URI'] = postgresql://user_name:password@localhost:5432(localhost)/name_db` - virtual_bookshelf/virtual_bookshelf/__init__.py
- `set FLASKAPP = app.py` - установить переменную
- `flask db init`
- `flask db update` - применить миграции к базе данных
- `flask run` - запуск сервера для разработки