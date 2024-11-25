#!/bin/bash

# Максимальное количество попыток
RETRIES=0
DB_RETRIES=${DB_RETRIES:-5}

# Ожидаем доступности базы данных
until python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        dbname='$POSTGRES_DB',
        user='$POSTGRES_USER',
        password='$POSTGRES_PASSWORD',
        host='$DATABASE_HOST',
        port='$DATABASE_PORT'
    )
    conn.close()
    exit(0)
except:
    exit(1)
"; do
  RETRIES=$((RETRIES+1))
  echo "Waiting for postgres db... (attempt $RETRIES/$DB_RETRIES)"

  # Проверяем, не превышено ли максимальное количество попыток
  if [ "$RETRIES" -ge "$DB_RETRIES" ]; then
    echo "Failed db connection after $DB_RETRIES attempts. Terminating..."
    exit 1
  fi
  sleep 2
done

# Выполняем миграции
python manage.py makemigrations
python manage.py migrate

# Запускаем сервер
exec "$@"
