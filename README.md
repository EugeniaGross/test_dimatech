В корневой папке проекта создать файл .env. Пример содержания .env:</br>
```
POSTGRES_PORT=5432
POSTGRES_DB=payments
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345678
POSTGRES_HOST=db
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "123456789"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
SIGNATURE_SECRET_KEY = "gfdmhghif38yrf9ew0jkf32"
TESTING = 1 # указывается при проведении тестирования
```

Запуск проекта c помошью docker compose: </br>
```
docker compose up --build
```
Запуск проекта без docker compose (Windows): </br>
```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cd application
sanic main
```
Запуск проекта без docker compose (Linux, MacOS): </br>
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd application
sanic main
```

API документация доступна по адресу: http://localhost:8000/docs и http://localhost:8000/docs/swagger

Тестовый администратор:
```
email: test_admin@example.com
password: 12345678
```

Тестовый пользователь:
```
email: test_user@example.com
password: 12345678
```